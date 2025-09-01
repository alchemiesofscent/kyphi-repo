#!/usr/bin/env python3
"""
Merge a diff.json (GPT output) into the canonical data/MASTER.json.

Usage:
    python scripts/merge_diff.py data/MASTER.json diffs/my_diff.json [added_by]

- Assigns new IDs for recipes, ingredients, aliases, and entries.
- Deduplicates existing recipes/ingredients by slug.
- Deduplicates aliases by (ingredient_id + variant_label).
- Deduplicates entries by (recipe_id, ingredient_id, amount_raw, preparation).
- Stamps new entries with added_at + added_by.
"""

import json, sys, datetime

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def idx_by(arr, key):
    return {x[key]: x for x in arr}

def next_id(arr, key):
    return (max([x.get(key,0) for x in arr]) + 1) if arr else 1

def merge(master_path, diff_path, added_by="gpt"):
    master = load(master_path)
    diff = load(diff_path)

    recipes_by_slug = idx_by(master["recipes"], "slug")
    ingredients_by_slug = idx_by(master["ingredients"], "slug")

    # 1) Recipes
    for r in diff.get("recipes", []):
        if r["slug"] not in recipes_by_slug:
            new = {"recipe_id": next_id(master["recipes"], "recipe_id"), **r}
            master["recipes"].append(new)
            recipes_by_slug[new["slug"]] = new

    # 2) Ingredients
    for ing in diff.get("ingredients", []):
        slug = ing["slug"]
        if slug in ingredients_by_slug:
            # warn if label differs
            if ingredients_by_slug[slug]["label"] != ing["label"]:
                print(f"WARNING: slug collision for '{slug}' "
                      f"(existing='{ingredients_by_slug[slug]['label']}', new='{ing['label']}')")
            continue
        new = {"ingredient_id": next_id(master["ingredients"], "ingredient_id"), **ing}
        master["ingredients"].append(new)
        ingredients_by_slug[new["slug"]] = new

    # 3) Aliases
    seen_alias = {(a["ingredient_id"], a["variant_label"]) for a in master.get("aliases", [])}
    for a in diff.get("aliases", []):
        ing = ingredients_by_slug.get(a["ingredient_slug"])
        if not ing:
            print(f"WARNING: alias references unknown ingredient_slug={a['ingredient_slug']}")
            continue
        key = (ing["ingredient_id"], a["variant_label"])
        if key in seen_alias: 
            continue
        master["aliases"].append({
            "alias_id": next_id(master["aliases"], "alias_id"),
            "ingredient_id": ing["ingredient_id"],
            "variant_label": a["variant_label"],
            "language": a.get("language"),
            "source": a.get("source")
        })
        seen_alias.add(key)

    # 4) Entries
    seen_entry = {
        (e["recipe_id"], e["ingredient_id"], e.get("amount_raw",""), e.get("preparation","") or "")
        for e in master.get("entries", [])
    }
    for e in diff.get("entries", []):
        r = recipes_by_slug.get(e["recipe_slug"])
        i = ingredients_by_slug.get(e["ingredient_slug"])
        if not r or not i:
            print(f"WARNING: entry references unknown slug(s): "
                  f"recipe={e['recipe_slug']} ingredient={e['ingredient_slug']}")
            continue
        tup = (r["recipe_id"], i["ingredient_id"], e.get("amount_raw",""), e.get("preparation","") or "")
        if tup in seen_entry:
            continue
        master["entries"].append({
            "entry_id": next_id(master["entries"], "entry_id"),
            "recipe_id": r["recipe_id"],
            "ingredient_id": i["ingredient_id"],
            "amount_raw": e.get("amount_raw"),
            "amount_value": e.get("amount_value"),
            "amount_unit": e.get("amount_unit"),
            "preparation": e.get("preparation"),
            "notes": e.get("notes"),
            "source_citation": e.get("source_citation"),
            "source_span": e.get("source_span"),
            "added_at": datetime.datetime.utcnow().isoformat(),
            "added_by": added_by
        })
        seen_entry.add(tup)

    save(master_path, master)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: merge_diff.py data/MASTER.json diffs/your_diff.json [added_by]")
        sys.exit(1)
    merge(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "gpt")
