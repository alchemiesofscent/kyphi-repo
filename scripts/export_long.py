#!/usr/bin/env python3
import json, sys

def export(master_path, out_path):
    with open(master_path, "r", encoding="utf-8") as f:
        m = json.load(f)
    recipes = {r["recipe_id"]: r for r in m["recipes"]}
    ingredients = {i["ingredient_id"]: i for i in m["ingredients"]}
    rows = []
    for e in m["entries"]:
        rows.append({
            "recipe": recipes[e["recipe_id"]]["label"],
            "ingredient": ingredients[e["ingredient_id"]]["label"],
            "amount": e.get("amount_raw"),
            "preparation": e.get("preparation"),
            "notes": e.get("notes")
        })
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: export_long.py data/MASTER.json docs/kyphi_long.json")
        sys.exit(1)
    export(sys.argv[1], sys.argv[2])
