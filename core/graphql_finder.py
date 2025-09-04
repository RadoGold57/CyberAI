# core/graphql_finder.py
import httpx

COMMON_GRAPHQL_PATHS = [
    "/graphql",
    "/api/graphql",
    "/graphiql",
    "/graphql/console"
]

async def scan_graphql(base_url):
    findings = []
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    async with httpx.AsyncClient(follow_redirects=True, timeout=8) as client:
        for path in COMMON_GRAPHQL_PATHS:
            url = base_url.rstrip("/") + path
            try:
                r = await client.post(url, json={"query": "{ __typename }"})
                if r.status_code == 200 and "data" in r.text:
                    findings.append({
                        "type": "GraphQL Endpoint",
                        "url": url,
                        "status": r.status_code,
                        "response": r.text[:200]  # limit preview
                    })
                elif r.status_code in [200, 400] and "errors" in r.text.lower():
                    findings.append({
                        "type": "GraphQL Endpoint (error)",
                        "url": url,
                        "status": r.status_code
                    })
            except Exception:
                pass
    return findings
