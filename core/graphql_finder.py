import httpx

GRAPHQL_ENDPOINTS = [
    "/graphql", "/api/graphql", "/gql", "/graphiql"
]

def find_graphql(urls):
    findings = []
    roots = set()
    for u in urls:
        roots.add(u.split("/")[0] + "//" + u.split("/")[2])
    client = httpx.Client(follow_redirects=True, timeout=8)
    for root in roots:
        for endpoint in GRAPHQL_ENDPOINTS:
            target = root + endpoint
            try:
                r = client.post(target, json={"query": "{__typename}"})
                if r.status_code == 200 and "__typename" in r.text:
                    findings.append({
                        "type": "GraphQL Endpoint",
                        "url": target
                    })
            except:
                pass
    client.close()
    return findings
