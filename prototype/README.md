# Documents2Wiki prototype

The prototype requests a searchable PDF from Azure Document Intelligence Read, sends that PDF to a writer for a cited source summary, and creates links to highlighted passages. The worked claim includes a prepared example you can inspect offline. [Setup and commands](pdf-citations.md) · [Python implementation](pdf_evidence.py)

For the reasoning behind extraction, wiki updates and citations, start with the [ingestion workflow](../approach/ingestion.md).

## Proposed application

A small Python application would split a combined claim-file PDF into logical documents, publish the agent-written wiki, then run the subrogation questions against that revision. The resulting report would include cited answers and a record of the documents and pages the research agent checked. The design uses FastAPI for the HTTP interface and Microsoft Agent Framework with a Foundry deployment for the agent. [MVP implementation plan](../approach/implementation-plan.md) · [Proposed HTTP operations](http-api.md) · [Claim files and example payloads](data-and-citations.md) · [Foundry model provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/microsoft-foundry)

The proposed trial asks whether handlers can verify a finding and whether the wiki helps an agent find the right PDF passage. [Trial design](../approach/evaluation.md)

The earlier handover design is available as a historical snapshot. [Previous design](previous-handover-design.zip)
