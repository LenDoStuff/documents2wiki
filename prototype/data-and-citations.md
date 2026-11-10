# Claim files and citations

A **document version** identifies an immutable original. A **revision** identifies the set of documents and wiki pages available to a reader at a point in time. A **run** records the questions answered against that revision. These IDs let a handler reopen an answer after new evidence arrives.

```text
C-1042/
  originals/
    D-01-v1.pdf
    D-02-v1.pdf
    D-03-v1.pdf
  evidence/D-03-v1/read/
    read.json          source and PDF fingerprints, Read text, page and word positions
    searchable.pdf     the PDF returned by Read and attached to the writer
    citations/         highlighted PDFs created when a passage is cited
  revisions/r3/
    claim.json
    wiki/
      index.md
      file-overview.md
      chronology.md
      issues.md
      action-plan.md
      documents/
        D-01-v1.md
        D-02-v1.md
        D-03-v1.md
  runs/run-001/
    checklist.json
    answers.json
```

The proposed `claim.json` records which original versions and extraction IDs belong to the revision, their titles, page counts, immutable paths and text in physical page order. Keep supplied receipt dates distinct from upload timestamps and dates reported inside documents. Source summaries describe the version they summarize, including when a later document corrects it.

## One citation from answer to source

Both a wiki footnote and a research answer display the supporting source words. For PDFs the saved citation carries `document_version_id`, `analysis_id`, physical `page`, `quote`, `offset`, `length`, and the resolved `href`. The offset and length refer to the saved Read text in Unicode code points. The extraction ID binds the original, the Read result and the downloaded PDF. Count physical pages from 1, including the cover. The application checks that the document and extraction belong to the selected claim revision before opening the PDF.

For example, the engineer’s opinion and test recommendation are on the same page. They get distinct footnote IDs and distinct links. In this excerpt from the example wiki, the OKF source and the footnote point to the same highlighted passage. [Example issues page](../examples/water-damage/wiki/issues.md) · [OKF specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)

```markdown
---
type: Claim actions
title: Open actions
sources:
  - id: D-03-v1-p3-test
    resource: ../evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3
---

The engineer recommended a pressure test.[^D-03-v1-p3-test]

[^D-03-v1-p3-test]: [Engineering report, p. 3 — “I recommend a pressure test of the supply pipe and connection…”](../evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3).
```

The recommendation has a quote to highlight. The answer “no result was found in the three documents at this revision” describes the scope and outcome of the search. It does not have a source passage asserting that no test ever took place. [Highlighted recommendation](../examples/water-damage/evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3) · [PDF command and fallbacks](pdf-citations.md)

## Applying a small edit

The writer can name a page, heading and the entry to amend. The publisher checks the existing wording against the specified revision, resolves supplied PDF wording against pages read by the writer, and produces the source links. If the entry moved or another upload published first, reread the current entry before applying the edit.

For the signed correction in the example, the proposal can target the exact line in the `r3` chronology. [Existing entry](../examples/water-damage/wiki/chronology.md#events) · [Correction, p. 1](../examples/water-damage/sources/D-04-v1.md#pdf-page-1)

```json
{
  "page_id": "chronology",
  "heading": "Events",
  "replace": "- **12 May** — Engineer’s site inspection, as recorded in the engineering report.[^D-03-v1-p2-inspection]",
  "text": "- **13 May** — Engineer’s site inspection. The signed addendum corrects the 12 May date in the original report.",
  "citations": [
    {"document_version_id": "D-04-v1", "locator": "pdf-page-1", "quote": "My site diary confirms the inspection was on 13 May."},
    {"document_version_id": "D-03-v1", "page": 2, "quote": "I recorded the inspection on 12 May."}
  ]
}
```

Store a submission ID with each completed arrival. Within one claim, a replay with the same ID and content returns the published result. A reused ID with conflicting content needs a distinct submission. Stage the complete revision before making it visible so a failed write leaves readers with the previous complete file.
