# Documents2Wiki

Documents2Wiki is designed to turn one combined claim-file PDF into a wiki and a subrogation report. The wiki explains where the claim stands. The report answers a replaceable set of recovery questions and links each finding to its evidence. [MVP implementation plan](approach/implementation-plan.md)

## MVP workflow

1. **Find the documents in the claim PDF.** Intake detects where each record begins and ends. A loss notice, a work order and a multipage engineering report each get their own inventory entry linked to the physical pages of the upload. [Ingestion design](approach/ingestion.md)
2. **Create the wiki.** The writer agent publishes the overview, chronology, issues, open actions and cited document summaries automatically. Where two sources disagree, it records both accounts and identifies the point of conflict. [Writer instructions](prompts/purpose.md)
3. **Generate the subrogation report.** A research agent uses the published wiki, searches the claim documents and opens source pages to answer each question in order. The report shows the answers, supporting passages, gaps and documents the agent reviewed, reviewed in part or left unread. The starter questions are provisional and can be replaced by subrogation experts. [Starter questions](presets/subrogation-starter.json) · [Report and review coverage](approach/agent-retrieval.md#what-the-report-shows)

## Read a handover

**Did anyone pressure-test the pipe?** In the fictional water-damage claim, the engineer recommended a test. Open the action and follow its footnote to the engineer’s words on page 3. The file overview lists the three records reviewed at the 18 May handover. None contains a test result. You can read this hand-authored example without setup. [Open action](examples/water-damage/wiki/action-plan.md) · [Documents on file](examples/water-damage/wiki/file-overview.md#documents-received)

## Run the prototype

The prototype processes **one PDF at a time**. With the supplied sample, you can generate a passage link offline. With Azure credentials, you can turn a scan into a searchable PDF with Document Intelligence Read and send it to a model for a cited document summary. [Offline citation example](prototype/pdf-citations.md#cite-a-passage) · [Live PDF workflow](prototype/pdf-citations.md#prepare-a-document-version)

## Explore the design

A **revision** captures the documents and wiki pages available at a point in time. Each report uses one revision, so a reader can see which records were available when the agent answered.

| Reader question | Start here |
| --- | --- |
| What goes on each wiki page, and how should it describe disputed facts? | [Claim pages and dimensions](approach/claim-wiki.md) · [Writer instructions](prompts/purpose.md) |
| What changes when a correction arrives? | [Worked example before and after the addendum](examples/water-damage/README.md#a-correction-arrives) · [Update workflow](approach/ingestion.md#updating-the-claim-wiki) |
| How would we tell whether the wiki helps handlers and agents? | [Trial design and scoring](approach/evaluation.md) |
| How would a claims platform integrate this? | [Proposed HTTP operations](prototype/http-api.md) · [Storage and citations](prototype/data-and-citations.md) |
