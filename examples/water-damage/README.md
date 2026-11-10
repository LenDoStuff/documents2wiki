# A worked claim from documents to wiki

Claim `C-1042` is a fictional water-damage file. The handler receives a loss notice, a contractor’s work order and an engineer’s report. A signed correction arrives later. The engineering report is available as a fictional scanned PDF and a numbered transcript. The other records are Markdown transcriptions. Receipt metadata is separate from source wording. [Original scan](sources/D-03-v1.pdf) · [Searchable reading copy](evidence/D-03-v1/read/searchable.pdf)

## Take over the file at r3

Open the wiki index and follow **File overview**. Revision `r3` is the handover on 18 May. It includes the first three records. The worked pages are a hand-authored example of the intended output. [Open the claim wiki](wiki/index.md)

| Question a handler might ask | What the available record supports |
| --- | --- |
| Who worked on the pipe? | Contractor A replaced the cold-water supply coupling on 5 May. [Signed work order, p. 1](sources/D-02-v1.md#pdf-page-1) |
| Did that work cause the damage? | The insured suspected roof entry. The engineer considered the coupling a possible source and left the cause unresolved. This is where a handler considering recovery would start. [Loss notice, p. 1](sources/D-01-v1.md#pdf-page-1) · [Engineering report, p. 3 — “one possible explanation”](evidence/D-03-v1/read/citations/p3-507-163-86217db25bf5.pdf#page=3) |
| What is still outstanding? | The engineer recommended a pressure test. The three documents reviewed at handover contain no result. [Open action](wiki/action-plan.md) · [Engineering report, p. 3 — “I recommend a pressure test of the supply pipe and connection to help distinguish this possibility from another route of water entry.”](evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3) |

## A correction arrives

On 21 May the engineer submits a signed addendum. The intended `r4` edit to the chronology reads **“13 May — Engineer’s site inspection. The signed addendum corrects the 12 May date in the original report.”** The inspection is one event with two supporting pages. The new version also gets a document summary and an inventory entry. The `r3` snapshot linked above preserves what the handler knew on 18 May. [Report, p. 2](evidence/D-03-v1/read/citations/p2-286-98-86217db25bf5.pdf#page=2) · [Addendum, p. 1](sources/D-04-v1.md#pdf-page-1)

To try the writer yourself, give it the creation prompt and the first three documents below. For the engineer’s report, attach the searchable PDF. Its embedded text and word positions were prepared locally to simulate the two outputs from Read. Add the fourth document after reviewing the first output. For retrieval tests, use the same source set in both runs and reserve this walkthrough for scoring. [Creation prompt](../../prompts/purpose.md) · [Run the PDF prototype](../../prototype/pdf-citations.md) · [Trial design](../../approach/evaluation.md)

| Source version | Received | Available from |
| --- | --- | --- |
| [D-01-v1 · Loss notice](sources/D-01-v1.md) | 8 May | `r1` |
| [D-02-v1 · Work order](sources/D-02-v1.md) | 9 May | `r2` |
| [D-03-v1 · Engineering report (PDF for the writer)](evidence/D-03-v1/read/searchable.pdf) | 18 May | `r3` |
| [D-04-v1 · Signed addendum](sources/D-04-v1.md) | 21 May | `r4` |

The current PDF example lives in `evidence/D-03-v1/read/`. The files beside that directory preserve citations issued by the earlier Layout prototype.

[Documents2Wiki notebook](../../README.md)
