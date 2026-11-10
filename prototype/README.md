# Documents2Wiki prototype

The prototype requests a searchable PDF from Azure Document Intelligence Read, sends that PDF to a writer for a cited source summary, and creates links to highlighted passages. The worked claim includes a prepared example you can inspect offline. [Setup and commands](pdf-citations.md) · [Python implementation](pdf_evidence.py)

For the reasoning behind extraction, wiki updates and citations, start with the [ingestion workflow](../approach/ingestion.md).

## Proposed application

A small Python application could accept a document, start the writer, and publish the revision. A handler could then ask a question against that revision in a browser. The current design uses FastAPI for the HTTP interface and Microsoft Agent Framework with a Foundry deployment for the agent. [Proposed HTTP operations](http-api.md) · [Claim files and example payloads](data-and-citations.md) · [Foundry model provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/microsoft-foundry)

The first trial asks whether handlers can verify a finding and whether the wiki helps an agent find the right source. It can also surface search misses and formats that need a more precise locator, such as a spreadsheet cell. [Trial design](../approach/evaluation.md)

The earlier handover design is available as a historical snapshot. [Previous design](previous-handover-design.zip)
