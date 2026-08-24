# PyCloudflareDDNS

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Cloudflare](https://img.shields.io/badge/Cloudflare-DNS%20API-F38020?logo=cloudflare&logoColor=white)](https://api.cloudflare.com/)
[![IPv4%20%2B%20IPv6](https://img.shields.io/badge/IPv4%20%2B%20IPv6-supported-2E8B57)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-1f6feb)](LICENSE)

[Versão em português](README.md)

## About

Automatically updates Cloudflare `A` (IPv4) and `AAAA` (IPv6) DNS records with
the machine's current public IP addresses. The program queries one or more IP
providers and only changes a record when its address has changed.

## Requirements

- Python 3.10 or newer
- A domain/zone managed by Cloudflare
- A Cloudflare API token with `Zone - Read` and `DNS - Edit` permissions for
  the desired zone

## Configuration

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   ```bash
   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # Linux/macOS
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```dotenv
   CF_API_TOKEN=your_cloudflare_api_token
   ZONE_NAME=example.com
   IPV4_RECORDS=home.example.com
   IPV6_RECORDS=
   IPV4_PROVIDERS=https://api.ipify.org,https://ifconfig.me/ip
   IPV6_PROVIDERS=https://api6.ipify.org
   ```

| Variable | Description |
| --- | --- |
| `CF_API_TOKEN` | API token with zone read and DNS edit access. |
| `ZONE_NAME` | Cloudflare zone domain. |
| `IPV4_RECORDS` | `A` record names, separated by commas. |
| `IPV6_RECORDS` | `AAAA` record names, separated by commas. |
| `IPV4_PROVIDERS` | URLs returning the public IPv4, separated by commas. |
| `IPV6_PROVIDERS` | URLs returning the public IPv6, separated by commas. |

Leave a record or provider list empty to disable that IP type. Providers are
tried in the listed order. Do not share `.env` or your API token.

## Important: IPv4 CGNAT

**CGNAT** (Carrier-Grade NAT) places multiple customers behind the same public
IPv4 address. In this situation, the address returned by IP providers may be
shared and does not allow direct inbound connections to your network, even when
the DNS record is updated correctly.

PyCloudflareDDNS updates DNS, but it cannot disable CGNAT or create a public
IPv4 address. To receive inbound IPv4 connections, ask your ISP to disable
CGNAT or provide a public IPv4 address. If the ISP does not offer that option,
you will need to change provider. IPv6 may continue to work normally if it is
available and correctly configured on your network.

## Running

With the virtual environment activated, run:

```bash
python main.py
```

The terminal output shows credential validation, detected IP addresses, and the
records that were updated. For automatic execution, schedule this command with
Windows Task Scheduler or `cron`.
