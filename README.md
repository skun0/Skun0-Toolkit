# Skun0-Toolkit

A Python-based command-line toolkit for OSINT, domain reconnaissance, CCTV research, and network analysis.

Developed by [Skun0](https://github.com/skun0).

## Features

### OSINT

* Holehe email checks
* IP geolocation
* Phone number lookup
* Carrier and number type detection
* Timezone information
* Multiple phone number formats

### Domain Recon

* DNS record lookup
* A
* AAAA
* MX
* NS
* TXT
* CNAME
* SOA
* CAA
* WHOIS lookup
* Subdomain Finder placeholder

### Network Scanner

* TCP port scanner
* Custom port ranges
* Asynchronous scanning
* ARP network discovery
* MAC address detection

### CCTV

* Country listing
* Camera count by country
* Camera endpoint collection from publicly indexed sources

## Requirements

* Python 3.10+
* Git
* Npcap for Scapy on Windows

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/skun0/Skun0-Toolkit.git
cd Skun0-Toolkit
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the toolkit:

```bash
python main.py
```

## Usage

After starting the program, the main menu provides:

```text
[1] OSINT
[2] Domain Recon
[3] CCTV
[4] Network Scanner
[U] Check for updates
```

Select a module by entering its corresponding number.

## Updates

The toolkit includes a Git-based update system.

When `U` is selected, the program:

1. Checks the current Git repository.
2. Fetches the latest `main` branch from GitHub.
3. Compares the local commit with `origin/main`.
4. Downloads the latest version if an update is available.
5. Restarts the program after updating.

The update system requires the toolkit to be installed from the Git repository and Git to be available in the system PATH.

## Project Structure

```text
Skun0-Toolkit/
├── main.py
├── requirements.txt
├── README.md
```

## Notes

Some features depend on external services and may stop working if their endpoints, APIs, or website structure change.

Network scanning should only be performed against systems and networks you own or have permission to test.

## Roadmap

* Save results via JSON
* General code improvements
* Support for Linux/macOS

## License

This project is provided for educational and research purposes.
