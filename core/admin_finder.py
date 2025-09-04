import httpx
import asyncio

ADMIN_PATHS = [
    "/admin", "/administrator", "/internal", "/dashboard", "/manage", "/controlpanel"
]

async def find_admin_pages(base_url):
    findings = []
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    async with httpx.AsyncClient(follow_redirects=True, timeout=8) as client:
        tasks = []
        for path in ADMIN_PATHS:
            url = base_url.rstrip("/") + path
            tasks.append(check_url(client, url))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if res:
                findings.append(res)
    return findings

async def check_url(client, url):
    try:
        r = await client.get(url)
        if r.status_code in [200, 401, 403]:
            return {
                "type": "Admin Page",
                "url": url,
                "status": r.status_code
            }
    except:
        return None

