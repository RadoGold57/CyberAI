import httpx

def find_graphql(urls):
    print("[+] Checking for GraphQL endpoints...")
    findings = []
    checked = set()

    for url in urls:
        for endpoint in ["/graphql", "/api/graphql"]:
            if url.endswith(endpoint) or endpoint in url:
                try:
                    if url in checked:
                        continue
                    r = httpx.post(url, json={"query": "{__typename}"}, timeout=10)
                    if "data" in r.text or "__typename" in r.text:
                        findings.append({
                            "url": url,
                            "type": "GraphQL Introspection Enabled",
                            "payload": "{__typename}",
                            "evidence": "GraphQL response received"
                        })
                        checked.add(url)
                except Exception:
                    pass
    return findings
