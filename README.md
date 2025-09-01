# Kyphi Recipe Aligner

Turn this into a shareable mini app + durable data workflow.

## Repo layout

docs/ # static site for GitHub Pages
index.html # the aligner app
kyphi_long.json # auto-built long-format data for the app
data/
MASTER.json # source of truth (IDs + all entries)
schema_master.json # master schema
schema_diff.json # diff schema (what GPT outputs)
diffs/
(drop your diff files here and open a PR)
scripts/
merge_diff.py # merges diffs into MASTER.json
export_long.py # materializes docs/kyphi_long.json from MASTER.json
.github/workflows/
ci.yml # validates diffs, merges on PR, rebuilds docs/kyphi_long.json


## Workflow
1. **Never** edit `data/MASTER.json` by hand.
2. For each ingestion, ask GPT to output a **diff** that validates `data/schema_diff.json`.
3. Save the diff as `diffs/2025-09-01-rufus.json` and open a Pull Request.
4. CI will:
   - validate the diff against the schema,
   - dry-run the merge,
   - on merge to `main`, apply the merge, bump `data/MASTER.json` and rebuild `docs/kyphi_long.json`.
5. The site is served from `docs/` via GitHub Pages.

## Local development

python3 scripts/merge_diff.py data/MASTER.json diffs/example_diff.json
python3 scripts/export_long.py data/MASTER.json docs/kyphi_long.json


Set Pages source to **main /docs** in repo settings.