<div align="center">

# 🔎 Python Port Scanner

Multi-threaded TCP port scanner developed with Python for network reconnaissance and service enumeration.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Socket Programming](https://img.shields.io/badge/Socket_Programming-000000?style=for-the-badge&logo=python&logoColor=white)
![Threading](https://img.shields.io/badge/Threading-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

</div>

---

# 📌 Features

- Multi-threaded TCP port scanning
- Service detection
- Banner grabbing
- Custom port range scanning
- Result export to text file
- Colored terminal output

---

# ⚙️ Technologies Used

- Python
- Socket Programming
- Threading
- TCP/IP Networking

---

# 📂 Project Structure

```txt
python-port-scanner/
│
├── scanner.py
├── requirements.txt
├── README.md
├── screenshots/
│   └── demo.png
└── scan_results.txt
🚀 Installation

Clone repository:

git clone https://github.com/phllonq/python-port-scanner.git

Enter project directory:

cd python-port-scanner

Install dependencies:

pip install -r requirements.txt
▶️ Usage

Basic scan:

python scanner.py -t scanme.nmap.org -p 1-1000

Localhost scan:

python scanner.py -t 127.0.0.1 -p 1-1000
📸 Demo




📄 Example Output
[OPEN] Port 22 | Service: ssh | Banner: OpenSSH
[OPEN] Port 80 | Service: http | Banner: Apache
[OPEN] Port 443 | Service: https | Banner: nginx
🧠 Learning Objectives

This project was built to practice and improve understanding of:

TCP port scanning
Service enumeration
Python socket programming
Multi-threading
Basic reconnaissance techniques
Network communication fundamentals
⚠️ Disclaimer

This project is intended for educational purposes and authorized testing environments only.

Do not use this tool against systems or networks without proper permission.

👨‍💻 Author

GitHub: https://github.com/phllonq