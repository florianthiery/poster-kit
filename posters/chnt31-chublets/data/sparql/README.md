# SPARQL queries of poster chnt31-chublets

Since round 2 (2026-10-31) none of these queries is printed on the poster; the files and results stay as evidence for `brief.numbers.0` (416) and for later use.

| Query | File | Run against | Result file | Run on |
|---|---|---|---|---|
| Chublets by category | `categories.rq` | `dist/n4o-rse.github.io-chublets-wikibase-demo.ttl` of `n4o-rse/chublets-wikibase-demo` (commit 90a4e39a, data as of 2026-10-25), rdflib | `categories-result.csv` | 2026-10-31 |
| Number of chublets | `count.rq` | same file | `count-result.csv` | 2026-10-31 |
| Chublets on Wikidata | `wikidata-chublets.rq` | Wikidata Query Service | `wikidata-chublets-result.csv` (**not yet delivered**) | TODO |

The Wikidata query could not be run from the build sandbox (the proxy refuses `query.wikidata.org`). To run it:

1. Open https://query.wikidata.org/ and paste `wikidata-chublets.rq`.
2. Run it, then "Download", "CSV file", and save the file as `wikidata-chublets-result.csv` in this folder.
3. Note the date and time of the run in the table above.
4. `python csv_to_rows.py wikidata-chublets-result.csv` prints the table rows for `poster.yaml` (block `q_wikidata`).

The class `wd:Q141115627` (chublet) is taken from the Starter Pack of `chublets-wikibase-demo`, which checked it against
Wikidata on 2026-10-21; it has not been checked again from here.
