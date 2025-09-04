import asyncio
from core.crawler_async import async_crawl
from core.idor_scanner import scan_idor
from core.info_exposure import scan_info_exposure
from core.graphql_finder import find_graphql
from core.admin_finder import find_admin_panels
from core.forbidden_bypass import check_403_bypass
from core.burp_export import export_burp_json

async def run_scan(target, ai_payloads=False, concurrency=30):
    findings = []
    urls = await async_crawl(target, max_pages=500, concurrency=concurrency)

    findings += scan_idor(urls)
    findings += scan_info_exposure(urls)
    findings += find_graphql(urls)
    findings += find_admin_panels(target)
    findings += check_403_bypass(urls)

    export_burp_json(findings, f"results/{target}_burp.json")
    return findings
