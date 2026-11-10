# What belongs in a claim wiki

The handler’s first question is usually “Where does this file stand?” The overview should answer it in a few paragraphs. Someone investigating a particular figure, event or opinion should be able to follow it to the document and page where it was recorded. The same structure can serve an industrial equipment loss, a cargo shortage or a liability claim.

## Pages a handler can open

| Page | What belongs there |
| --- | --- |
| **File overview** | Identify the reported loss, key parties and their roles, the latest material development, and the most important open question. List the documents on file with receipt dates and links to their summaries. |
| **Chronology** | Put events in the order they happened. Label approximate and disputed dates. Keep receipt dates in the inventory so a late report doesn’t move an earlier event. |
| **Issues and evidence** | Use a heading for each live question. Relevant topics might include cause, policy wording, liability, loss amount or recovery from another party. Attribute positions and show what evidence supports each one. |
| **Open actions** | Record what was requested or recommended, by whom, and what outcome is on file. Include an owner or due date when the file supplies one. Distinguish an outstanding request from a suggested follow-up. |

Use topics that the particular claim raises. On an equipment failure, a service report may establish repair dates while interrupted production remains disputed. On a cargo claim, the packing list and survey may give different quantities. Put those figures side by side with their sources. For amounts, keep the original currency and identify whether the figure is an estimate, an invoice, a reserve or a payment.

## Folder for one published revision

```text
wiki/
  index.md             links to claim pages and document summaries
  file-overview.md
  chronology.md
  issues.md
  action-plan.md
  documents/
    D-01-v1.md         cited summary of one source version
```

A revision is the state of one claim after a set of documents has been processed. Each document summary records the source title, author or role when known, receipt metadata and terms a handler may search for. A material statement links to the source version that supports it. For PDFs, the handler can open the supporting words highlighted on the same searchable pages the writer read. [How PDF citations work](ingestion.md#what-a-pdf-citation-opens) · [Example index](../examples/water-damage/wiki/index.md) · [Cited document summary](../examples/water-damage/wiki/documents/D-03-v1.md)
