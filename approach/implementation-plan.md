# MVP implementation plan

Given one combined claim-file PDF, produce a cited claim wiki and a subrogation report for the same revision. Intake discovers the logical documents inside the upload. The wiki writer publishes automatically. The research agent uses the wiki and the source pages to answer the configured questions. The existing Python prototype already prepares a searchable PDF, drafts a single-source summary and resolves passage citations. [Current prototype](../prototype/README.md)

## 1. Segment the claim file

Store the original upload and reuse the Read extraction. Process the physical pages in order. Give the boundary detector page text and layout cues such as titles, senders, signatures and page numbering. Inspect the page image when the text leaves a boundary unclear. For large files, process bounded batches with overlapping context and reconcile decisions at the joins.

Write an inventory entry for each logical document with a version ID, title when known, source PDF identity and inclusive physical page range. Validate that every page from 1 through the last page is accounted for exactly once. Keep uncertain pages in an explicitly labelled range with the reason and make them searchable. A retry of the same submission should reuse the saved inventory and IDs. [Ingestion design](ingestion.md)

**First check.** Assemble a test packet from the fictional loss notice (p. 1), work order (p. 2) and three-page engineering report (pp. 3–5). Keep the expected ranges in the test fixture, hidden from the detector. Check that the engineer’s cover stays with the report and that the recommendation opens on physical page 5. Repeat with a batch boundary inside the report and with an unreadable separator. [Worked source records](../examples/water-damage/README.md)

## 2. Publish the wiki

Give the writer each logical document’s source pages and their original page numbers. Build one cited summary per document, then the overview, chronology, issues, open actions and index. Extend the current citation resolver to verify that the cited page belongs to that document in the revision. A document-local page number must resolve to the corresponding physical page before the link is saved. Publish the inventory and wiki together so readers can reopen a complete revision. [Writer instructions](../prompts/purpose.md) · [Revision storage](../prototype/data-and-citations.md)

**First check.** The work order establishes what Contractor A did on 5 May. The engineer identifies one possible cause and recommends a test. The wiki should preserve both qualifications. Add the signed correction in a subsequent revision and check that its inspection entry cites both dates and that the earlier handover still opens. For two incompatible independent accounts, check that the writer attributes both and labels the conflict.

## 3. Generate the subrogation report

Load the ordered question preset and record its ID, version and exact questions with the run. For each question, let the agent navigate the wiki, search the selected revision and open source pages. Save the answer, status, citations and gaps. Render the answers in preset order in a readable report. Keep the questions outside the writer and retrieval code so subrogation experts can replace them and rerun the report against the same wiki. [Starter questions](../presets/subrogation-starter.json)

Record tool activity as each question runs. Build the report’s **Documents reviewed** table from the full revision inventory and the pages the research agent actually opened. Include readable pages, unreadable pages and documents with no source reads. Keep question-level coverage so a page opened for one answer does not silently count toward another. [Report and coverage example](agent-retrieval.md#what-the-report-shows)

**First check.** On the fictional claim, the parties answer should cite the work order. The cause answer should attribute the engineer’s opinion and the insured’s alternative explanation. An answer about outstanding evidence should cite the test recommendation and scope any missing result to the records checked. Run a second preset against the same revision and confirm each saved report reopens with its own wording and coverage.

## 4. Connect intake to the two outputs

Wire the stages together behind the proposed claim operations. A completed submission produces a revision. Run the starter preset on that revision and expose links to the wiki, report and highlighted passages. Stage partial writes so a failed report can resume or rerun against the same published wiki. Keep run IDs separate from revision IDs so replacing the questions does not require another extraction. [HTTP operations](../prototype/http-api.md)

**End-to-end check.** Start from the combined test PDF with no supplied boundaries. Open the final report, follow a citation to the correct physical page of the original claim file’s searchable copy, and find an inventory entry the agent skipped or only partly reviewed in a controlled run. Inspecting those outputs demonstrates the workflow. Pilot scoring thresholds can be set later.
