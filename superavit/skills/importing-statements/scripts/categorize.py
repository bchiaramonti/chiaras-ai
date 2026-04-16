#!/usr/bin/env python3
"""
Superavit — Transaction Categorizer (keyword-based)

Matches transactions to categories using keyword lookup.
Unmatched transactions return category_id=null for Claude fallback.

Usage:
    python categorize.py <transactions_json_file> <categories_json_file>
    echo '<transactions_json>' | python categorize.py - <categories_json_file>

Input transactions JSON: [{"description": "IFOOD *REST", "amount": -45.90}, ...]
Input categories JSON: [{"id": "uuid", "name": "Alimentacao", "keywords": ["ifood", ...]}, ...]

Output: JSON array of matches to stdout.
"""

import json
import sys
from pathlib import Path


def load_json(source: str) -> list:
    """Load JSON from file path or stdin (if source is '-')."""
    if source == "-":
        return json.load(sys.stdin)
    path = Path(source)
    if not path.exists():
        print(json.dumps({"error": f"File not found: {source}"}), file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def categorize(transactions: list, categories: list) -> list:
    """Match transactions to categories by keyword lookup.

    For each transaction, checks if description.lower() contains any keyword
    from any category. First match wins (categories are checked in order).

    Returns a list of match results, one per transaction.
    """
    # Pre-process: build keyword → category mapping
    keyword_map = []
    for cat in categories:
        cat_id = cat.get("id")
        cat_name = cat.get("name", "")
        keywords = cat.get("keywords", [])
        # Handle keywords as JSON string or list
        if isinstance(keywords, str):
            try:
                keywords = json.loads(keywords)
            except (json.JSONDecodeError, TypeError):
                keywords = []
        for kw in keywords:
            if kw:  # Skip empty keywords
                keyword_map.append({
                    "keyword": kw.lower(),
                    "category_id": cat_id,
                    "category_name": cat_name,
                })

    results = []
    for idx, txn in enumerate(transactions):
        desc = txn.get("description", "").lower()
        matched = False

        for entry in keyword_map:
            if entry["keyword"] in desc:
                results.append({
                    "index": idx,
                    "category_id": entry["category_id"],
                    "category_name": entry["category_name"],
                    "matched_keyword": entry["keyword"],
                })
                matched = True
                break

        if not matched:
            results.append({
                "index": idx,
                "category_id": None,
                "category_name": None,
                "matched_keyword": None,
            })

    return results


def main():
    if len(sys.argv) < 3:
        print("Usage:", file=sys.stderr)
        print("  python categorize.py <transactions_json> <categories_json>", file=sys.stderr)
        print("  echo '<json>' | python categorize.py - <categories_json>", file=sys.stderr)
        sys.exit(1)

    transactions_source = sys.argv[1]
    categories_source = sys.argv[2]

    try:
        transactions = load_json(transactions_source)
        categories = load_json(categories_source)
        results = categorize(transactions, categories)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}", "type": "json_error"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "type": "unexpected_error"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
