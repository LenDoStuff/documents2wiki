# Documents2Wiki

This notebook records the design for turning one insurance claim file into a wiki. On an industrial equipment claim, a handler could see what failed, what the engineer concluded and what still needs attention. A research agent can use the same wiki to find and verify evidence in the file.

When a claim PDF arrives, Azure Document Intelligence **Read** returns a PDF with selectable text. The writer reads that PDF and cites the words that support each change. A handler can open the same passage highlighted from a wiki entry or a research answer. [Ingestion workflow](approach/ingestion.md)

**Try it on the worked claim.** The engineer recommended a pressure test. The wiki lists the result as outstanding. Follow the citation to page 3 to check exactly what the engineer said. [Open action](examples/water-damage/wiki/action-plan.md) · [Highlighted recommendation](examples/water-damage/evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3)

| Folder | What you’ll find |
| --- | --- |
| `approach/` | The design. After ingestion, read about the [claim pages](approach/claim-wiki.md), [agent retrieval](approach/agent-retrieval.md), or the [proposed trial](approach/evaluation.md). |
| `prompts/` | Instructions for the agent that creates and updates the wiki. [Writing prompt](prompts/purpose.md) |
| `examples/` | A fictional claim with original wording, wiki pages and a later correction. [Worked claim](examples/water-damage/README.md) |
| `prototype/` | Commands to prepare a PDF, draft its cited summary and open a highlighted passage. [Prototype guide](prototype/README.md) |

The prototype can process one PDF. Automatic intake, publication of a complete claim wiki and checklist research are still proposed.
