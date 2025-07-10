# Subdomain Enumeration Tool

A fast, multithreaded Python tool for discovering subdomains of a target domain.  
Useful for cybersecurity reconnaissance, bug bounty hunting, and infrastructure mapping.

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/status-active-brightgreen)

---

## 🚀 Features

✅ Supports both **HTTP** and **HTTPS**  
✅ Multithreaded scanning for speed  
✅ DNS resolution checks to avoid unnecessary HTTP requests  
✅ Logs results and errors to a log file  
✅ Progress bar with `tqdm` for real-time updates  
✅ Rate limiting to avoid getting blocked  
✅ Command-line interface with flexible options  
✅ Outputs discovered subdomains to a file

---

## 🛠 Installation

First, clone this repository:

```bash
git clone https://github.com/sanjai20/subdomain-enumeration-tool.git
cd subdomain-enumeration-tool
```

Install required Python packages:

```bash
pip install requests tqdm
```

---

## 📄 Usage

Basic scan:

```bash
python subdomain_enum.py example.com
```

Advanced usage:

```bash
python subdomain_enum.py example.com -w subdomains.txt -o results.txt -r 0.5
```

| Option                | Description                                  |
|------------------------|----------------------------------------------|
| `example.com`         | Domain to scan                               |
| `-w subdomains.txt`   | Path to subdomain wordlist (default: `subdomains.txt`) |
| `-o results.txt`      | Output file for discovered subdomains (default: `discovered_subdomains.txt`) |
| `-r 0.5`              | Delay (in seconds) between requests (default: 0.2) |

---

## 🔍 Example

Sample wordlist (`subdomains.txt`):

```
www
mail
api
ftp
blog
test
```

Run the tool:

```bash
python subdomain_enum.py youtube.com -w subdomains.txt -o found.txt -r 0.3
```

Sample output saved in `found.txt`:

```
http://www.youtube.com (200)
https://mail.youtube.com (200)
```

Logs are stored in:

```
subdomain_enum.log
```

---

## 💡 How It Works

- Loads subdomain names from a file
- Resolves each subdomain using DNS
- Sends HTTP/HTTPS requests to check availability
- Runs threads concurrently for speed
- Logs results and errors
- Saves discovered subdomains to an output file

---

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a PR or issue.

---

## 🙋‍♂️ Author

**Sanjai**  
[GitHub Profile](https://github.com/sanjai20)

---
