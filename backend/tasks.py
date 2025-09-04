# backend/tasks.py
from core import recon, admin_finder, graphql_finder, info_exposure, idor_scanner, forbidden_bypass
from core.report import save_burp_json
from datetime import datetime
import asyncio
import os

RESULTS_DIR = os.path.join("results")
os.makedirs(RESULTS_DIR, exist_ok=True)

async def run_modules(target):
    tasks = [
        recon.run_async_recon(target),
        asyncio.to_thread(admin_finder.find_admin_pages, target),
        asyncio.to_thread(graphql_finder.scan_graphql, target),
        asyncio.to_thread(info_exposure.scan_info_exposure, target),
        asyncio.to_thread(idor_scanner.scan_idor, target),
        forbidden_bypass.check_forbidden_bypass(target)
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)  # ✅ now it's awaited



def run_full_scan(target):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(run_modules(target))  # ✅ now results are real data

    # Flatten results into a single list of dicts
    flat_results = []
    for r in results:
        if isinstance(r, list):
            flat_results.extend(r)
        elif isinstance(r, dict):
            flat_results.append(r)

    save_burp_json(flat_results, target)  # ✅ safe for .get()