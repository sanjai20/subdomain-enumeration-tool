# subdomain_enum.py

import requests
import socket
import argparse
import time
import hashlib
import csv
import json
import threading
import ssl
from tqdm import tqdm
from colorama import Fore, Style
from urllib.parse import urlparse
import os

from db_utils import init_db, save_result

# -----------------------------
# CONFIG
# -----------------------------

MAX_RETRIES = 3
TIMEOUT = 5
RATE_LIMIT = 0.3

# -----------------------------
# Wildcard Detection
# -----------------------------

def check_wildcard(domain):
    random_sub = f"randomxyz987.{domain}"
    try:
        ip = socket.gethostbyname(random_sub)
        print(f"{Fore.YELLOW}[!] Wildcard detected: {random_sub} resolves to {ip}{Style.RESET_ALL}")
        return ip
    except socket.gaierror:
        return None

# -----------------------------
# DNS Resolution
# -----------------------------

def resolve_domain(subdomain, domain):
    fqdn = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(fqdn)
        return fqdn, ip
    except socket.gaierror:
        return fqdn, None

# -----------------------------
# Reverse DNS
# -----------------------------

def reverse_dns(ip):
    try:
        host = socket.gethostbyaddr(ip)
        return host[0]
    except:
        return None

# -----------------------------
# SSL Certificate SANs
# -----------------------------

def get_ssl_sans(hostname):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(
            socket.socket(), server_hostname=hostname
        ) as s:
            s.settimeout(3)
            s.connect((hostname, 443))
            cert = s.getpeercert()
            sans = []
            for entry in cert.get("subjectAltName", []):
                if entry[0] == "DNS":
                    sans.append(entry[1])
            return sans
    except Exception:
        return []

# -----------------------------
# HTTP Check
# -----------------------------

def check_http(fqdn, scheme):
    url = f"{scheme}://{fqdn}"
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
            server_header = response.headers.get("Server", "")
            content_hash = hashlib.sha256(response.content).hexdigest()
            return {
                "url": url,
                "status": response.status_code,
                "content_hash": content_hash,
                "length": len(response.content),
                "title": get_title(response.text),
                "server": server_header
            }
        except Exception:
            retries += 1
            time.sleep(RATE_LIMIT)
    return None

def get_title(html_text):
    if "<title>" in html_text:
        start = html_text.find("<title>") + 7
        end = html_text.find("</title>")
        return html_text[start:end].strip()
    return None

# -----------------------------
# Banner Grabbing
# -----------------------------

def grab_banner(host, port):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        data = s.recv(1024)
        return data.decode(errors="ignore")
    except:
        return None

# -----------------------------
# Port Scanning
# -----------------------------

def scan_ports(hostname, ports):
    open_ports = []
    banners = {}
    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((hostname, port))
            open_ports.append(port)
            banner = grab_banner(hostname, port)
            banners[port] = banner
            s.close()
        except:
            pass
    return open_ports, banners

# -----------------------------
# Wayback Lookup
# -----------------------------

def wayback_lookup(domain):
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}&output=json&fl=original"
    try:
        r = requests.get(url, timeout=10)
        subs = set()
        if r.ok:
            data = r.json()
            for entry in data[1:]:
                parsed = urlparse(entry[0])
                sub = parsed.hostname
                if sub and sub.endswith(domain):
                    parts = sub.split(".")
                    if len(parts) > 2:
                        subs.add(parts[-3])
                    elif len(parts) == 2:
                        subs.add(parts[0])
        return list(subs)
    except:
        return []

# -----------------------------
# Save to CSV
# -----------------------------

def save_csv(results, output):
    keys = results[0].keys()
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

# -----------------------------
# Save to JSON
# -----------------------------

def save_json(results, output):
    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

# -----------------------------
# Main Scanning Logic
# -----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Target domain (e.g. example.com)")
    parser.add_argument("-w", "--wordlist", default="subdomains.txt", help="Wordlist file")
    parser.add_argument("-o", "--output", default="results.csv", help="Output CSV file")
    parser.add_argument("--json", help="Also save results to JSON file")
    parser.add_argument("--https", action="store_true", help="Test HTTPS in addition to HTTP")
    parser.add_argument("--ports", help="Comma-separated list of ports to scan (e.g. 22,80,443)")

    args = parser.parse_args()
    domain = args.domain
    port_list = [int(p.strip()) for p in args.ports.split(",")] if args.ports else []

    init_db()

    wildcard_ip = check_wildcard(domain)

    subdomains = []
    try:
        with open(args.wordlist, "r", encoding="utf-8") as f:
            subdomains.extend(f.read().splitlines())
    except FileNotFoundError:
        print(f"{Fore.YELLOW}[-] Wordlist not found. Continuing without it.{Style.RESET_ALL}")

    wb_subs = wayback_lookup(domain)
    if wb_subs:
        print(f"{Fore.CYAN}[+] Found {len(wb_subs)} subdomains from Wayback Machine.{Style.RESET_ALL}")
        subdomains.extend(wb_subs)

    subdomains = list(sorted(set(subdomains)))

    results = []
    lock = threading.Lock()

    def process(sub):
        fqdn, ip = resolve_domain(sub, domain)
        if ip:
            if wildcard_ip and ip == wildcard_ip:
                return

            ptr = reverse_dns(ip)
            open_ports, banners = scan_ports(fqdn, port_list) if port_list else ([], {})

            for scheme in ["http", "https"] if args.https else ["http"]:
                res = check_http(fqdn, scheme)
                if res:
                    sans = get_ssl_sans(fqdn) if scheme == "https" else []
                    row = {
                        "domain": domain,
                        "subdomain": fqdn,
                        "ip": ip,
                        "reverse_dns": ptr,
                        "scheme": scheme,
                        "url": res["url"],
                        "status": res["status"],
                        "length": res["length"],
                        "title": res["title"],
                        "content_hash": res["content_hash"],
                        "server_header": res["server"],
                        "ssl_sans": ", ".join(sans),
                        "open_ports": ",".join(str(p) for p in open_ports),
                        "banners": json.dumps(banners)
                    }
                    with lock:
                        results.append(row)
                        # ✅ Save to database!
                        save_result(row)
                        color = Fore.GREEN if res["status"] < 400 else Fore.YELLOW
                        print(f"{color}[+] {res['url']} ({res['status']}){Style.RESET_ALL}")

        time.sleep(RATE_LIMIT)

    threads = []
    for sub in tqdm(subdomains, desc="Scanning", ncols=80):
        t = threading.Thread(target=process, args=(sub,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if results:
        save_csv(results, args.output)
        print(f"{Fore.CYAN}Saved CSV to {args.output}{Style.RESET_ALL}")
        if args.json:
            save_json(results, args.json)
            print(f"{Fore.CYAN}Saved JSON to {args.json}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No subdomains discovered.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
