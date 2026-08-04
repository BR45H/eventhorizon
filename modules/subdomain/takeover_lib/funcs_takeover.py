from .fingerprints import FINGERPRINTS
import dns.resolver
import requests
import urllib3

urllib3.disable_warnings()

def resolve_cname(subdomain: str, timeout: float = 5.0) -> str | None:
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout

    try:
        resp = resolver.resolve(subdomain, "CNAME")
        return str(resp[0].target).rstrip(".")

    except dns.resolver.NoAnswer:
        return None

    except dns.resolver.NXDOMAIN:
        return "NXDOMAIN"

    except Exception:
        return None

def identify_service(cname: str) -> str | None:
    for service, data in FINGERPRINTS.items():
        for sufix in data["cname"]:
            if sufix in cname:
                return service

    return None

def check_vuln(subdomain: str, service: str) -> bool:
    data = FINGERPRINTS[service]

    for schema in ("https", "http"):
        try:
            resp = requests.get(
                f"{schema}://{subdomain}",
                timeout=8,
                verify=False,
                allow_redirects=True,
            )

        except requests.exceptions.ConnectionError as e:
            if "Name or service not known" in str(e) or "nodename nor servname" in str(e):
                return True
            continue

        except requests.RequestException:
            continue

        body = resp.text
        for signature in data["fingerprint"]:
            if signature in body:
                return True

    return False

def process_subdomain(subdomain: str) -> dict | None:
    cname = resolve_cname(subdomain)

    if cname is None:
        return None

    if cname == "NXDOMAIN":
        return {
            "subdomain": subdomain,
            "cname": None,
            "service": None,
            "status": "NXDOMAIN",
            "detail": "Subdomain not resolving — investigate manually"
        }

    service = identify_service(cname)

    if service is None:
        target_status = resolve_cname(cname)
        if target_status == "NXDOMAIN":
            return {
                "subdomain": subdomain,
                "cname": cname,
                "service": None,
                "status": "VULNERABLE",
                "detail": "CNAME target does not resolve (dangling, unknown service)"
            }

        return {
        "subdomain": subdomain,
        "cname": cname,
        "service": None,
        "status": "unknown_service",
        "detail": "CNAME resolves but no fingerprint match — manual review recommended"
        }
    
    vuln = check_vuln(subdomain, service)

    return {
        "subdomain": subdomain,
        "cname": cname,
        "service": service,
        "status": "VULNERABLE" if vuln else "cname_points_but_ok"
    }