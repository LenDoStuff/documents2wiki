"""Offline checks for the Azure requests, embedded-text model input and PDF citations."""

import base64
from contextlib import redirect_stdout
from io import BytesIO, StringIO
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import httpx
import pymupdf as pdf
import requests
from urllib3.response import HTTPResponse

from pdf_evidence import API_VERSION, READ_MODEL, analysis_id, cite, digest, draft, main, prepare


DEMO = Path(__file__).resolve().parents[1] / "examples/water-damage"
LEGACY = DEMO / "evidence/D-03-v1"
SAMPLE = LEGACY / "read"
SOURCE = DEMO / "sources/D-03-v1.pdf"


def save_fixture(folder, source, version, result, searchable):
    folder.mkdir(exist_ok=True)
    source_hash, pdf_hash = digest(source.read_bytes()), digest(searchable)
    record = {"document_version_id": version, "analyzeResult": result, "source_sha256": source_hash,
              "searchable_sha256": pdf_hash, "analysis_id": analysis_id(source_hash, result, pdf_hash)}
    (folder / "read.json").write_text(json.dumps(record), encoding="utf-8")
    (folder / "searchable.pdf").write_bytes(searchable)


class PdfEvidenceTests(unittest.TestCase):
    def test_scan_to_searchable_copy_and_distinct_passages(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "report"
            original_hash = digest(SOURCE.read_bytes())
            with patch("pdf_evidence.azure_read", side_effect=AssertionError("unexpected Azure request")):
                extraction = prepare(SOURCE, bundle, "D-03-v1", SAMPLE)
                self.assertEqual(prepare(SOURCE, bundle, "D-03-v1"), extraction)
            self.assertEqual((bundle / "searchable.pdf").read_bytes(), (SAMPLE / "searchable.pdf").read_bytes())
            with pdf.open(SOURCE) as original, pdf.open(bundle / "searchable.pdf") as searchable:
                self.assertEqual(original_hash, digest(SOURCE.read_bytes()))
                self.assertFalse(any(p.get_text() for p in original))
                self.assertTrue(searchable[2].search_for("pressure test"))
                self.assertFalse(any(list(p.annots() or ()) for p in searchable))
                for before, after in zip(original, searchable):
                    self.assertEqual(before.get_pixmap(dpi=72).samples, after.get_pixmap(dpi=72).samples)
            wording = [
                "one possible explanation for the pattern of moisture.",
                "I recommend a pressure test of the supply pipe and connection",
            ]
            reports = [cite(bundle, 3, text) for text in wording]
            self.assertNotEqual(reports[0]["href"], reports[1]["href"])
            for label, report in zip(wording, reports):
                with pdf.open(bundle / report["href"].split("#")[0]) as doc:
                    page = doc[2]
                    self.assertIn(f"{page.xref} 0 R", doc.xref_get_key(doc.pdf_catalog(), "OpenAction")[1])
                    mark, = list(page.annots())
                    self.assertEqual("Highlight", mark.type[1])
                    self.assertEqual(label, " ".join(mark.info["content"].split()))
                    self.assertFalse(any(list(p.annots() or ()) for p in (doc[0], doc[1])))
                    hits = page.search_for(label, quads=True)
                    self.assertTrue(hits)
                    self.assertTrue(all(mark.rect.contains(hit.rect.tl + (1, 1)) for hit in hits))

    def test_rotated_crop_unicode_and_repeated_word_offsets(self):
        # This simulated Read output retains the native PDF crop and rotation.
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            source, fixture, bundle = directory / "rotated.pdf", directory / "result", directory / "bundle"
            with pdf.open() as doc:
                page = doc.new_page(width=380, height=240)
                page.insert_text((60, 105), "Pr\u00fcfung Alpha Alpha Alpha", fontsize=16)
                page.set_cropbox(pdf.Rect(20, 10, 360, 230))
                page.set_rotation(90)
                doc.save(source)
            with pdf.open(source) as doc:
                page = doc[0]
                content = "\U0001f50e "
                words = []
                for x0, y0, x1, y1, word, *_ in page.get_text("words"):
                    rect = pdf.Rect(x0, y0, x1, y1)
                    points = [p * page.rotation_matrix for p in (rect.tl, rect.tr, rect.br, rect.bl)]
                    words.append({"content": word, "span": {"offset": len(content), "length": len(word)},
                                  "polygon": [v / 72 for point in points for v in point]})
                    content += word + " "
                item = {"pageNumber": 1, "width": page.rect.width / 72, "height": page.rect.height / 72,
                        "unit": "inch", "words": words, "spans": [{"offset": 0, "length": len(content)}]}
            result = {"apiVersion": API_VERSION, "modelId": READ_MODEL, "stringIndexType": "unicodeCodePoint",
                      "content": content, "pages": [item]}
            save_fixture(fixture, source, "rotated", result, source.read_bytes())
            prepare(source, bundle, "rotated", fixture)
            with pdf.open(bundle / "searchable.pdf") as doc:
                page = doc[0]
                self.assertEqual(page.rotation, 90)
                self.assertEqual(3, len(page.search_for("Alpha")))
                positions = page.search_for("Pr\u00fcfung", quads=True)
                self.assertEqual(len(positions), 1)
                expected = pdf.Point(*words[0]["polygon"][:2]) * 72 * page.derotation_matrix
                self.assertLess(abs(positions[0].ul - expected), 2)
            with self.assertRaisesRegex(ValueError, "more than once"):
                cite(bundle, 1, "Alpha Alpha")
            start = words[2]["span"]["offset"]
            anchored = cite(bundle, 1, "Alpha Alpha", start)
            self.assertEqual((anchored["offset"], anchored["length"]), (start, len("Alpha Alpha")))
            with pdf.open(bundle / anchored["href"].split("#")[0]) as doc:
                page = doc[0]
                mark = page.first_annot
                expected = pdf.Point(*words[2]["polygon"][:2]) * 72 * page.derotation_matrix
                self.assertLess(abs(pdf.Point(mark.vertices[0]) - expected), 0.1)
                self.assertLess(abs(pdf.Point(mark.vertices[0]) - page.search_for("Alpha", quads=True)[1].ul), 0.1)
            # Re-extraction and missing positions must never silently redirect an old citation.
            words[2].pop("polygon")
            save_fixture(fixture, source, "rotated", result, source.read_bytes())
            with self.assertRaisesRegex(ValueError, "new bundle"):
                prepare(source, bundle, "rotated", fixture)
            other = directory / "missing-position"
            prepare(source, other, "rotated", fixture)
            partial = cite(other, 1, "Alpha Alpha", start)
            self.assertEqual(partial["location"], "page_only")
            self.assertEqual(partial["href"], "searchable.pdf#page=1")
            with self.assertRaisesRegex(ValueError, "No exact"):
                cite(other, 1, "pressure test")
            with self.assertRaisesRegex(ValueError, "outside"):
                cite(other, 2)
            item["width"] += 1  # different visible page frame
            save_fixture(fixture, source, "rotated", result, source.read_bytes())
            self.assertEqual(cite(fixture, 1, "Pr\u00fcfung")["location"], "page_only")
            item["width"] -= 1
            # Same dimensions, but Read's first word is displaced from the embedded one.
            words[0]["polygon"] = [v + 0.5 if i % 2 == 0 else v for i, v in enumerate(words[0]["polygon"])]
            save_fixture(fixture, source, "rotated", result, source.read_bytes())
            self.assertEqual(cite(fixture, 1, "Pr\u00fcfung")["location"], "page_only")

    def test_read_and_writer_send_the_right_pdfs(self):
        # Exercise both real SDKs up to the HTTP boundary, using the fictional claim.
        original = SOURCE.read_bytes()
        searchable = (SAMPLE / "searchable.pdf").read_bytes()
        result = json.loads((SAMPLE / "read.json").read_text(encoding="utf-8"))["analyzeResult"]
        operation = "https://read.invalid/documentintelligence/documentModels/prebuilt-read/analyzeResults/test-operation"
        env = {"AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT": "https://read.invalid", "AZURE_DOCUMENT_INTELLIGENCE_KEY": "fixture",
               "AZURE_OPENAI_ENDPOINT": "https://writer.invalid", "AZURE_OPENAI_API_KEY": "fixture", "AZURE_OPENAI_DEPLOYMENT": "writer"}
        calls = []

        def read_http(_session, method, url, **kw):
            target = urlsplit(url)
            calls.append((method, target.path))
            self.assertEqual(target.hostname, "read.invalid")
            self.assertEqual(parse_qs(target.query)["api-version"], [API_VERSION])
            response = requests.Response()
            response.url = url
            if method == "POST":
                self.assertTrue(target.path.endswith("/documentModels/prebuilt-read:analyze"))
                self.assertEqual(parse_qs(target.query)["output"], ["pdf"])
                self.assertEqual(parse_qs(target.query)["stringIndexType"], ["unicodeCodePoint"])
                self.assertIn(kw["headers"]["Content-Type"], ("application/octet-stream", "application/pdf"))
                self.assertEqual(kw["data"], original)
                response.status_code, data = 202, b""
                response.headers["Operation-Location"] = operation + "?api-version=" + API_VERSION
            elif target.path == urlsplit(operation).path:
                response.status_code, data = 200, json.dumps({"status": "succeeded", "analyzeResult": result}).encode()
                response.headers["Content-Type"] = "application/json"
            else:
                self.assertEqual(target.path, urlsplit(operation).path + "/pdf")
                response.status_code, data = 200, searchable
                response.headers["Content-Type"] = "application/pdf"
            response._content = data
            response._content_consumed = True
            response.raw = HTTPResponse(body=BytesIO(data), preload_content=False)
            return response

        quote = "I recommend a pressure test of the supply pipe and connection"
        passages = [{"text": "The engineer recommended a pressure test.", "page": 3, "quote": quote}]

        def writer_http(_client, request, **kw):
            self.assertEqual(str(request.url), "https://writer.invalid/openai/v1/responses")
            payload = json.loads(request.content)
            self.assertEqual(payload["model"], "writer")
            attachment, instruction = payload["input"][0]["content"]
            self.assertEqual((attachment["type"], attachment["filename"]), ("input_file", "D-03-v1.pdf"))
            prefix, encoded = attachment["file_data"].split(",", 1)
            self.assertEqual(prefix, "data:application/pdf;base64")
            self.assertEqual(base64.b64decode(encoded, validate=True), searchable)
            self.assertNotEqual(searchable, original)
            self.assertIn("Maintain one wiki", payload["instructions"])
            self.assertEqual(instruction["type"], "input_text")
            message = {"type": "message", "id": "msg_example", "role": "assistant", "status": "completed",
                       "content": [{"type": "output_text", "text": json.dumps({"statements": passages}), "annotations": []}]}
            return httpx.Response(200, json={"id": "resp_example", "object": "response", "status": "completed",
                                             "created_at": 1, "output": [message]}, request=request)

        with tempfile.TemporaryDirectory() as tmp, patch.dict("os.environ", env), \
                patch("requests.sessions.Session.request", new=read_http), \
                patch("azure.core.pipeline.transport.RequestsTransport.sleep"), patch("httpx.Client.send", new=writer_http):
            bundle = Path(tmp) / "evidence"
            output = StringIO()
            with patch("sys.argv", ["pdf_evidence", "prepare", str(SOURCE), str(bundle), "--version", "D-03-v1", "--draft"]), redirect_stdout(output):
                main()
            prepared = json.loads(output.getvalue())
            extraction = prepared["analysis_id"]
            self.assertEqual(Path(prepared["writer_input"]).read_bytes(), searchable)
            self.assertEqual(prepare(SOURCE, bundle, "D-03-v1"), extraction)
            self.assertEqual([method for method, _ in calls], ["POST", "GET", "GET"])
            self.assertEqual(json.loads((bundle / "read.json").read_text())["operation_id"], "test-operation")
            self.assertEqual((bundle / "searchable.pdf").read_bytes(), searchable)
            summary = prepared["draft"]
            self.assertEqual(summary["analysis_id"], extraction)
            self.assertEqual(summary["statements"][0]["citation"], cite(bundle, 3, quote))
            self.assertEqual(summary["statements"][0]["citation"]["location"], "highlight")
            passages[0]["quote"] = "The pressure test was completed."
            with self.assertRaisesRegex(ValueError, "No exact"):
                draft(bundle)

    def test_rejected_pairs_do_not_publish_and_old_citations_still_resolve(self):
        result = json.loads((SAMPLE / "read.json").read_text(encoding="utf-8"))["analyzeResult"]
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "new"
            with self.assertRaisesRegex(ValueError, "another source or version"):
                prepare(SOURCE, target, "other-version", SAMPLE)
            with self.assertRaisesRegex(ValueError, "earlier Layout extraction"):
                prepare(SOURCE, target, "D-03-v1", LEGACY)
            with patch("pdf_evidence.azure_read", return_value=(result, SOURCE.read_bytes(), "test")):
                with self.assertRaisesRegex(ValueError, "no embedded text"):
                    prepare(SOURCE, target, "D-03-v1")
            self.assertFalse(target.exists())
            prepare(SOURCE, target, "D-03-v1", SAMPLE)
            (target / "searchable.pdf").write_bytes(SOURCE.read_bytes())
            with self.assertRaisesRegex(ValueError, "no longer matches"):
                prepare(SOURCE, target, "D-03-v1")
        old = cite(LEGACY, 3, result["content"][686:819])
        self.assertTrue((LEGACY / old["href"].split("#")[0]).is_file())
        self.assertIn("a2abb7d9c043", old["href"])

    def test_worked_answer_and_wiki_open_the_same_exact_source(self):
        root = DEMO.parents[1]
        spec = (root / "prototype/http-api.md").read_text(encoding="utf-8")
        answer = json.loads(re.search(r"\x60{3}json\n(.*?)\n\x60{3}", spec, re.S)[1])
        saved, = answer["citations"]
        local = cite(SAMPLE, saved["page"], saved["quote"], saved["offset"])
        route = f"/api/v1/claims/{answer['claim_id']}/revisions/{answer['revision']}/documents/{local['document_version_id']}/"
        self.assertEqual(saved, dict(local, href=route + local["href"]))
        wiki = (DEMO / "wiki/action-plan.md").read_text(encoding="utf-8")
        self.assertIn("evidence/D-03-v1/read/" + local["href"], wiki)
        self.assertIn(" ".join(saved["quote"].split()), wiki)


if __name__ == "__main__":
    unittest.main()
