"""
Rule-based threat detection rules for STRIDE categories.
Each rule is a dict with:
  - id, stride_category, title, description, check (callable), impact, likelihood,
    severity, evidence_fn (callable), mitigation, patterns
"""
from __future__ import annotations
from typing import Callable, List, Dict, Any

from core.models import Component, DataFlow, Architecture


# ── Helper predicates ─────────────────────────────────────────────────────────

def _is_internet(c: Component) -> bool:
    return c.internet_facing

def _no_auth(c: Component) -> bool:
    return not c.authentication

def _no_authz(c: Component) -> bool:
    return not c.authorization

def _no_enc_rest(c: Component) -> bool:
    return not c.encryption_at_rest

def _no_logging(c: Component) -> bool:
    return not c.logging_enabled

def _no_rate_limit(c: Component) -> bool:
    return not c.rate_limiting

def _no_input_val(c: Component) -> bool:
    return not c.input_validation

def _sensitive(c: Component) -> bool:
    return c.data_sensitivity in ("high", "critical")

def _is_db(c: Component) -> bool:
    return c.type.lower() in ("database", "db", "storage")

def _is_external(c: Component) -> bool:
    return c.type.lower() in ("external", "user", "actor")

def _is_admin(c: Component) -> bool:
    return "admin" in c.name.lower() or "administrator" in c.name.lower()

def _is_api(c: Component) -> bool:
    return "api" in c.name.lower() or "gateway" in c.name.lower()

def _flow_unencrypted(df: DataFlow) -> bool:
    return not df.encrypted

def _flow_unauthenticated(df: DataFlow) -> bool:
    return not df.authenticated

def _flow_crosses_boundary(df: DataFlow) -> bool:
    return df.crosses_trust_boundary

def _flow_insecure_proto(df: DataFlow) -> bool:
    return df.protocol.upper() in ("HTTP", "FTP", "TELNET", "SMTP")


# ── Component-level rules ─────────────────────────────────────────────────────

COMPONENT_RULES: List[Dict[str, Any]] = [

    # ── SPOOFING ──────────────────────────────────────────────────────────────
    {
        "id": "SPO-001",
        "stride_category": "Spoofing",
        "title": "Missing Authentication on Internet-Facing Service",
        "description": (
            "The component is accessible from the internet but does not enforce "
            "authentication, allowing any party to masquerade as a legitimate user."
        ),
        "check": lambda c, _: _is_internet(c) and _no_auth(c),
        "impact": 4, "likelihood": 5, "severity": "Critical",
        "evidence_fn": lambda c, _: (
            f"Component '{c.name}' is internet-facing={c.internet_facing} "
            f"and authentication={c.authentication}."
        ),
        "mitigation": "Implement strong authentication (e.g., OAuth 2.0, JWT) on all internet-facing endpoints.",
        "patterns": ["Strong Authentication", "Token-Based Authentication", "Multi-Factor Authentication"],
    },
    {
        "id": "SPO-002",
        "stride_category": "Spoofing",
        "title": "External Entity Without Identity Verification",
        "description": (
            "An external entity interacts with the system without verified identity, "
            "enabling spoofing of trusted users or services."
        ),
        "check": lambda c, _: _is_external(c) and _no_auth(c),
        "impact": 3, "likelihood": 4, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"External entity '{c.name}' (type={c.type}) has authentication={c.authentication}."
        ),
        "mitigation": "Verify all external entity identities using certificates or token-based auth.",
        "patterns": ["Strong Authentication", "Token-Based Authentication"],
    },
    {
        "id": "SPO-003",
        "stride_category": "Spoofing",
        "title": "Administrative Interface Without Strong Authentication",
        "description": (
            "Administrative interfaces with weak or no authentication are prime targets "
            "for credential spoofing and account takeover."
        ),
        "check": lambda c, _: _is_admin(c) and _no_auth(c),
        "impact": 5, "likelihood": 3, "severity": "Critical",
        "evidence_fn": lambda c, _: (
            f"Admin component '{c.name}' has authentication={c.authentication}."
        ),
        "mitigation": "Apply MFA and strong password policies to all administrative accounts.",
        "patterns": ["Multi-Factor Authentication", "Strong Authentication"],
    },

    # ── TAMPERING ─────────────────────────────────────────────────────────────
    {
        "id": "TAM-001",
        "stride_category": "Tampering",
        "title": "Missing Input Validation",
        "description": (
            "The component does not validate incoming data, creating opportunities "
            "for injection attacks, data corruption, and business-logic tampering."
        ),
        "check": lambda c, _: _no_input_val(c) and (_is_internet(c) or _is_api(c)),
        "impact": 4, "likelihood": 4, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"Component '{c.name}': input_validation={c.input_validation}, "
            f"internet_facing={c.internet_facing}."
        ),
        "mitigation": "Apply strict server-side input validation and output encoding on all inputs.",
        "patterns": ["Input Validation", "Output Encoding"],
    },
    {
        "id": "TAM-002",
        "stride_category": "Tampering",
        "title": "Database Write Without Authorization",
        "description": (
            "A database component has no authorization controls, allowing any service "
            "to write or modify data without access checks."
        ),
        "check": lambda c, _: _is_db(c) and _no_authz(c),
        "impact": 4, "likelihood": 3, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"Database '{c.name}': authorization={c.authorization}."
        ),
        "mitigation": "Enforce RBAC for all database write operations; use parameterized queries.",
        "patterns": ["Database Access Control", "Role-Based Access Control"],
    },
    {
        "id": "TAM-003",
        "stride_category": "Tampering",
        "title": "Sensitive Data Stored Without Encryption",
        "description": (
            "Sensitive data stored without encryption can be directly tampered with "
            "if storage is compromised."
        ),
        "check": lambda c, _: _sensitive(c) and _no_enc_rest(c),
        "impact": 4, "likelihood": 3, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"Component '{c.name}': data_sensitivity={c.data_sensitivity}, "
            f"encryption_at_rest={c.encryption_at_rest}."
        ),
        "mitigation": "Encrypt all sensitive data at rest using AES-256 or similar.",
        "patterns": ["Encryption at Rest", "Secrets Management"],
    },

    # ── REPUDIATION ───────────────────────────────────────────────────────────
    {
        "id": "REP-001",
        "stride_category": "Repudiation",
        "title": "Audit Logging Disabled",
        "description": (
            "Without logging, users can deny performing actions and forensic "
            "investigation becomes impossible."
        ),
        "check": lambda c, _: _no_logging(c) and not _is_external(c),
        "impact": 3, "likelihood": 3, "severity": "Medium",
        "evidence_fn": lambda c, _: f"Component '{c.name}': logging_enabled={c.logging_enabled}.",
        "mitigation": "Enable tamper-resistant audit logging for all significant operations.",
        "patterns": ["Secure Logging", "Audit Trail"],
    },
    {
        "id": "REP-002",
        "stride_category": "Repudiation",
        "title": "Sensitive Transaction Without Non-Repudiation",
        "description": (
            "Sensitive financial or high-value operations lack logging, making it "
            "impossible to prove or dispute transaction ownership."
        ),
        "check": lambda c, _: _sensitive(c) and _no_logging(c),
        "impact": 4, "likelihood": 3, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"Component '{c.name}': data_sensitivity={c.data_sensitivity}, "
            f"logging_enabled={c.logging_enabled}."
        ),
        "mitigation": "Implement tamper-proof audit trails linked to verified user identities.",
        "patterns": ["Audit Trail", "Digital Signatures"],
    },

    # ── INFORMATION DISCLOSURE ───────────────────────────────────────────────
    {
        "id": "INF-001",
        "stride_category": "InformationDisclosure",
        "title": "Database Directly Exposed to Internet",
        "description": (
            "A database component is directly reachable from external zones, "
            "dramatically increasing the risk of data leakage."
        ),
        "check": lambda c, _: _is_db(c) and _is_internet(c),
        "impact": 5, "likelihood": 3, "severity": "Critical",
        "evidence_fn": lambda c, _: (
            f"Database '{c.name}': type={c.type}, internet_facing={c.internet_facing}."
        ),
        "mitigation": "Place databases in private network zones; never expose them directly to the internet.",
        "patterns": ["Network Segmentation", "Database Access Control"],
    },
    {
        "id": "INF-002",
        "stride_category": "InformationDisclosure",
        "title": "Sensitive Data Without Encryption at Rest",
        "description": (
            "Sensitive information stored in plaintext can be read by anyone with "
            "file-system or backup access."
        ),
        "check": lambda c, _: _sensitive(c) and _no_enc_rest(c) and _is_db(c),
        "impact": 5, "likelihood": 3, "severity": "Critical",
        "evidence_fn": lambda c, _: (
            f"Database '{c.name}': data_sensitivity={c.data_sensitivity}, "
            f"encryption_at_rest={c.encryption_at_rest}."
        ),
        "mitigation": "Encrypt sensitive columns and database files using AES-256.",
        "patterns": ["Encryption at Rest"],
    },
    {
        "id": "INF-003",
        "stride_category": "InformationDisclosure",
        "title": "Missing Secrets Management",
        "description": (
            "Credentials, API keys, and configuration secrets are likely stored in "
            "plaintext configuration files or environment variables."
        ),
        # Only fire if logging is also disabled — indicates immature security posture
        "check": lambda c, _: (
            (_is_api(c) or "auth" in c.name.lower() or "service" in c.type.lower())
            and _no_logging(c)
            and _no_enc_rest(c)
        ),
        "impact": 4, "likelihood": 3, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"Component '{c.name}' (type={c.type}) handles sensitive configuration "
            f"but has logging_enabled={c.logging_enabled} and encryption_at_rest={c.encryption_at_rest}."
        ),
        "mitigation": "Use a secrets management system (Vault, AWS Secrets Manager, etc.) for all credentials.",
        "patterns": ["Secrets Management"],
    },

    # ── DENIAL OF SERVICE ─────────────────────────────────────────────────────
    {
        "id": "DOS-001",
        "stride_category": "DenialOfService",
        "title": "Public Service Without Rate Limiting",
        "description": (
            "Internet-facing services without rate limiting are vulnerable to "
            "volumetric denial-of-service and brute-force attacks."
        ),
        "check": lambda c, _: _is_internet(c) and _no_rate_limit(c),
        "impact": 4, "likelihood": 4, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"Component '{c.name}': internet_facing={c.internet_facing}, "
            f"rate_limiting={c.rate_limiting}."
        ),
        "mitigation": "Apply rate limiting and request throttling on all public-facing endpoints.",
        "patterns": ["Rate Limiting", "API Gateway"],
    },
    {
        "id": "DOS-002",
        "stride_category": "DenialOfService",
        "title": "Single Point of Failure",
        "description": (
            "The component has no redundancy or failover mechanism, making the "
            "entire system vulnerable to unavailability."
        ),
        # Only fire if explicitly marked non-redundant AND no rate limiting
        "check": lambda c, _: (
            not c.metadata.get("redundant", True)
            and _is_internet(c)
            and _no_rate_limit(c)
        ),
        "impact": 4, "likelihood": 3, "severity": "High",
        "evidence_fn": lambda c, _: (
            f"Component '{c.name}' is internet-facing with no redundancy configured."
        ),
        "mitigation": "Implement load balancing, redundancy, and auto-failover for critical components.",
        "patterns": ["Redundancy and Failover", "Circuit Breaker"],
    },

    # ── ELEVATION OF PRIVILEGE ────────────────────────────────────────────────
    {
        "id": "EOP-001",
        "stride_category": "ElevationOfPrivilege",
        "title": "Missing Authorization Controls",
        "description": (
            "The component performs operations without authorisation checks, "
            "potentially allowing any authenticated user to perform privileged actions."
        ),
        "check": lambda c, _: _no_authz(c) and not _is_external(c),
        "impact": 4, "likelihood": 3, "severity": "High",
        "evidence_fn": lambda c, _: f"Component '{c.name}': authorization={c.authorization}.",
        "mitigation": "Implement RBAC or ABAC to enforce least-privilege access.",
        "patterns": ["Role-Based Access Control", "Least Privilege"],
    },
    {
        "id": "EOP-002",
        "stride_category": "ElevationOfPrivilege",
        "title": "Administrative Functions Without Least Privilege",
        "description": (
            "Administrative functionality is accessible without strict privilege "
            "boundaries, enabling privilege escalation."
        ),
        "check": lambda c, _: _is_admin(c) and _no_authz(c),
        "impact": 5, "likelihood": 3, "severity": "Critical",
        "evidence_fn": lambda c, _: (
            f"Admin component '{c.name}': authorization={c.authorization}."
        ),
        "mitigation": "Apply least-privilege principle; use RBAC for all admin operations.",
        "patterns": ["Least Privilege", "Role-Based Access Control", "Zero Trust"],
    },
    {
        "id": "EOP-003",
        "stride_category": "ElevationOfPrivilege",
        "title": "Service With Excessive Permissions",
        "description": (
            "A service appears to have broad permissions without clear scoping, "
            "violating the principle of least privilege."
        ),
        "check": lambda c, _: not c.authorization and c.type.lower() == "service",
        "impact": 3, "likelihood": 3, "severity": "Medium",
        "evidence_fn": lambda c, _: (
            f"Service '{c.name}': authorization={c.authorization}."
        ),
        "mitigation": "Define and enforce granular permission scopes for each service.",
        "patterns": ["Least Privilege", "Attribute-Based Access Control"],
    },
]

# ── Data-flow level rules ─────────────────────────────────────────────────────

FLOW_RULES: List[Dict[str, Any]] = [

    # SPOOFING
    {
        "id": "SPO-F001",
        "stride_category": "Spoofing",
        "title": "Unauthenticated Data Flow",
        "description": (
            "Data is transmitted between components without authentication, "
            "enabling man-in-the-middle spoofing."
        ),
        "check": lambda df, _: _flow_unauthenticated(df),
        "impact": 3, "likelihood": 3, "severity": "Medium",
        "evidence_fn": lambda df, _: (
            f"Flow from '{df.source}' to '{df.destination}': "
            f"authenticated={df.authenticated}, protocol={df.protocol}."
        ),
        "mitigation": "Authenticate all inter-service communication using mutual TLS or signed tokens.",
        "patterns": ["Token-Based Authentication", "Strong Authentication"],
    },

    # TAMPERING
    {
        "id": "TAM-F001",
        "stride_category": "Tampering",
        "title": "Unencrypted Data Flow",
        "description": (
            "Data transmitted in plaintext can be intercepted and modified by "
            "adversaries with network access."
        ),
        "check": lambda df, _: _flow_unencrypted(df),
        "impact": 4, "likelihood": 4, "severity": "High",
        "evidence_fn": lambda df, _: (
            f"Flow from '{df.source}' to '{df.destination}': "
            f"encrypted={df.encrypted}, protocol={df.protocol}."
        ),
        "mitigation": "Enforce TLS/HTTPS for all data flows, especially across trust boundaries.",
        "patterns": ["Encryption in Transit"],
    },
    {
        "id": "TAM-F002",
        "stride_category": "Tampering",
        "title": "Insecure Protocol in Use",
        "description": (
            "An insecure protocol (HTTP, FTP, Telnet) is used for data transmission, "
            "making data modification trivial."
        ),
        "check": lambda df, _: _flow_insecure_proto(df),
        "impact": 4, "likelihood": 4, "severity": "High",
        "evidence_fn": lambda df, _: (
            f"Flow from '{df.source}' to '{df.destination}': protocol={df.protocol}."
        ),
        "mitigation": "Replace insecure protocols with their secure equivalents (HTTPS, SFTP, SSH).",
        "patterns": ["Encryption in Transit"],
    },

    # REPUDIATION
    {
        "id": "REP-F001",
        "stride_category": "Repudiation",
        "title": "Trust Boundary Crossing Without Audit",
        "description": (
            "Data crossing a trust boundary is not logged, making it impossible to "
            "investigate cross-boundary attacks."
        ),
        # Only fire if BOTH crosses boundary AND source component has logging disabled
        "check": lambda df, arch: (
            _flow_crosses_boundary(df) and _flow_unauthenticated(df)
            and not _has_logging(df, arch)
        ),
        "impact": 3, "likelihood": 3, "severity": "Medium",
        "evidence_fn": lambda df, _: (
            f"Flow from '{df.source}' to '{df.destination}': "
            f"crosses_trust_boundary={df.crosses_trust_boundary}, "
            f"authenticated={df.authenticated}."
        ),
        "mitigation": "Log and monitor all data crossing trust boundaries with contextual metadata.",
        "patterns": ["Audit Trail", "Secure Logging"],
    },

    # INFORMATION DISCLOSURE
    {
        "id": "INF-F001",
        "stride_category": "InformationDisclosure",
        "title": "Sensitive Data in Unencrypted Flow",
        "description": (
            "Sensitive data is transmitted without encryption, exposing it to "
            "network eavesdroppers."
        ),
        "check": lambda df, arch: (
            _flow_unencrypted(df) and (
                "sensitive" in df.data.lower()
                or "password" in df.data.lower()
                or "payment" in df.data.lower()
                or "credit" in df.data.lower()
                or "personal" in df.data.lower()
                or "token" in df.data.lower()
                or _is_sensitive_flow(df, arch)
            )
        ),
        "impact": 5, "likelihood": 4, "severity": "Critical",
        "evidence_fn": lambda df, _: (
            f"Flow from '{df.source}' to '{df.destination}': "
            f"data='{df.data}', encrypted={df.encrypted}."
        ),
        "mitigation": "Apply end-to-end encryption for all flows carrying sensitive data.",
        "patterns": ["Encryption in Transit", "Encryption at Rest"],
    },

    # DENIAL OF SERVICE
    {
        "id": "DOS-F001",
        "stride_category": "DenialOfService",
        "title": "External Flow Without Input Size Control",
        "description": (
            "Flows from external entities lack size or rate controls, enabling "
            "resource exhaustion attacks."
        ),
        "check": lambda df, arch: _is_external_flow(df, arch),
        "impact": 3, "likelihood": 3, "severity": "Medium",
        "evidence_fn": lambda df, arch: (
            f"Flow from '{df.source}' to '{df.destination}' originates from an external entity."
        ),
        "mitigation": "Enforce request size limits and rate controls at API gateway.",
        "patterns": ["Rate Limiting", "API Gateway", "Circuit Breaker"],
    },

    # ELEVATION OF PRIVILEGE
    {
        "id": "EOP-F001",
        "stride_category": "ElevationOfPrivilege",
        "title": "Privilege Escalation via Unauthenticated Trust Boundary Crossing",
        "description": (
            "An unauthenticated flow crosses a trust boundary, potentially enabling "
            "privilege escalation into a higher-privilege zone."
        ),
        "check": lambda df, _: _flow_crosses_boundary(df) and _flow_unauthenticated(df),
        "impact": 4, "likelihood": 3, "severity": "High",
        "evidence_fn": lambda df, _: (
            f"Flow from '{df.source}' to '{df.destination}': "
            f"crosses_trust_boundary={df.crosses_trust_boundary}, "
            f"authenticated={df.authenticated}."
        ),
        "mitigation": "Authenticate all cross-boundary flows; enforce Zero Trust principles.",
        "patterns": ["Zero Trust", "Role-Based Access Control"],
    },
]


def _is_sensitive_flow(df: DataFlow, arch: Architecture) -> bool:
    src = arch.get_component(df.source)
    dst = arch.get_component(df.destination)
    for c in (src, dst):
        if c and c.data_sensitivity in ("high", "critical"):
            return True
    return False


def _is_external_flow(df: DataFlow, arch: Architecture) -> bool:
    src = arch.get_component(df.source)
    if src and src.type.lower() in ("user", "external", "actor"):
        return True
    return False


def _has_logging(df: DataFlow, arch: Architecture) -> bool:
    """Returns True if BOTH source and destination have logging enabled."""
    src = arch.get_component(df.source)
    dst = arch.get_component(df.destination)
    src_log = src.logging_enabled if src else False
    dst_log = dst.logging_enabled if dst else False
    return src_log and dst_log
