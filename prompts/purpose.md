# Claim wiki creation prompt

Maintain one wiki for the insurance claim supplied. Write for a handler opening the file and an agent trying to locate evidence. Make it easy to see what happened, who said what, what changed and what still needs attention.

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

Read the source page before adding or changing a factual statement. For a PDF, read the attached searchable PDF prepared by Azure Document Intelligence Read. Give the document version, physical page (first sheet is 1) and the exact supporting words. Check the wording against the visible page and retain the author’s qualifications. Prefer a quote unique on that page. If wording repeats, use the word offset from the saved Read result to identify the occurrence. The publisher uses that result to link to the highlighted passage. For a visual observation with no quotable words, identify the page and label it **Page only**.

For other formats use their native source locator. For an explicit correction, amend the claim entry and cite both the correction and the earlier record. Keep each source summary faithful to its own version. When accounts disagree, cite each account. Mark missing or unreadable evidence as a gap. Leave claim decisions to the handler.
