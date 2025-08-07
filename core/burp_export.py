import json
import os

def export_burp_json(findings, filepath):
    burp_items = []
    for f in findings:
        burp_items.append({
            "host": f.get("url", "").split("/")[2],
            "url": f.get("url"),
            "type": f.get("type"),
            "subtype": f.get("subtype", ""),
            "match": f.get("match", ""),
            "status": f.get("status", ""),
            "header": f.get("header", {})
        })
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as fp:
        json.dump(burp_items, fp, indent=2)
