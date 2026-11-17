# What belongs in a claim wiki

At handover, a handler needs a short account of where the claim stands. When a date, an amount or an opinion matters to a decision, they also need the source. Each revision has four claim pages and a cited summary for each document version. The index links them together. [Worked claim index](../examples/water-damage/wiki/index.md)

## Pages a handler can open

| Handler’s question | What the page contains | Worked page |
| --- | --- | --- |
| Where does the file stand? | Reported loss, parties and roles, latest development, main open question and inventory of documents received. | [File overview](../examples/water-damage/wiki/file-overview.md) |
| What happened, and in what order? | Events in date order, with approximate or disputed dates labelled. | [Chronology](../examples/water-damage/wiki/chronology.md) |
| What does the evidence say about a live question? | A heading for each issue the file raises, such as cause, coverage, liability, loss amount or recovery. Each account has a source. | [Issues and evidence](../examples/water-damage/wiki/issues.md) |
| What needs follow-up? | Requests, recommendations and documented outcomes, with owners and due dates where supplied. | [Open actions](../examples/water-damage/wiki/action-plan.md) |

## Dimensions that give a claim entry its meaning

Use the dimensions that matter to the issue on file. A repair bill raises different questions from a witness account.

| Dimension | What to preserve | Example |
| --- | --- | --- |
| Time | When the event happened and when the record arrived. | Contractor A replaced the coupling on 5 May. The handler received the work order on 9 May. [Work order and receipt](../examples/water-damage/sources/D-02-v1.md) |
| Attribution and certainty | Who observed, suspected or concluded what, including qualifications. | The insured suspected roof entry. The engineer described a coupling leak as one possible explanation. [Accounts and sources](../examples/water-damage/wiki/issues.md) |
| Action status | What someone recommended, what was done and what result is on file. State which records were checked when reporting a gap. | The engineer recommended a pressure test. The three documents at the 18 May handover contain no result. [Open action](../examples/water-damage/wiki/action-plan.md) |
| Revision | What the handler could establish from the records available at that handover. | The report gave 12 May as the inspection date. A later signed addendum corrected it to 13 May. The proposed edit cites both records. [Worked correction](../examples/water-damage/README.md#a-correction-arrives) |
| Amount and basis | What a figure measures, its currency or unit, and who supplied it. | On a repair claim, label an estimate, an invoice and a payment separately. On a cargo claim, show any differing quantities from the packing list and survey with their sources. |

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

Each document summary records the source title, author or role when known, receipt metadata and terms a handler may search for. It preserves what that version said even after another document corrects the claim chronology. For PDFs, a passage citation opens the supporting words highlighted on the searchable page when their position can be verified. [Cited engineering report summary](../examples/water-damage/wiki/documents/D-03-v1.md) · [PDF citation behavior](ingestion.md#what-a-pdf-citation-opens)
