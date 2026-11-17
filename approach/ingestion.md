# From incoming document to updated wiki

Intake receives **one combined claim-file PDF** and detects the boundaries of the logical documents inside it. A logical document is a claim record such as a loss notice, work order or engineering report. A multipage report gets one inventory entry, one version ID and one summary. Each entry points to the physical pages of the original upload. [Implementation steps and segmentation check](implementation-plan.md#1-segment-the-claim-file)

The writer reads the **searchable PDF returned by Azure Document Intelligence Read**. The same analysis identifies where each word falls on the page.

## PDF ingestion workflow

```mermaid
flowchart TD
    P["PDF arrives · retain original"] --> R["Azure Document Intelligence Read"]
    R --> F["Searchable PDF with embedded text"]
    R --> T["Page text and word positions"]
    F --> B["Detect logical documents and map their physical pages"]
    T --> B
    B --> W["Writer reads each record and amends affected entries"]
    F --> A["Later, a research agent checks a source page"]
    W --> C["Cite the physical page and exact words"]
    A --> C
    T --> H["Match the quote and highlight it in a copy of the PDF"]
    C --> H
```

1. **Keep the original.** Save the incoming claim-file PDF and send its bytes to `prebuilt-read` with `output=pdf` (API `2024-11-30`).
2. **Collect both results from that operation.** Download Azure’s PDF with its embedded text as `searchable.pdf`. Save the Read result, including physical page numbers, character offsets and word positions, in `read.json`. Keep the pair together for this version. [Microsoft’s searchable PDF documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-read?view=doc-intel-4.0.0#searchable-pdfs)
3. **Find the records.** Use adjacent pages to identify starts and continuations. Save each logical document’s range in the inventory. Record ambiguous boundaries and keep the affected pages available to the writer and the report agent.
4. **Give the writer the document’s PDF pages.** Supply the searchable pages with their mapping to the physical pages of the upload. The writer can inspect wording, diagrams and stamps. When it cites evidence, resolve the quote in `read.json` on the mapped page. [Writing prompt](../prompts/purpose.md) · [Example original scan](../examples/water-damage/sources/D-03-v1.pdf) · [Example writer input](../examples/water-damage/evidence/D-03-v1/read/searchable.pdf)

## Updating the claim wiki

- **First build.** Give one writer the documents already on file. It creates a cited summary per source version, the four claim pages and their index. [Claim page structure](claim-wiki.md)
- **Later arrival.** The writer summarizes the new version, lists it once and opens the entries its evidence could change. It amends the affected wording and cites the page that justifies the change. A routine receipt may need only its summary and inventory links. A conflicting account is attributed alongside the earlier one.

The agent publishes the wiki and inventory together as a revision once the changes and their source links have been assembled. The preset report can then run against that revision. A repeat delivery of the same submission returns the saved revision. Earlier handovers remain available. [Storage design](../prototype/data-and-citations.md)

## What a PDF citation opens

The writer supplies the document version, physical page and **exact supporting words**. The citation command matches the quote in the saved extraction and uses the selected words’ positions to create a PDF with that passage highlighted. A wiki footnote and a later research answer can use the same link. Opening it takes the handler to that page with the quotation visible.

For example, the water-damage wiki records a recommendation and leaves the test result open. The highlight shows exactly what the engineer said. [Open action](../examples/water-damage/wiki/action-plan.md) · [Engineering report, p. 3 — “I recommend a pressure test of the supply pipe and connection to help distinguish this possibility from another route of water entry.”](../examples/water-damage/evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3)

If the wording occurs twice on a page, select the intended occurrence by its character offset. For evidence spanning pages, cite each page’s passage separately. Review a quote if it fails to match or the extracted wording differs from the visible source. When the page is known but the words cannot be positioned, label the link **Page only**. The prototype can prepare one PDF, send it to a writer for a cited source summary and generate its highlights. [Run the PDF commands](../prototype/pdf-citations.md)

## One amendment

The original report recorded the inspection on **12 May**. A signed addendum corrects it to **13 May**. The updated chronology has one inspection entry and cites both records so the handler can trace the change. [Original inspection record, p. 2](../examples/water-damage/evidence/D-03-v1/read/citations/p2-286-98-86217db25bf5.pdf#page=2) · [Signed addendum, p. 1](../examples/water-damage/sources/D-04-v1.md#pdf-page-1)
