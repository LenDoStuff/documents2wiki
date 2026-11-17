# Possible HTTP operations

This sketch connects a claims platform or browser to the two MVP outputs. A completed claim-file submission starts document segmentation and wiki creation. The research agent uses the published revision to generate a subrogation report. The paths below are illustrative and relative to `/api/v1/claims/{claim_id}`.

| Request | Example behavior |
| --- | --- |
| `POST /documents` | Accept one combined claim-file PDF, a claim-scoped `submission_id` and an optional receipt timestamp. Run Read, detect logical document boundaries and pass the mapped pages to the writer. Record each logical document’s version, extraction ID and physical pages in the revision. A matching retry returns the earlier result. |
| `GET /wiki` | Return the latest revision and its page index. |
| `GET /revisions/{revision}/wiki/{page_id}` | Return the named wiki page from the selected revision. |
| `GET /revisions/{revision}/documents/{version}/pages/{page}` | Return the Read text of the physical page, global word offsets, and the original and searchable PDF links. Resolve the version and extraction against this claim and revision. |
| `GET /revisions/{revision}/documents/{version}/citations/{citation_id}` | Resolve a stored passage for this claim, revision and extraction. Serve the searchable PDF with the selected words highlighted. A page-only result links to the reading copy with its physical page number. |
| `POST /checklist-runs` | Run the selected subrogation preset against a published revision. Save its ID, version and ordered questions, then return a report with one answer per question and review coverage for every logical document in the revision. |
| `GET /checklist-runs/{run_id}` | Reopen the report with its revision, questions, answers, citations, gaps, usage and document coverage. |

For example, suppose the agent opened all three records at `r3` to answer the pressure-test question. The example below shows one answer in that report. The read history is illustrative. The PDF citation comes from the worked example. The local CLI returns a bundle-relative link. The proposed service can expose the same citation through its revision-scoped route.

```json
{
  "claim_id": "C-1042",
  "revision": "r3",
  "question_id": "q1",
  "text": "What was the pressure-test result?",
  "status": "not_found",
  "answer": "The engineer recommended a pressure test. No result was found in the three documents at r3.",
  "citations": [
    {
      "document_version_id": "D-03-v1",
      "analysis_id": "86217db25bf55bd2f33566fc13b1ac29d0ee1e83529535b31952c7ad757a95ea",
      "page": 3,
      "href": "/api/v1/claims/C-1042/revisions/r3/documents/D-03-v1/citations/p3-686-133-86217db25bf5.pdf#page=3",
      "location": "highlight",
      "quote": "I recommend a pressure test of the supply pipe and connection\nto help distinguish this possibility from another route of water entry.",
      "offset": 686,
      "length": 133
    }
  ],
  "gap": "A completed test report or measurements.",
  "review": {
    "wiki_pages_opened": ["action-plan"],
    "documents_searched": ["D-01-v1", "D-02-v1", "D-03-v1"],
    "source_pages_opened": {"D-01-v1": [1], "D-02-v1": [1], "D-03-v1": [1, 2, 3]},
    "unreadable_pages": []
  }
}
```

Distinguish an answer supported by the evidence (`answered`), a partial answer (`partial`), conflicting accounts (`conflicting_evidence`), a completed search that found no requested evidence (`not_found`), and a search interrupted before the relevant sources were checked (`incomplete_search`). Keep the question’s own coverage with its answer. The report also shows the combined document coverage, stop reason and resource use for the run. [Report coverage and example](../approach/agent-retrieval.md#what-the-report-shows)

In a rendered answer the source title, page and quoted wording use the returned link. [Engineering report, p. 3 — “I recommend a pressure test of the supply pipe and connection…”](../examples/water-damage/evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3)
