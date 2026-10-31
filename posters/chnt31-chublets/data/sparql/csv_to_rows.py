"""Print the rows of a Wikidata CSV result as YAML lines for the poster table (standard library only).

Usage: python csv_to_rows.py wikidata-chublets-result.csv
Columns used: itemLabel, repository, licenceLabel. Several licences of one item are joined with ", ".
"""
import csv
import sys


def main(path):
    items = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = row.get("itemLabel", "")
            entry = items.setdefault(key, {"repository": "", "licences": []})
            repo = row.get("repository", "")
            if repo and not entry["repository"]:
                entry["repository"] = repo.replace("https://", "").replace("http://", "")
            lic = row.get("licenceLabel", "")
            if lic and lic not in entry["licences"]:
                entry["licences"].append(lic)
    for label in sorted(items):
        e = items[label]
        cells = [label, e["repository"] or "-", ", ".join(e["licences"]) or "-"]
        print("          - [" + ", ".join('"' + c.replace('"', "'") + '"' for c in cells) + "]")
    print("# %d rows" % len(items), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
