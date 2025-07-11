# Subdomain Enumeration Tool

A Python-based subdomain discovery and reconnaissance tool designed for scanning single domains or performing bulk enumeration across the Tranco Top-1M domain list. Results are saved into a centralized SQLite database for powerful querying and analysis.

---

## ✨ Features

✅ Subdomain discovery:
- Wordlist-based enumeration
- Wayback Machine integrations

✅ HTTP/HTTPS probing:
- HTTP status codes
- Server headers
- Page titles
- Response lengths
- SSL certificate SANs

✅ Optional port scanning

✅ Wildcard domain detection

✅ Saves results to:
- CSV
- JSON
- SQLite database

✅ Bulk scanning support:
- Integrate large domain lists
- Parallel scanning

✅ Database-ready for analytics:
- Query scan results
- Export filtered data

---

## ⚙️ Requirements

- Python 3.x
- Install dependencies:

```bash
pip install requests tqdm colorama
```

---

## 🚀 How to Use

### Single Domain Scan

Run the tool on one domain:

```powershell
python subdomain_enum.py example.com --https --ports 80,443
```

- `--https` → scan both HTTP and HTTPS
- `--ports` → scan custom ports (comma-separated)

Example output:

```
[+] http://www.example.com (200)
[+] https://www.example.com (200)
Saved CSV to results.csv
Saved JSON to results.json
```

---

### Bulk Scanning (Top 1 Million Domains)

Your tool supports bulk scans from the Tranco Top-1M list.

#### 1. Place your Tranco CSV file:

```
E:\subdomain_ennumeration_Project\top-1m.csv
```

#### 2. Edit bulk_scan.py

Set how many domains you wish to scan:

```python
domains = read_tranco_csv("top-1m.csv", limit=20)
```

#### 3. Run bulk scan:

```powershell
python bulk_scan.py
```

Results are saved as separate CSV/JSON files in:

```
bulk_results/
```

…and inserted into the SQLite database.

---

## 💾 Database Storage

All scan results are saved into:

```
subdomain_scans.db
```

Schema example:

| Field            | Description                      |
|------------------|-----------------------------------|
| domain           | e.g. example.com                  |
| subdomain        | e.g. www.example.com              |
| ip               | resolved IP address               |
| reverse_dns      | PTR record                        |
| scheme           | http / https                      |
| url              | full URL                          |
| status           | HTTP response code                |
| length           | page size                         |
| title            | HTML title tag                    |
| content_hash     | SHA256 hash of page content       |
| server_header    | Server header                     |
| ssl_sans         | SSL Subject Alternative Names     |
| open_ports       | scanned open ports                |
| banners          | banner grab from open ports       |

---

## 🔎 Query Your Data

Example SQL queries:

### Show all successful subdomains

```sql
SELECT subdomain, url, status
FROM scan_results
WHERE status = 200;
```

---

### Find servers running Nginx

```sql
SELECT domain, subdomain, server_header
FROM scan_results
WHERE server_header LIKE '%nginx%';
```

---

### List subdomains with open ports

```sql
SELECT domain, subdomain, open_ports
FROM scan_results
WHERE open_ports IS NOT NULL AND open_ports <> '';
```

---

### Filter by specific domain

```sql
SELECT *
FROM scan_results
WHERE domain = 'facebook.com';
```

---

## 📊 Exporting Data

From DB Browser for SQLite:
- Export tables as CSV or JSON
- Build reports and dashboards

---

## 🌟 Future Enhancements

- Threat intelligence integration:
  - Shodan
  - VirusTotal
- Dashboard visualization
- Vulnerability detection

---

## 🤝 Disclaimer

This tool is for **educational and security research purposes only.**  
Do not scan domains you do not own or have permission to test.

---

Built for research, bug bounty, and large-scale asset discovery.
