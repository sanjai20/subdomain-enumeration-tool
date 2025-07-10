import threading
import requests
import socket
import argparse
import time
import logging
from tqdm import tqdm

# -------------------------------
# Logging Configuration
# -------------------------------

logging.basicConfig(
    filename='subdomain_enum.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -------------------------------
# DNS Resolution Check
# -------------------------------

def is_resolvable(fqdn):
    try:
        socket.gethostbyname(fqdn)
        return True
    except socket.gaierror:
        return False

# -------------------------------
# Subdomain Check Function
# -------------------------------

def check_subdomain(subdomain, domain, discovered_subdomains, lock, rate_limit):
    fqdn = f"{subdomain}.{domain}"
    urls = [f"http://{fqdn}", f"https://{fqdn}"]

    if not is_resolvable(fqdn):
        logging.warning(f"Unresolvable: {fqdn}")
        return

    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            if status < 400:
                with lock:
                    discovered_subdomains.append(f"{url} ({status})")
                logging.info(f"[+] Found: {url} ({status})")
            else:
                logging.warning(f"[-] {url} returned status {status}")
        except requests.exceptions.RequestException as e:
            logging.warning(f"[!] Error connecting to {url}: {e}")
        time.sleep(rate_limit)

# -------------------------------
# Main Function
# -------------------------------

def main():
    parser = argparse.ArgumentParser(description="Advanced Subdomain Enumeration Tool")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", default="subdomains.txt", help="File containing subdomains")
    parser.add_argument("-o", "--output", default="discovered_subdomains.txt", help="Output file name")
    parser.add_argument("-r", "--rate", type=float, default=0.2, help="Rate limit (seconds between requests)")

    args = parser.parse_args()
    domain = args.domain
    input_file = args.wordlist
    output_file = args.output
    rate_limit = args.rate

    # Load subdomains
    try:
        with open(input_file, "r") as f:
            subdomains = f.read().splitlines()
    except FileNotFoundError:
        print(f"[-] Wordlist '{input_file}' not found.")
        return

    discovered_subdomains = []
    lock = threading.Lock()
    threads = []

    print(f"[*] Enumerating subdomains for: {domain}")
    time.sleep(0.5)

    for sub in tqdm(subdomains, desc="Scanning", ncols=80):
        t = threading.Thread(target=check_subdomain, args=(sub, domain, discovered_subdomains, lock, rate_limit))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Write output
    if discovered_subdomains:
        with open(output_file, "w") as f:
            for entry in discovered_subdomains:
                f.write(entry + "\n")
        print(f"[+] Discovered subdomains saved to {output_file}")
    else:
        print("[-] No subdomains discovered.")

    print(f"[✓] Log saved to subdomain_enum.log")

if __name__ == "__main__":
    main()
