from core.recon import fetch_urls
from core.scanner import test_xss
from core.idor import test_idor
from core.info_leak import scan_for_secrets
from core.graphql_finder import find_graphql
from core.report import write_markdown_report
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <target_domain>")
        return

    target = sys.argv[1]
    print(f"[+] Starting CyberAI on {target}")

    urls = fetch_urls(target)

    findings = []
    findings += test_xss(urls)
    findings += test_idor(urls)
    findings += scan_for_secrets(urls)
    findings += find_graphql(urls)

    write_markdown_report(findings, target)

if __name__ == "__main__":
    main()
