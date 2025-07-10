# Subdomain Enumeration Tool

A fast, multithreaded Python tool for discovering subdomains of a target domain, now enhanced to support **bulk scanning of popular domains** from the Tranco Top 1 Million list.

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/status-active-brightgreen)

---

## 🚀 Features

✅ Subdomain scanning using:
- Wordlists
- Historical data from the Wayback Machine
- Optional AI-driven predictions (OpenAI)

✅ Supports both HTTP and HTTPS scanning

✅ DNS resolution checks to avoid unnecessary requests

✅ Detects wildcard DNS to reduce false positives

✅ Reverse DNS lookups for discovered IPs

✅ SSL certificate SAN (Subject Alternative Names) enumeration

✅ Port scanning for popular ports (optional)

✅ Banner grabbing for open ports

✅ Response fingerprinting via SHA-256 hashes

✅ Colorized console output for better readability

✅ Progress bar for tracking scanning progress

✅ CSV and JSON result exports

✅ Bulk scanning for lists of domains (e.g. Tranco Top 1M)

---

## 🛠 Installation

Clone this repository:

```bash
git clone https://github.com/sanjai20/subdomain-enumeration-tool.git
cd subdomain-enumeration-tool
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you plan to use AI-driven predictions, also install OpenAI’s SDK:

```bash
pip install openai
```

---

## 📄 Single-Domain Usage

Run the tool on a single target domain:

```bash
python subdomain_enum.py example.com
```

Advanced usage:

```bash
python subdomain_enum.py example.com \
    -w subdomains.txt \
    -o results.csv \
    --json results.json \
    --https \
    --ports 22,80,443 \
    --openai YOUR_OPENAI_API_KEY
```

| Option                  | Description |
|--------------------------|-------------|
| `example.com`           | The target domain to scan |
| `-w subdomains.txt`     | Path to wordlist file |
| `-o results.csv`        | Output CSV file |
| `--json results.json`   | Optional JSON output file |
| `--https`               | Scan HTTPS endpoints |
| `--ports 22,80,443`     | Ports to scan on discovered subdomains |
| `--openai API_KEY`      | Use OpenAI to predict likely subdomains |

---

## 🔍 Example Output

Discovered subdomains will be saved in CSV and/or JSON formats, e.g.:

**CSV Example:**

| subdomain            | ip               | scheme | url                      | status | server_header     |
|----------------------|------------------|--------|--------------------------|--------|-------------------|
| www.example.com      | 93.184.216.34    | http   | http://www.example.com   | 200    | nginx/1.18.0      |

---

## 🗂 Bulk Scanning with Tranco List

You can scan multiple popular domains automatically using the included `bulk_scan.py` script.

### Prepare a Tranco List

Download the `top-1m.csv` from:
- [https://tranco-list.eu](https://tranco-list.eu)

Place it in your project directory as `top-1m.csv`.

---

### Run Bulk Scan

Scan the top N domains:

```bash
python bulk_scan.py
```

By default, it scans the top 10 domains. Edit `bulk_scan.py` to increase this limit.

Each scanned domain will produce:
```
bulk_results/example_com.csv
bulk_results/example_com.json
```

---

## ⚠️ Important Notes

- Scanning a large list like Tranco Top 1M can be resource-intensive.
- Respect the legal and ethical boundaries of scanning.
- Be mindful of rate limits and avoid aggressive scanning that could get your IP blocked.

---

## 💡 Upcoming Enhancements

Planned next steps:
- Integrate Shodan and Censys lookups
- Add SQLite or Postgres database storage
- Slack/Discord alerting
- Screenshots of discovered subdomains
- Multi-threaded or async bulk scanning
- Cloud provider detection (AWS, Azure, GCP)

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or pull request.

---

## 🙋‍♂️ Author

**Sanjai**  
[GitHub Profile](https://github.com/sanjai20)

---

## 📝 License

This project is licensed under the MIT License.
