"""Connection settings, semantic health statuses, and server-side SSRF protection."""

from __future__ import annotations

import ipaddress
import re
import socket
from enum import Enum
from urllib.parse import urlparse

# Exact browser storage key per Step D acceptance criteria #6
CONNECTION_STORAGE_KEY = "analysts-ledger-agentos-url"
DEFAULT_ENDPOINT_URL = "/api"


class ConnectionState(str, Enum):
    """Semantic connection states for the Research Desk."""

    READY = "ready"
    CHECKING = "checking"
    OFFLINE = "offline"


def get_connection_status_label(state: str | ConnectionState) -> str:
    """Return the exact semantic label (Ready, Checking, Offline)."""
    val = state.value if isinstance(state, ConnectionState) else str(state)
    mapping = {
        "ready": "Ready",
        "checking": "Checking",
        "offline": "Offline",
    }
    return mapping.get(val.lower(), "Offline")


def normalize_endpoint_url(value: str | None) -> str:
    """Normalize endpoint URL: strip whitespace and trailing slashes; map /agentos to /api."""
    if not value:
        return DEFAULT_ENDPOINT_URL
    trimmed = value.strip().rstrip("/")
    if not trimmed or trimmed == "/agentos":
        return DEFAULT_ENDPOINT_URL
    return trimmed


# SSRF & Private Network Protection
PRIVATE_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),      # Loopback IPv4
    ipaddress.ip_network("10.0.0.0/8"),       # Private Class A
    ipaddress.ip_network("172.16.0.0/12"),    # Private Class B
    ipaddress.ip_network("192.168.0.0/16"),   # Private Class C
    ipaddress.ip_network("169.254.0.0/16"),   # Link-Local / Cloud Metadata (169.254.169.254)
    ipaddress.ip_network("0.0.0.0/8"),        # Current network
    ipaddress.ip_network("::1/128"),          # Loopback IPv6
    ipaddress.ip_network("fe80::/10"),        # Link-Local IPv6
    ipaddress.ip_network("fc00::/7"),         # Unique Local IPv6
]


def is_prohibited_ip(ip_obj: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Return True if IP is loopback, link-local, private, or reserved."""
    if ip_obj.is_loopback or ip_obj.is_private or ip_obj.is_link_local or ip_obj.is_reserved:
        return True
    return any(ip_obj in net for net in PRIVATE_NETWORKS)


def is_prohibited_ip_or_host(dest: str) -> bool:
    """Check if destination string contains a prohibited IP, localhost, or metadata address."""
    cleaned = dest.strip()
    if cleaned.startswith(("http://", "https://")):
        parsed = urlparse(cleaned)
        hostname = parsed.hostname or ""
    else:
        # Check directly if it is a raw IPv4/IPv6 address (e.g. fe80::1)
        raw_target = cleaned.strip("[]")
        try:
            ip = ipaddress.ip_address(raw_target)
            return is_prohibited_ip(ip)
        except ValueError:
            pass
        # Strip path/port if present for host:port or host/path
        hostname = re.split(r"[:/]", cleaned)[0].strip("[]")

    if not hostname:
        return True

    if hostname.lower() in {"localhost", "metadata", "instance-data"}:
        return True

    # Try parsing directly as IP
    try:
        ip = ipaddress.ip_address(hostname)
        return is_prohibited_ip(ip)
    except ValueError:
        pass

    # For link-local / metadata strings in URL
    if "169.254.169.254" in cleaned:
        return True

    return False


def validate_server_url_safety(url_str: str) -> tuple[bool, str]:
    """Validate URL destination against SSRF, internal networks, and DNS rebinding."""
    if not url_str or not url_str.strip():
        return False, "URL cannot be empty."

    parsed = urlparse(url_str.strip())
    hostname = parsed.hostname

    if not hostname:
        return False, "Invalid host in URL."

    if is_prohibited_ip_or_host(hostname):
        return False, f"Prohibited internal address or host: {hostname}"

    # DNS Resolution check (prevent DNS rebinding attacks)
    try:
        addr_info = socket.getaddrinfo(hostname, None)
        for _, _, _, _, sockaddr in addr_info:
            resolved_ip_str = sockaddr[0]
            try:
                ip_obj = ipaddress.ip_address(resolved_ip_str)
                if is_prohibited_ip(ip_obj):
                    return False, f"Resolved to prohibited internal address: {resolved_ip_str}"
            except ValueError:
                return False, f"Invalid resolved address format: {resolved_ip_str}"
    except (socket.gaierror, socket.herror) as exc:
        return False, f"Could not resolve host: {exc}"

    return True, "Safe"
