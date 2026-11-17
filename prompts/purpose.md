# Claim wiki creation prompt

Maintain one wiki for the insurance claim supplied. Write for a handler opening the file and for the research agent answering the preset report questions. Use the claim inventory’s logical documents and version IDs. Make it easy to see what happened, who said what, what changed and what still needs attention.

```text
wiki/
  index.md
  file-overview.md
  chronology.md
  issues.md
  action-plan.md
  documents/<document-version-id>.md
```

Link the four claim pages and one cited summary per source version from the index. Use the names, roles, document titles and technical terms found in the file.

- **File overview.** Summarize the reported loss, key parties, current position and open questions. List each document with its receipt date when supplied and a link to its summary.
- **Chronology.** Order events by when they happened. Label approximate, unknown or disputed dates.
- **Issues and evidence.** Give each live question a descriptive heading. Attribute observations, opinions and decisions. Preserve qualifications, conflicting accounts, currencies and the basis of each amount.
- **Open actions.** Record requests, recommendations and documented outcomes. Include owners and due dates where the file identifies them.

On the first build, account for the documents already on file and their material facts. When a document arrives, summarize the new version, list it once and amend each entry its evidence changes. A routine receipt may need only its summary and inventory links.

Read the source page before adding or changing a factual statement. For a PDF, read the attached searchable pages prepared by Azure Document Intelligence Read. Give the logical document version, physical page of the original upload (first sheet is 1) and the exact supporting words. When reading an excerpt, use its supplied page mapping. Check the wording against the visible page and retain the author’s qualifications. Prefer a quote unique on that page. If wording repeats, use the word offset from the saved Read result to identify the occurrence. The publisher uses that result to link to the highlighted passage. For a visual observation with no quotable words, identify the page and label it **Page only**.

### When accounts differ

- **Conflicting accounts.** When sources make incompatible statements about the same fact, write **Conflicting accounts**, name the disputed fact, attribute each account and cite each passage. Keep both visible in the claim entry. A later receipt date alone gives neither account precedence.
- **Possible explanations.** Preserve the author’s degree of certainty. If two people suggest different possible causes and the file establishes neither, describe both possibilities and leave the cause open.
- **Explicit source correction.** When a source expressly corrects an earlier statement, amend the affected claim entry. Name the earlier statement, identify who corrected it and cite both passages. For an inspection date, keep one inspection in the chronology. Each document summary continues to describe what its own version said.

Mark missing or unreadable evidence as a gap. Leave claim decisions to the handler.
