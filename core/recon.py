import subprocess

def run_subfinder(domain):
    result = subprocess.run(["subfinder", "-d", domain, "-silent"], capture_output=True, text=True)
    return list(set(result.stdout.strip().splitlines()))

def run_gau(domain):
    result = subprocess.run(["gau", domain], capture_output=True, text=True)
    return list(set(result.stdout.strip().splitlines()))

def fetch_urls(domain):
    print(f"[+] Running subfinder on {domain}")
    subs = run_subfinder(domain)

    print(f"[+] Running gau on {domain} and discovered subdomains")
    all_urls = set()
    for sub in subs + [domain]:
        urls = run_gau(sub)
        all_urls.update(urls)
    return list(all_urls)
