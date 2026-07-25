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
* Fine-grained control over execution (timeouts, retries, rate)
* Consistent and predictable output
* Extensibility for future protocols and features

---

## Planned Features

### Subdomain

* Bruteforce-based subdomain discovery
* DNS resolution

### SMB

* Controlled connection handling
* Authentication attempts (user/password)
* Password spraying (rate-controlled)

### Core

* Target normalization (domain, IP, file input)
* Configurable execution parameters
* Logging and verbosity control

---

## CLI Design

The tool follows a simple structure:

```
eventhorizon <module> <action> [options]
```

Examples:

```
eventhorizon smb connect -t <target> --anonymous
eventhorizon smb spray -t <target> -U users.txt -P passwords.txt
eventhorizon subdomain bruteforce -t example.com -w subdomains.txt
eventhorizon subdomain bruteforce -t example.com -w subdomains.txt -r
```

---

## Execution Philosophy

Event Horizon is not designed to maximize throughput.

Instead, it focuses on:

* Controlled request pacing
* Minimal unnecessary noise
* Operator-defined behavior
* Safe defaults with optional tuning

---

## Status

This project is currently in early development.

Core architecture and CLI structure are being defined before full implementation.

---

## License

MIT License
