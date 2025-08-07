import asyncio
import json
import os
from backend.pipeline import run_scan

def run_scan_task(target, ai_payloads, concurrency, job_id):
    results = asyncio.run(run_scan(target, ai_payloads, concurrency))
    os.makedirs("results", exist_ok=True)
    with open(f"results/{job_id}.json", "w") as f:
        json.dump(results, f, indent=2)
    return True
