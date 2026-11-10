# How to test Documents2Wiki

The first trial asks two questions. Can a handler understand a claim and check its evidence more easily? Does access to the wiki help an agent answer from the same originals? This notebook contains a worked example and proposed tests. Measurements are still open.

## Review with a handler

Give a handler an unfamiliar file. Ask them to explain the current position, name the most important unresolved issue, and open the page that supports their account. Record the time, any source they cannot find, and any phrase that gives a stronger impression than the original. Ask which issue or term they would look for first on a real claim. For a comparison, use comparable fresh claims and alternate which one the handler sees with a wiki, to avoid rewarding familiarity with a file they just read.

## Compare retrieval with and without a wiki

Use the same revision, manifest, original pages, questions, model, retrieval tools and time or token budget. Start each run in a fresh session. In one condition the agent can search and open the originals. In the other it can also open the wiki index, entries and summaries. Withhold the walkthrough, expected answers and later documents from both. For `r3` allow only source versions `D-01-v1`, `D-02-v1` and `D-03-v1`. [Worked claim and source list](../examples/water-damage/README.md)

| Trial question | What to check against the source |
| --- | --- |
| When did Contractor A replace the coupling? | 5 May is the work date. 9 May is the receipt date. [Work order, p. 1](../examples/water-damage/sources/D-02-v1.md#pdf-page-1) · [Receipt record](../examples/water-damage/sources/D-02-v1.md#file-record) |
| Who signed for completion, and when? | The customer signed that afternoon. The work-order summary omits that detail, so the agent must consult the original. [Work order, p. 1](../examples/water-damage/sources/D-02-v1.md#pdf-page-1) |
| What does the file establish about the cause and the pressure test? | Attribute both possible causes. Report the recommendation and the missing result at `r3`. [Loss notice, p. 1](../examples/water-damage/sources/D-01-v1.md#pdf-page-1) · [Engineer’s opinion, p. 3](../examples/water-damage/evidence/D-03-v1/read/citations/p3-507-163-86217db25bf5.pdf#page=3) · [Test recommendation, p. 3](../examples/water-damage/evidence/D-03-v1/read/citations/p3-686-133-86217db25bf5.pdf#page=3) |
| What date did the engineer give for the inspection? | Ask at each revision. `r3` supports 12 May. After adding the signed correction, `r4` supports 13 May and explains the earlier record. [Report, p. 2](../examples/water-damage/evidence/D-03-v1/read/citations/p2-286-98-86217db25bf5.pdf#page=2) · [Addendum, p. 1](../examples/water-damage/sources/D-04-v1.md#pdf-page-1) |

For each answer record **correctness**, **whether the link opens the right version, page and source words, and whether those words support the answer**, and **whether the agent identified gaps or overstated certainty**. Record source pages opened, elapsed time and tokens alongside quality. Track the cost of building and updating the wiki separately so repeated questions can be compared fairly.

## Check the writer and broaden the trial

On the first build, compare the four pages with the source set for material omissions. Add the correction and check that there is one amended inspection entry, a summary of the addendum and a working citation. Reopen the earlier revision and repeat the question. Then try a second claim with different issues, such as a machinery loss involving both repair costs and interrupted production. Use handler feedback to decide whether the common pages need to change.

Two studies informed these checks. FRUIT evaluates whether new evidence supports an edit to an existing article. WikiBench examines which facts a generated codebase wiki covers or misses. [FRUIT](https://aclanthology.org/2022.naacl-main.269/) · [WikiBench](https://www.langchain.com/blog/evaluating-openwiki-with-wikibench)
