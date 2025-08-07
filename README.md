# CyberAI 🔍🤖

**CyberAI** is an autonomous offensive security tool inspired by [xBow](https://xbow.com), designed to perform automated recon, vulnerability scanning, and basic exploitation. Built by [Ridwan Adebayo](https://github.com/yourusername), this tool assists pentesters and bug bounty hunters by identifying common web vulnerabilities with machine efficiency.

---

## ✨ Features

- 🔎 **Subdomain & URL Enumeration** (via Subfinder + GAU)
- 🧪 **Reflected XSS Detection**
- 🔐 **IDOR Scanning** (parameter fuzzing for access control bypass)
- 🔍 **Sensitive Info Exposure** (detect API keys, JWTs, AWS tokens, etc.)
- 🧬 **GraphQL Endpoint Detection & Introspection Probe**
- 🧾 **Auto-Generated Markdown Reports**

---

## 🚀 Usage

### ✅ Requirements

- Python 3.8+
- Go-based tools:
  - [`subfinder`](https://github.com/projectdiscovery/subfinder)
  - [`gau`](https://github.com/lc/gau)

### 📦 Installation

```bash
git clone https://github.com/RadoGold57/CyberAI.git
cd CyberAI
pip install -r requirements.txt
