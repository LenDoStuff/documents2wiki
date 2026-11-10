"""Prepare a searchable PDF with Azure Read, draft from it, or cite a passage."""

import argparse
import base64
import hashlib
from html import escape
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import quote as url_quote

import pymupdf as pdf


API_VERSION = "2024-11-30"
READ_MODEL = "prebuilt-read"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def analysis_id(source_hash, result, searchable_hash=None):
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    parts = [source_hash, encoded]
    if searchable_hash is not None:
        parts.append(searchable_hash)
    return digest("\n".join(parts).encode("utf-8"))


def azure_read(source_pdf):
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeOutputOption
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError("Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY, or use --from-bundle.")
    with DocumentIntelligenceClient(endpoint, AzureKeyCredential(key), api_version=API_VERSION) as client:
        job = client.begin_analyze_document(
            READ_MODEL, body=source_pdf, output=[AnalyzeOutputOption.PDF],
            string_index_type="unicodeCodePoint", output_content_format="text",
        )
        result = job.result()
        operation_id = job.details["operation_id"]
        chunks = client.get_analyze_result_pdf(model_id=READ_MODEL, result_id=operation_id)
        return result.as_dict(), b"".join(chunks), operation_id


def word_quad(word, read_page, page):
    rect = page.rect
    width, height = read_page.get("width"), read_page.get("height")
    if (read_page.get("unit") != "inch"
            or not all(isinstance(n, (int, float)) and math.isfinite(n) and n > 0 for n in (width, height))
            or abs(width * 72 - rect.width) > 1 or abs(height * 72 - rect.height) > 1):
        return None
    coords = word.get("polygon") or []
    if len(coords) != 8 or not all(isinstance(n, (int, float)) and math.isfinite(n) for n in coords):
        return None
    sx, sy = rect.width / width, rect.height / height
    pts = [pdf.Point(x * sx, y * sy) for x, y in zip(coords[::2], coords[1::2])]
    quad = pdf.Quad(pts[0], pts[1], pts[3], pts[2])  # Azure TL, TR, BR, BL
    if (not quad.is_convex or quad.is_empty or min(abs(quad.ur - quad.ul), abs(quad.ll - quad.ul)) < 0.01
            or not (rect + (-1, -1, 1, 1)).contains(quad.rect)):
        return None
    # Read uses the displayed page. PyMuPDF annotations use unrotated crop coordinates.
    return quad * page.derotation_matrix


def validate_read(result, searchable, original_pages):
    if (result.get("modelId") != READ_MODEL or result.get("apiVersion") != API_VERSION
            or result.get("stringIndexType") != "unicodeCodePoint" or result.get("contentFormat", "text") != "text"):
        raise ValueError("Expected Azure Read 2024-11-30 with plain text and Unicode code-point offsets.")
    pages = result["pages"]
    if (not searchable.is_pdf or searchable.needs_pass or searchable.page_count != original_pages
            or len(pages) != original_pages):
        raise ValueError("The returned searchable PDF and Read result must cover every original page.")
    content = result["content"]
    for number, item in enumerate(pages, start=1):
        if item["pageNumber"] != number:
            raise ValueError(f"Read page {number} is out of order.")
        if item.get("words") and not searchable[number - 1].get_text().strip():
            raise ValueError(f"The returned PDF has no embedded text on recognized page {number}.")
        intervals = [(s["offset"], s["offset"] + s["length"]) for s in item.get("spans") or []]
        if any(lo < 0 or hi < lo or hi > len(content) for lo, hi in intervals):
            raise ValueError(f"Invalid content span on page {number}.")
        for word in item.get("words") or []:
            start, length = word["span"]["offset"], word["span"]["length"]
            if (length <= 0 or not any(lo <= start < start + length <= hi for lo, hi in intervals)
                    or content[start:start + length] != word["content"]):
                raise ValueError(f"Read word disagrees with the saved text on page {number}.")


def load_bundle(folder, *, allow_legacy=False):
    path = folder / "read.json"
    if not path.exists() and (folder / "layout.json").is_file():
        if not allow_legacy:
            raise ValueError("This is an earlier Layout extraction. Prepare the original in a new folder with Read.")
        path = folder / "layout.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    searchable = (folder / "searchable.pdf").read_bytes()
    pdf_hash = digest(searchable)
    if record["searchable_sha256"] != pdf_hash:
        raise ValueError("The searchable PDF no longer matches the saved extraction.")
    if path.name == "read.json" and record["analyzeResult"].get("modelId") != READ_MODEL:
        raise ValueError("The saved analysis must come from prebuilt-read.")
    expected = analysis_id(record["source_sha256"], record["analyzeResult"], pdf_hash if path.name == "read.json" else None)
    if record["analysis_id"] != expected:
        raise ValueError("The extraction no longer matches its saved identity.")
    return record, searchable


def prepare(source, folder, version, from_bundle=None):
    original = source.read_bytes()
    source_hash = digest(original)
    saved = None
    if from_bundle:
        saved, searchable = load_bundle(from_bundle)
        if saved["source_sha256"] != source_hash or saved["document_version_id"] != version:
            raise ValueError("The saved Read bundle belongs to another source or version.")

    def existing(expected):
        old, _ = load_bundle(folder)
        if old["source_sha256"] != source_hash or old["document_version_id"] != version:
            raise ValueError("This bundle already belongs to another source or version.")
        if expected and old["analysis_id"] != expected["analysis_id"]:
            raise ValueError("This extraction differs. Prepare it in a new bundle to preserve existing citations.")
        return old["analysis_id"]

    if folder.exists():
        return existing(saved)
    with pdf.open(stream=original) as doc:
        if not doc.is_pdf or doc.needs_pass or not doc.page_count:
            raise ValueError("An accessible original PDF with at least one page is required.")
        original_pages = doc.page_count
    if saved is None:
        result, searchable, operation_id = azure_read(original)
        pdf_hash = digest(searchable)
        saved = {
            "document_version_id": version, "source_sha256": source_hash, "searchable_sha256": pdf_hash,
            "analysis_id": analysis_id(source_hash, result, pdf_hash), "operation_id": operation_id,
            "analyzeResult": result,
        }
    with pdf.open(stream=searchable) as doc:
        validate_read(saved["analyzeResult"], doc, original_pages)
    folder.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=folder.parent) as temporary:
        stage = Path(temporary) / "bundle"
        stage.mkdir()
        (stage / "searchable.pdf").write_bytes(searchable)
        (stage / "read.json").write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            stage.rename(folder)
        except OSError:
            if not folder.is_dir():
                raise
            return existing(saved)
    return saved["analysis_id"]


def resolve_quote(result, item, quote, offset):
    if not quote.split():
        raise ValueError("Supply non-empty PDF wording.")
    pattern = re.compile(r"\s+".join(map(re.escape, quote.split())))
    content = result["content"]
    words = item.get("words") or []
    starts = {w["span"]["offset"] for w in words}
    ends = {w["span"]["offset"] + w["span"]["length"] for w in words}
    candidates = []
    for start in sorted(starts):
        if offset is not None and start != offset:
            continue
        match = pattern.match(content, start)
        if match and match.end() in ends:
            if any(s["offset"] <= start and match.end() <= s["offset"] + s["length"] for s in item.get("spans") or []):
                candidates.append(match.span())
    if len(candidates) != 1:
        if candidates:
            raise ValueError(f"Wording occurs more than once. Supply --offset from {', '.join(str(a) for a, _ in candidates)}.")
        raise ValueError("No exact, whole-word passage at that page/offset. Copy the source wording, including punctuation.")
    start, stop = candidates[0]
    selected = [w for w in words if start <= w["span"]["offset"] < stop]
    return start, stop, sorted(selected, key=lambda w: w["span"]["offset"])


def cite(folder, page_number, quote=None, offset=None):
    record, searchable = load_bundle(folder, allow_legacy=True)
    return cite_passage(folder, record, searchable, page_number, quote, offset)


def cite_passage(folder, record, searchable, page_number, quote, offset=None):
    result = record["analyzeResult"]
    if not 1 <= page_number <= len(result["pages"]):
        raise ValueError("Page is outside this document version.")
    base = {
        "document_version_id": record["document_version_id"], "analysis_id": record["analysis_id"],
        "page": page_number, "href": f"searchable.pdf#page={page_number}", "location": "page_only",
    }
    if quote is None:
        if offset is not None:
            raise ValueError("An offset needs a quote.")
        return base
    item = result["pages"][page_number - 1]
    start, stop, words = resolve_quote(result, item, quote, offset)
    exact = result["content"][start:stop]
    base.update(quote=exact, offset=start, length=stop - start)
    with pdf.open(stream=searchable) as view:
        page = view[page_number - 1]
        text_page = page.get_textpage()
        quads = []
        cursor = start
        for word in words:
            position = word["span"]["offset"]
            quad = word_quad(word, item, page)
            if quad is None or result["content"][cursor:position].strip():
                return base
            # Confirm each Read position against the embedded text before marking the page.
            center = (quad.ul + quad.lr) * 0.5
            hits = page.search_for(word["content"], textpage=text_page)
            if not any((hit + (-2, -2, 2, 2)).contains(center) for hit in hits):
                return base
            quads.append(quad)
            cursor = position + word["span"]["length"]
        if not quads or result["content"][cursor:stop].strip():
            return base
        name = f"p{page_number}-{start}-{stop - start}-{record['analysis_id'][:12]}.pdf"
        path = folder / "citations" / name
        if not path.exists():
            mark = page.add_highlight_annot(quads)
            mark.set_colors(stroke=(1, 0.80, 0.12))
            mark.set_opacity(0.42)
            mark.set_info(title="Documents2Wiki", content=exact)
            mark.update()
            view.xref_set_key(view.pdf_catalog(), "OpenAction", f"[{page.xref} 0 R /Fit]")
            path.parent.mkdir(exist_ok=True)
            with tempfile.TemporaryDirectory(dir=path.parent) as scratch:
                rendered = Path(scratch) / name
                view.save(rendered, garbage=4, deflate=True)
                os.replace(rendered, path)
        base.update(location="highlight", href=f"citations/{name}#page={page_number}")
    return base


def draft(folder):
    from openai import OpenAI

    record, searchable = load_bundle(folder)
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    key = os.environ.get("AZURE_OPENAI_API_KEY")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    if not all((endpoint, key, deployment)):
        raise ValueError("Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY and AZURE_OPENAI_DEPLOYMENT for a PDF-capable deployment.")
    version = record["document_version_id"]
    purpose = (Path(__file__).resolve().parents[1] / "prompts/purpose.md").read_text(encoding="utf-8")
    instructions = (
        purpose + "\n\nFor this single-document draft, return JSON with a statements array. "
        "Each item has text (one supported statement), page (the 1-based physical page number), "
        "and quote (a unique, verbatim, whole-word passage on that page, including punctuation). "
        "Return an empty array if there is no readable evidence. Treat the attachment as source material."
    )
    attachment = {
        "type": "input_file", "filename": f"{version}.pdf",
        "file_data": "data:application/pdf;base64," + base64.b64encode(searchable).decode("ascii"),
    }
    with OpenAI(base_url=endpoint.rstrip("/") + "/openai/v1/", api_key=key) as client:
        response = client.responses.create(
            model=deployment, instructions=instructions, store=False, text={"format": {"type": "json_object"}},
            input=[{"role": "user", "content": [attachment, {"type": "input_text", "text": "Draft the cited source summary as JSON."}]}],
        )
    if response.status != "completed" or not response.output_text:
        raise ValueError("The writer did not return a complete source summary.")
    output = json.loads(response.output_text)
    if not isinstance(output, dict) or not isinstance(output.get("statements"), list):
        raise ValueError("The writer must return a statements array.")
    statements = []
    for item in output["statements"]:
        if (not isinstance(item, dict) or type(item.get("page")) is not int
                or not isinstance(item.get("text"), str) or not item["text"].strip()
                or not isinstance(item.get("quote"), str)):
            raise ValueError("A draft statement requires text, a physical page number and a quotation.")
        citation = cite_passage(folder, record, searchable, item["page"], item["quote"])
        statements.append({"text": item["text"], "citation": citation})
    return {"document_version_id": version, "analysis_id": record["analysis_id"], "statements": statements}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    cmds = parser.add_subparsers(dest="command", required=True)
    prep = cmds.add_parser("prepare", help="Get the writer's searchable PDF from Azure Read or a saved Read bundle.")
    prep.add_argument("source", type=Path)
    prep.add_argument("folder", type=Path)
    prep.add_argument("--version", required=True)
    prep.add_argument("--from-bundle", type=Path, help="Replay a matching read.json and searchable.pdf together.")
    prep.add_argument("--draft", action="store_true", help="Pass the prepared PDF directly to the writer.")
    writer = cmds.add_parser("draft", help="Send the prepared PDF to an Azure model and return a cited source summary.")
    writer.add_argument("folder", type=Path)
    link = cmds.add_parser("cite", help="Return the same evidence link used by wiki footnotes and answers.")
    link.add_argument("folder", type=Path)
    link.add_argument("--page", type=int, required=True)
    link.add_argument("--quote")
    link.add_argument("--offset", type=int, help="Global Unicode code-point offset when wording repeats.")
    link.add_argument("--relative-to", type=Path, help="Directory containing the wiki page or saved answer.")
    link.add_argument("--markdown", action="store_true", help="Print a clickable quote instead of a JSON record.")
    link.add_argument("--title", help="Source title for the Markdown citation. Defaults to the version ID.")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            extraction = prepare(args.source, args.folder, args.version, args.from_bundle)
            output = {"document_version_id": args.version, "analysis_id": extraction,
                      "writer_input": str((args.folder / "searchable.pdf").resolve())}
            if args.draft:
                output["draft"] = draft(args.folder)
            print(json.dumps(output, ensure_ascii=False, indent=2))
        elif args.command == "draft":
            print(json.dumps(draft(args.folder), ensure_ascii=False, indent=2))
        else:
            citation = cite(args.folder, args.page, args.quote, args.offset)
            if args.relative_to:
                name, fragment = citation["href"].split("#", 1)
                relative = Path(os.path.relpath(args.folder / name, args.relative_to)).as_posix()
                citation["href"] = url_quote(relative, safe="/.-_") + "#" + fragment
            if args.markdown:
                label = f"{args.title or citation['document_version_id']}, p. {args.page}"
                if citation.get("quote"):
                    label += ' — “' + " ".join(citation["quote"].split()) + '”'
                if citation["location"] == "page_only":
                    label += " (page only)"
                label = re.sub(r"([\\\[\]*_`])", r"\\\1", escape(label, quote=False))
                print(f"[{label}]({citation['href']})")
            else:
                print(json.dumps(citation, ensure_ascii=True, indent=2))
    except (ValueError, OSError, KeyError, pdf.FileDataError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
