import ipaddress
import re
import socket
from scapy.all import IP, TCP, ICMP, sr1
from core.output import error

DOMAIN_REGEX = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))+$'

def parse_ports(ports: str) -> list[int]:
    valid_ports = []
    ports_list = ports.split(",")

    for port in ports_list:
        if "-" in port:
            range1, range2 = port.split("-")
            try:
                range1, range2 = int(range1), int(range2)
            except ValueError:
                error(f"Invalid range: {range1} - {range2}")
                return None

            if (0<range1<=65535) and (0<range2<=65535) and (range1<range2):
                for n in range(range1, range2+1):
                    valid_ports.append(n)
            else:
                error("Invalid range.")
                return None

        else:
            try:
                prt = int(port)
            except ValueError:
                error(f"Invalid port: {port}")
                return None

            if (0<prt<=65535):
                valid_ports.append(prt)
            else:
                error(f"Invalid port: {port}")
                return None

    return valid_ports
            
def normalize_target(target: str):
    try:
        ip = ipaddress.ip_address(target)
        return str(ip)
    except ValueError:
        pass

    if re.match(DOMAIN_REGEX, target):
        try:
            result = socket.getaddrinfo(target, None, socket.AF_UNSPEC)
            ip_resolved = result[0][4][0]
            return str(ip_resolved)
        except socket.gaierror as e:
            error(f"Error to resolve '{target}': {e}")
            return None

    error(f"Invalid target: {target}")
    return None

def interpreting_response_TCP(resp) -> str:
    if resp is None:
        return "filtered"
    
    elif resp.haslayer(TCP):
        if resp[TCP].flags == "SA":
            return "open"
        
        elif resp[TCP].flags == "RA":
            return "closed"
        
    elif resp.haslayer(ICMP):
        return "filtered"

    else:
        return "unknown"

def csr_TCP(target: str, ttl: int, src: int, port: int):
    pkt = IP(dst=target, ttl=ttl) / TCP(sport=src, dport=port, flags="S")
    resp = sr1(pkt, timeout=1, verbose=0)
    return resp
