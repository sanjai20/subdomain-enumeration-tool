import csv
import subprocess
import time

def read_tranco_csv(path, limit=10):
    domains = []
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            domains.append(row[1].strip())
            if len(domains) >= limit:
                break
    return domains

def run_scan(domain, ports="80,443", use_https=True, output_dir="bulk_results"):
    cmd = [
        "python", "subdomain_enum.py",
        domain,
        "--ports", ports,
        "-o", f"{output_dir}/{domain.replace('.', '_')}.csv",
        "--json", f"{output_dir}/{domain.replace('.', '_')}.json"
    ]
    if use_https:
        cmd.append("--https")
    print(f"[*] Scanning {domain} ...")
    subprocess.run(cmd)

def main():
    domains = read_tranco_csv("top-1m.csv", limit=10)

    for domain in domains:
        run_scan(domain)
        time.sleep(1)  # optional delay to prevent being blocked

if __name__ == "__main__":
    main()
