# Run the PDF prototype

Run these commands from the project root. For a live claim, `prepare --draft` takes the original PDF through Read and sends the resulting PDF straight to the writer. The offline example below lets you inspect the PDF and its citations without either Azure service. [PDF ingestion workflow](../approach/ingestion.md#pdf-ingestion-workflow)

## Cite a passage

Install the dependencies, then generate a wiki link using the fictional engineering report. The example simulates a Read response using the report’s typeset words and a locally prepared searchable PDF.

```powershell
python -m pip install -r prototype/requirements.txt
python prototype/pdf_evidence.py cite examples/water-damage/evidence/D-03-v1/read --page 3 --quote "I recommend a pressure test of the supply pipe and connection to help distinguish this possibility from another route of water entry." --markdown --title "Engineering report" --relative-to examples/water-damage/wiki
```

For a saved answer, omit `--markdown` and set `--relative-to` to the directory containing the answer. The JSON includes the document version, extraction ID, page, exact quote, offset, length and link. If wording repeats, use `--offset` to select the occurrence. For a quotation spanning pages, cite each page separately. [Example answer](http-api.md) · [Citation behavior and page-only fallback](../approach/ingestion.md#what-a-pdf-citation-opens)

## Prepare a document version

For live extraction set `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` and `AZURE_DOCUMENT_INTELLIGENCE_KEY`, then supply the original PDF, an output directory and a version ID.

```powershell
python prototype/pdf_evidence.py prepare path/to/report.pdf path/to/evidence/D-03-v1/read --version D-03-v1
```

The command submits the original bytes to `prebuilt-read` with `output=pdf` and downloads the PDF from that analysis. It saves the returned bytes as `searchable.pdf` and the word positions and analysis identity in `read.json`. The printed `writer_input` is the path to the PDF. Running the command again for the same prepared version reuses it. [Azure Read and searchable PDFs](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-read?view=doc-intel-4.0.0#searchable-pdfs) · [Word offsets and coordinates](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/analyze-document-response?view=doc-intel-4.0.0)

To replay the example offline, pass its saved Read result and PDF together. The command checks that they belong to this original and version.

```powershell
python prototype/pdf_evidence.py prepare examples/water-damage/sources/D-03-v1.pdf .\demo-evidence --version D-03-v1 --from-bundle examples/water-damage/evidence/D-03-v1/read
```

## Draft a source summary from the PDF

Set `AZURE_OPENAI_ENDPOINT` to the Azure OpenAI resource URL (for example, `https://YOUR-RESOURCE.openai.azure.com`), `AZURE_OPENAI_API_KEY` to its key and `AZURE_OPENAI_DEPLOYMENT` to a deployment that accepts PDFs and supports JSON output. To prepare the PDF and draft its source summary in a single command, add `--draft`.

```powershell
python prototype/pdf_evidence.py prepare path/to/report.pdf path/to/evidence/D-03-v1/read --version D-03-v1 --draft
```

The writer sends the saved `searchable.pdf` as a file attachment with the claim wiki prompt. Azure’s PDF input gives the model the embedded text and an image of each page. The command prints a draft source summary as JSON, with each statement linked to its checked quote. Links are relative to the prepared directory. An unmatched or ambiguous quote stops the draft for review. To draft again from the same PDF, run `python prototype/pdf_evidence.py draft path/to/evidence/D-03-v1/read`. [Microsoft’s guide to PDF model input](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses#file-input)
