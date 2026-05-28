<div align="center">

# 🔎 Python Port Scanner

**Multi-threaded TCP port scanner developed with Python for network reconnaissance and service enumeration.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Socket Programming](https://img.shields.io/badge/Socket_Programming-000000?style=for-the-badge&logo=python&logoColor=white)
![Threading](https://img.shields.io/badge/Threading-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![Version](https://img.shields.io/badge/version-2.0-blue)
![Status](https://img.shields.io/badge/status-stable-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

</div>

---

## 📌 Table of Contents

- [Features](#-features)
- [Technologies](#️-technologies-used)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Example Output](#-example-output)
- [Project Structure](#-project-structure)
- [Learning Objectives](#-learning-objectives)
- [Disclaimer](#-disclaimer)
- [Author](#-author)
- [License](#-license)

---

## 📌 Features

| Feature                       | Description                                  |
| ----------------------------- | -------------------------------------------- |
| ✅ **Multi-threaded scanning** | Fast port scanning using thread pooling      |
| ✅ **Service detection**       | Identifies services running on open ports    |
| ✅ **Banner grabbing**         | Retrieves service banners for fingerprinting |
| ✅ **Custom port range**       | Scan specific port ranges (1-65535)          |
| ✅ **Single host scanning**    | Scan individual IP addresses                 |
| ✅ **Network scanning**        | Scan entire /24 subnets                      |
| ✅ **Colored output**          | Beautiful terminal output with colors        |
| ✅ **Result export**           | Saves results to timestamped text files      |
| ✅ **Graceful interrupt**      | Ctrl+C saves partial results                 |

---

## ⚙️ Technologies Used

| Technology             | Purpose                       |
| ---------------------- | ----------------------------- |
| **Python 3.6+**        | Core programming language     |
| **Socket Programming** | TCP connection handling       |
| **Threading**          | Concurrent port scanning      |
| **ThreadPoolExecutor** | Efficient thread management   |
| **Colorama**           | Cross-platform colored output |
| **Argparse**           | Command-line argument parsing |

---

## 📋 Requirements

### System Requirements
- **Python 3.6** or higher
- **Linux / macOS / Windows** (cross-platform)

### Python Dependencies
```txt
colorama>=0.4.6
Note: All other modules (socket, threading, argparse, concurrent.futures, datetime) are part of Python's standard library.

🚀 Installation
1. Clone the repository
bash
git clone https://github.com/phllonq/python-port-scanner.git
2. Enter project directory
bash
cd python-port-scanner
3. Install dependencies
bash
pip install -r requirements.txt
4. Make scanner executable (Linux/macOS)
bash
chmod +x scanner.py
▶️ Usage
Basic Syntax
bash
python scanner.py <TARGET> <START_PORT> <END_PORT> [OPTIONS]
Single Host Scan
bash
# Scan ports 1-1000 on a single host
python scanner.py scanme.nmap.org 1 1000

# Scan localhost
python scanner.py 127.0.0.1 1 1000

# Full port scan (1-65535) - slow but thorough
python scanner.py 192.168.1.1 1 65535

# Fast scan with 200 threads
python scanner.py 192.168.1.1 20 443 -w 200
Network Scan (/24 subnet)
bash
# Scan entire network for common ports
python scanner.py 192.168.1 1 100 -n

# Network scan with custom thread count
python scanner.py 10.0.0 80 443 -n -w 150
Command-line Options
Option	Description	Default
target	IP address or network (e.g., 192.168.1)	Required
start_port	Starting port number	Required
end_port	Ending port number	Required
-n, --network	Scan entire /24 network range	False
-w, --workers	Maximum number of threads	100
-o, --output	Custom output filename	Auto-generated
-h, --help	Show help message	-
📄 Example Output
Terminal Output
bash
$ python scanner.py scanme.nmap.org 1 100

============================================================
       Python TCP Port Scanner v2.0
       Multi-threaded Network Scanner
============================================================

============================================================
[*] Starting TCP scan on host: scanme.nmap.org
[*] Port range: 1-100
[*] Max threads: 100
[*] Start time: 2026-05-23 14:30:25
============================================================

╔══════════════════════════════════════════════════════════╗
║ OPEN PORT FOUND                                            ║
╠══════════════════════════════════════════════════════════╣
║ Host: scanme.nmap.org                                     ║
║ Port: 22                                                  ║
║ Service: ssh                                              ║
║ Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5          ║
╚══════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════╗
║ OPEN PORT FOUND                                            ║
╠══════════════════════════════════════════════════════════╣
║ Host: scanme.nmap.org                                     ║
║ Port: 80                                                  ║
║ Service: http                                             ║
║ Banner: Apache/2.4.41 (Ubuntu)                            ║
╚══════════════════════════════════════════════════════════╝

[*] Progress: 100.0% (100/100)

============================================================
[+] Scan complete for host: scanme.nmap.org
[+] End time: 2026-05-23 14:30:37
[+] Open ports found: 2
============================================================

[+] Results saved to: scan_results_20260523_143037.txt
[+] Scan completed successfully!
Output File (scan_results_*.txt)
txt
================================================================================
TCP PORT SCAN RESULTS
================================================================================
Target: scanme.nmap.org (45.33.32.156)
Scan time: 2026-05-23 14:30:25
Scan duration: 12.3 seconds
Total open ports: 11
================================================================================

PORT     STATE    SERVICE     BANNER
22/tcp   open     ssh         SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
80/tcp   open     http        Apache/2.4.41 (Ubuntu)
443/tcp  open     https       nginx/1.18.0

================================================================================
SUMMARY
================================================================================
🔴 High risk ports: None detected
🟡 Medium risk ports: 22(SSH), 443(HTTPS)
🟢 Web services: 80, 443
================================================================================
📂 Project Structure
txt
python-port-scanner/
│
├── scanner.py              # Main scanner script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
│
├── screenshots/           # Demo screenshots
│   └── demo.png
│
└── scan_results_*.txt     # Generated scan results (auto-named with timestamp)
🧠 Learning Objectives
This project was built to practice and improve understanding of:

Topic	Description
🔌 TCP port scanning	Understanding TCP handshake and port states
🎯 Service enumeration	Identifying services from port numbers
📡 Banner grabbing	Extracting service fingerprints
🧵 Multi-threading	Concurrent programming in Python
🖧 Socket programming	Low-level network communication
⚙️ ThreadPoolExecutor	Efficient thread management
🎨 CLI development	Building user-friendly command-line tools
📊 Result formatting	Structured output and file handling
⚠️ Disclaimer
IMPORTANT: This project is intended for educational purposes and authorized testing environments only.

✅ DO use on your own systems or with explicit permission

✅ DO use on platforms like HackTheBox, TryHackMe, or scanme.nmap.org

❌ DO NOT scan systems or networks without proper authorization

❌ DO NOT use for malicious purposes

Unauthorized port scanning may be:

Illegal in many jurisdictions

Against terms of service

Considered a cyber attack

The author assumes no liability for misuse of this tool.

👨‍💻 Author
Dino (phllonq)

🔐 Cybersecurity Student

🎯 Focus: Penetration Testing, Web Security, Network Analysis

🌍 Location: Binh Duong / Ho Chi Minh City, Vietnam

Connect With Me
Platform	Link
GitHub	@phllonq
TryHackMe	Dinok2
Email	18012006tranphilong@gmail.com
📄 License
text
MIT License

Copyright (c) 2026 Dino (phllonq)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
⭐ Show Your Support
If you found this project helpful or learned something from it:

⭐ Star the repository on GitHub

🍴 Fork it and experiment

📢 Share it with others learning cybersecurity

🐛 Report issues or suggest improvements

🙏 Acknowledgments
Nmap - Inspiration for many scanning techniques

scanme.nmap.org - For providing a legal scanning target

Python Community - For excellent documentation and libraries

<div align="center">
Made with ❤️ for the cybersecurity community

Keep learning, keep building, stay ethical!

</div> ```

