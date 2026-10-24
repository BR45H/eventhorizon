# 🇧🇷 [Versão em Português](README.pt-BR.md)
# Event Horizon

Event Horizon is a modular command-line tool designed for controlled network operations, enumeration, and connectivity testing.

The tool prioritizes precision, control, and low operational impact over raw speed or high-volume execution.

---

## Philosophy

Event Horizon is built around a simple principle:

> **Control over speed.**

Instead of performing aggressive, high-noise operations, the tool focuses on:

* Controlled execution
* Predictable behavior
* Low operational footprint
* Modular design
* Reliable CLI workflows

It is intended to act as a dependable “Swiss Army knife” for network-related tasks.

---

## Design Goals

* Modular architecture (`module -> action`)
* Clear and explicit command structure
* Fine-grained control over execution (timeouts, send mode, rate)
* Consistent and predictable output
* Extensibility for future protocols and features

---

## Modules & Actions

### tcp

* `synscan` — controlled SYN scan (via Scapy), with custom TTL and source port. Requires an explicit send mode (`sequential` or `batch`).
* `connectscan` — controlled TCP connect scan (full three-way handshake), with custom timeout. Requires an explicit send mode (`sequential` or `batch`).
* `portpeek` — one-off check on a single port.

### subdomain

* `bruteforce` — wordlist-based subdomain discovery, with optional DNS resolution and multithreaded lookups.
* `takeover` — subdomain takeover detection (CNAME resolution + service fingerprint database).

### smtp

* `vrfycrack` — SMTP user enumeration via the `VRFY` command, with optional banner grabbing.

---

## CLI Design

The tool follows a simple structure:

```
eventhorizon <module> <action> [options]
```

Examples:

```
eventhorizon tcp synscan -t example.com -m sequential
eventhorizon tcp synscan -t example.com -p 22,80,443 -m batch -v
eventhorizon tcp connectscan -t 192.168.1.1 -m batch --timeout 1.5
eventhorizon tcp portpeek -t example.com -p 443

eventhorizon subdomain bruteforce -t example.com -w subdomains.txt
eventhorizon subdomain bruteforce -t example.com -w subdomains.txt -r --threads 20
eventhorizon subdomain takeover -t example.com -w subdomains.txt -v

eventhorizon smtp vrfycrack -t mail.example.com -w users.txt -b -v
```

---

## Execution Philosophy

Event Horizon is not designed to maximize throughput.

Instead, it focuses on:

* Controlled request pacing
* Minimal unnecessary noise
* Operator-defined behavior
* Safe defaults with optional tuning — every port scan requires an explicit `--mode` (`sequential` or `batch`) instead of picking one silently

---

## Status

🚧 This project is under active early-stage development.

Implemented so far: TCP port scanning (SYN and connect-based, sequential and batch modes), subdomain bruteforce and takeover detection, SMTP user enumeration via VRFY.

---

## License

MIT License