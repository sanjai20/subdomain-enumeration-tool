import csv
import subprocess
from multiprocessing import Pool
import os
import time

def read_tranco_csv(path, limit=None):
    domains = []
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            domains.append(row[1].strip())
            if limit and len(domains) >= limit:
                break
    return domains

def worker(domain):
    output_dir = "bulk_results"
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "python",
        "subdomain_enum.py",
        domain,
        "--ports", "80,443",
        "--https",
        "-o", f"{output_dir}/{domain.replace('.', '_')}.csv",
        "--json", f"{output_dir}/{domain.replace('.', '_')}.json"
    ]

    print(f"[*] Scanning {domain} ...")
    subprocess.run(cmd, timeout=300)

def main():
    domains = read_tranco_csv("top-1m.csv", limit=20)

    with Pool(processes=4) as pool:
        pool.map(worker, domains)

if __name__ == "__main__":
    main()
