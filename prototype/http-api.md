# Possible HTTP operations

This sketch connects a claims platform or browser to two operations. A completed document submission starts the writer. A question or checklist runs against the revision the handler selected. The paths below are illustrative and relative to `/api/v1/claims/{claim_id}`.

| Request | Example behavior |
| --- | --- |
| `POST /documents` | Accept a PDF, a claim-scoped `submission_id` and an optional original receipt timestamp. A completed submission triggers Read and sends the returned searchable PDF to the writer. Save its extraction ID with the published revision. A matching retry returns the earlier result. |
| `GET /wiki` | Return the latest revision and its page index. |
| `GET /revisions/{revision}/wiki/{page_id}` | Return the named wiki page from the selected revision. |
| `GET /revisions/{revision}/documents/{version}/pages/{page}` | Return the Read text of the physical page, global word offsets, and the original and searchable PDF links. Resolve the version and extraction against this claim and revision. |
| `GET /revisions/{revision}/documents/{version}/citations/{citation_id}` | Resolve a stored passage for this claim, revision and extraction. Serve the searchable PDF with the selected words highlighted. A page-only result links to the reading copy with its physical page number. |
| `POST /checklist-runs` | Accept one or more ordered questions and a revision. Return one cited answer per question in the original order. |
| `GET /checklist-runs/{run_id}` | Reopen the saved answers, revision, usage and outstanding gaps. |

For example, the answer to a pressure-test question can separate the recommendation from the result that is missing in the reviewed file. The PDF fields below come from the worked example. The local CLI returns a bundle-relative link. The proposed service can expose the same citation through its revision-scoped route.

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
  "gap": "A completed test report or measurements."
}
```

Distinguish an answer supported by the evidence (`answered`), a partial answer (`partial`), conflicting accounts (`conflicting_evidence`), a completed search that found no requested evidence (`not_found`), and a search interrupted before the relevant sources were checked (`incomplete_search`). Keep the original question text, evidence and gap with each row. Record the run’s stop reason and resource use once for the whole run. [Worked answer](../approach/agent-retrieval.md#a-recommendation-and-a-missing-result)

In a rendered answer the source title, page and quoted wording use the returned link. [Engineering report, p. 3 — “I recommend a pressure test of the supply pipe and connection…”](../examples/water-damage/evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3)
