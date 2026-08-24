import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from utils import get_public_ip

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

@dataclass
class CloudflareRecord:
    id: str
    type: str
    name: str
    content: str
    ttl: int


class CloudflareDDNS:
    token: str
    zone_name: str
    zone_id: str|None
    headers: dict
    ipv4_record: list
    ipv6_record: list
    ipv4_providers: list
    ipv6_providers: list
    ipv4: str|None
    ipv6: str|None

    def run(self):
        # prepare the log callback function for gui
        self.log_callback = print

        self.log_callback("🔑 Checking credentials...")
        self.check_credentials()

        self.log_callback("\n🌐 Getting Zone ID...")
        self.zone_id = self.get_zone_id()

        self.log_callback("\n🌐 Checking selected DNS records...")
        self.check_records()

        self.log_callback("\n🌐 Checking IP providers...")
        self.check_providers()

        self.log_callback("\n🌐 Getting public IP...")
        self.check_ip()

        self.log_callback("\n🌐 Getting DNS records...")
        records = self.get_records()
        if records:
            for record in records:
                self.log_callback(f"\n🌐 Updating record {record.name} [{record.type}]...")
                self.update_record(record)


    def check_credentials(self):
        self.token = os.getenv("CF_API_TOKEN", "")
        self.zone_name = os.getenv("ZONE_NAME", "")

        if not self.token or not self.zone_name:
            self.log_callback("⚠️ Token or domain not configured.")
            return

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self.log_callback("✅ Credentials verified successfully.")

    def check_records(self):
        self.ipv4_record = [
            r.strip() for r in os.getenv("IPV4_RECORDS", "").split(",") if r.strip()
        ]
        self.ipv6_record = [
            r.strip() for r in os.getenv("IPV6_RECORDS", "").split(",") if r.strip()
        ]
        self.log_callback(
            f"🌐 IPv4 Records: {self.ipv4_record or 'None/Failed'}\n🌐 IPv6 Records: {self.ipv6_record or 'None/Failed'}"
        )

    def check_providers(self):
        self.ipv4_providers = [
            p.strip() for p in os.getenv("IPV4_PROVIDERS", "").split(",") if p.strip()
        ]
        self.ipv6_providers = [
            p.strip() for p in os.getenv("IPV6_PROVIDERS", "").split(",") if p.strip()
        ]

        self.log_callback(
            f"🌐 IPv4 Providers: {self.ipv4_providers or 'None/Failed'}\n🌐 IPv6 Providers: {self.ipv6_providers or 'None/Failed'}"
        )

    def check_ip(self):
        self.ipv4 = get_public_ip(self.ipv4_providers)
        self.ipv6 = get_public_ip(self.ipv6_providers)

        if not self.ipv4 and not self.ipv6:
            self.log_callback("⚠️ No public IP obtained. Check the providers.")
            return

        self.log_callback(
            f"🌐 IPv4: {self.ipv4 or 'Disabled/Failed'}\n🌐 IPv6: {self.ipv6 or 'Disabled/Failed'}"
        )

    def get_zone_id(self) -> str|None:
        try:
            zone_resp = requests.get(
                f"https://api.cloudflare.com/client/v4/zones?name={self.zone_name}",
                headers=self.headers,
            ).json()
            if not zone_resp.get("success"):
                self.log_callback("❌ Error fetching zone. Check the token.")
                return

            zone_id = zone_resp["result"][0]["id"] if zone_resp["result"] else None
            if not zone_id:
                self.log_callback("❌ Zone not found. Check the domain.")
                return
        except requests.RequestException as e:
            self.log_callback(f"❌ Error fetching zone: {e}")
            return

        return zone_id

    def get_records(self) -> list[CloudflareRecord]|None:
        zone_id = self.zone_id

        try:
            records_resp = requests.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                headers=self.headers,
            ).json()
            if not records_resp.get("success"):
                self.log_callback("❌ Error fetching DNS records.")
                return

            records = records_resp.get("result", [])
            records_objects = []

            for record in records:
                records_objects.append(
                    CloudflareRecord(
                        id=record.get("id", ""),
                        type=record.get("type", ""),
                        name=record.get("name", ""),
                        content=record.get("content", ""),
                        ttl=record.get("ttl", 1),
                    )
                )
            self.log_callback(f"✅ {len(records_objects)} DNS records retrieved successfully.")
        except requests.RequestException as e:
            self.log_callback(f"❌ Error fetching DNS records: {e}")
            return

        return records_objects

    def update_record(self, record: CloudflareRecord):
        try:
            ip_map = {
                "A": self.ipv4,
                "AAAA": self.ipv6,
            }

            target_ip = ip_map.get(record.type)

            if not target_ip:
                self.log_callback(f"❌ Unsupported record type: {record.type}")
                return

            if record.content == target_ip:
                self.log_callback(f"✅ {record.name} [{record.type}] is already up to date.")
                return

            upd_url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{record.id}"
            response = requests.put(upd_url, headers=self.headers, json=record.__dict__)

            if response.json().get("success"):
                self.log_callback(f"✅ {record.name} [{record.type}] updated successfully -> {target_ip}.")
        except requests.RequestException as e:
            self.log_callback(f"❌ Error updating record {record.name} [{record.type}]: {e}")
