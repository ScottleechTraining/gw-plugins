# S&C Master Resource notebooks: the set rule

Scott's ruling, 2026-11-10: the S&C Master Resource is a numbered SET of NotebookLM notebooks
(Master 1, Master 2, Master 3, ...). Every read pulls from all of them. Every write goes to the
newest one with room. This replaces the retired "no overflow notebook" rule from 2026-10-12.

Every command that reads or grows the S&C Master Resource follows this file. Do not pin a master
notebook id in a command.

## 1. Resolve the set (one call)

Call `mcp__notebooklm__notebook_list` once. The **master set** is every notebook whose title starts
with `S&C Master Resource`. The number at the end of the title is the notebook number. A title with
no number is Master 1.

Known members on 2026-11-10 (the list call is the truth, this table is a sanity check):

| Number | Title | id |
|---|---|---|
| 1 | `S&C Master Resource` | `f4704629-7eab-4d23-ac95-7f8a2d9e826c` (full, 291 of 300, frozen) |
| 2 | `S&C Master Resource 2` | `25a1ad61-2bd9-40d1-91eb-575d8debddac` |

`S&C Health and Recovery`, `PDF S&C Archive` and topic notebooks are NOT in the set.

## 2. Read: query every master

Take the ids of every master with `source_count` above 0 (an empty notebook returns an error).

- One master with sources: `mcp__notebooklm__notebook_query` on that id.
- Two or more: `mcp__notebooklm__cross_notebook_query` with `notebook_names` = those ids joined by
  commas. Never use `all=true` (the account holds 370+ notebooks).
- The cross query returns one answer per notebook. It does not merge them. Build the result from all
  of the answers, and name the notebook title next to each citation.
- If the cross query tool fails, run `notebook_query` on each master in turn. A failure on one master
  does not block the run when another master answered; name the failed master in the output.

## 3. Write: add to the newest master with room

- The **write target** is the highest-numbered master with `source_count` below 290.
- If no master is below 290, create the next one: `mcp__notebooklm__notebook_create` with title
  `S&C Master Resource <N+1>`. Print one line for the digest:
  `NEW MASTER NOTEBOOK: S&C Master Resource <N+1> created`. This is the only case where a run
  creates a master notebook, and it creates at most one per run.
- If `source_add` fails with a source-limit error before 290, treat that master as full and apply
  the same roll-over.
- Dedup against the source list of EVERY master (`notebook_get` on each) before an add. A source
  already in any master does not count as new.
- Never add to a master that is not the write target. Never move or delete sources to rebalance.
