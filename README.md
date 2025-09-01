# Kyphi Recipe Aligner

A web-based tool for aligning and comparing ancient kyphi incense recipes across different sources, with a durable data workflow powered by GitHub.

## 🌐 **Live Demo**

Visit the app at: `https://[your-username].github.io/[repo-name]/`

## 📁 **Repository Structure**

```
├── docs/                          # Static site (GitHub Pages)
│   ├── index.html                # Main aligner app
│   └── kyphi_long.json           # Auto-generated data (don't edit)
├── data/
│   ├── MASTER.json               # Canonical database (don't edit by hand)
│   ├── schema_master.json        # Schema for MASTER.json
│   └── schema_diff.json          # Schema for diff files
├── diffs/                        # Drop diff files here for ingestion
│   └── example_2025-09-01.json   # Sample diff format
├── scripts/
│   ├── merge_diff.py             # Merges diffs into MASTER.json
│   └── export_long.py            # Exports MASTER to long format
└── .github/workflows/
    └── ci.yml                    # Validates, merges, and deploys
```

## 🔄 **Workflow**

1. **Never edit `data/MASTER.json` by hand** - it's managed by automation
2. Create new ingestion diffs that validate against `data/schema_diff.json`
3. Save diffs as `diffs/YYYY-MM-DD-source.json` and open a Pull Request
4. CI will validate the diff and show a dry-run preview
5. On merge to `main`, CI will:
   - Apply the merge to `data/MASTER.json`
   - Rebuild `docs/kyphi_long.json` 
   - Commit changes and deploy to GitHub Pages

## 🚀 **Setup Instructions**

### 1. Repository Setup
```bash
git clone https://github.com/[username]/[repo-name]
cd [repo-name]
```

### 2. Enable GitHub Pages
- Go to repo **Settings → Pages**
- Set source to **Deploy from branch**
- Choose **main** branch and **/ docs** folder
- Save and wait for deployment

### 3. Test Locally
```bash
# Test merge functionality
python3 scripts/merge_diff.py data/MASTER.json diffs/example_2025-09-01.json "test"

# Generate web app data
python3 scripts/export_long.py data/MASTER.json docs/kyphi_long.json

# Serve locally (Python 3)
cd docs && python3 -m http.server 8000
# Visit http://localhost:8000
```

## 📝 **Creating Diff Files**

Ask GPT to output data in this format (validates against `data/schema_diff.json`):

```json
{
  "recipes": [{"slug": "recipe_id", "label": "Recipe Name", "language": "en", "source": "Book"}],
  "ingredients": [{"slug": "ingredient_id", "label": "Ingredient Name", "language": "en"}],
  "aliases": [{"ingredient_slug": "ingredient_id", "variant_label": "Alternative Name"}],
  "entries": [{
    "recipe_slug": "recipe_id",
    "ingredient_slug": "ingredient_id", 
    "amount_raw": "2 cups",
    "amount_value": 2,
    "amount_unit": "cups",
    "preparation": "ground",
    "notes": "optional notes"
  }]
}
```

## 🛠 **Requirements**

- Python 3.7+
- `jsonschema` library for validation

## 🔍 **Features**

- **Smart deduplication**: Prevents duplicate recipes, ingredients, and entries
- **Stable IDs**: Assigns permanent numeric IDs to all entities
- **Provenance tracking**: Records when and how data was added
- **Unicode-aware**: Proper handling of ancient Greek, Arabic, etc.
- **Search & filter**: Find ingredients across recipes with live search
- **Export options**: CSV and JSON export of filtered data
- **Mobile-friendly**: Responsive design works on all devices

## 🤝 **Contributing**

1. Fork the repository
2. Create a new diff file in `diffs/` following the schema
3. Open a Pull Request
4. CI will validate and provide feedback
5. On approval, changes are automatically merged and deployed

## 📊 **Data Model**

The system normalizes recipe data into:
- **Recipes**: Named formulations (with sources)
- **Ingredients**: Canonical ingredient names
- **Aliases**: Alternative names for ingredients  
- **Entries**: Recipe-ingredient relationships with amounts/prep

All entities get stable numeric IDs for reliable cross-referencing.
