import requests


def get_public_ip(providers: list) -> str|None:
        if not providers:
            return None

        for url in providers:
            try:
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                ip = resp.text.strip()
                if ip:
                    return ip
            except requests.RequestException:
                continue
        return None
