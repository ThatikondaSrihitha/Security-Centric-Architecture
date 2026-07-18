"""
12 Detailed Architecture Patterns page.
Layered, Microservices, Zero Trust, Secure MVC, Event-Driven,
Defense in Depth, API Gateway, Broker, Service Mesh, Client-Server, CQRS, Hexagonal.
"""
from __future__ import annotations
import streamlit as st
from page_modules.shared_styles import inject_css, page_header, section_heading

ARCH_PATTERNS = [
    {
        "id": "AP-001", "name": "Layered Architecture",
        "icon": "🏗️", "category": "Structural", "colour": "#00D4FF",
        "description": "Organizes code into horizontal layers (Presentation, Business Logic, Data Access) with strict dependencies flowing downward only.",
        "advantages": ["Clear separation of concerns", "Easy to test each layer independently", "Familiar pattern — wide developer knowledge", "Easy to replace individual layers"],
        "disadvantages": ["Can lead to 'sinkhole' anti-pattern", "Strict layering adds overhead", "May struggle with complex domains"],
        "use_cases": ["Enterprise web applications", "E-commerce platforms", "CMS systems", "Traditional REST APIs"],
        "threat_model": {
            "Spoofing": "Attackers impersonate users at presentation layer",
            "Tampering": "Data modified between layers without validation",
            "Information Disclosure": "Business logic leaks sensitive data to presentation layer",
            "Elevation of Privilege": "Business layer accessed directly, bypassing presentation auth",
        },
        "security_controls": ["Input validation at presentation layer", "Authorization checks at business layer", "Parameterized queries at data layer", "Layer-specific encryption", "Inter-layer authentication tokens"],
        "real_world": ["Django (Python)", "Spring MVC (Java)", "ASP.NET Core", "Ruby on Rails"],
        "diagram": """
┌─────────────────────────────┐
│   Presentation Layer        │ ← Input Validation, Auth UI
├─────────────────────────────┤
│   Business Logic Layer      │ ← Authorization, Business Rules
├─────────────────────────────┤
│   Data Access Layer         │ ← Parameterized Queries, ORM
├─────────────────────────────┤
│   Database Layer            │ ← Encryption at Rest, Access Control
└─────────────────────────────┘""",
    },
    {
        "id": "AP-002", "name": "Microservices Security Pattern",
        "icon": "🔬", "category": "Distributed", "colour": "#4ECDC4",
        "description": "Decomposes application into small, independently deployable services, each with its own security boundary, data store, and authentication.",
        "advantages": ["Independent security policies per service", "Blast radius containment on breach", "Independent scaling and deployment", "Technology flexibility per service"],
        "disadvantages": ["Complex inter-service authentication", "Network attack surface increases", "Distributed tracing complexity", "Secret sprawl risk"],
        "use_cases": ["Large-scale SaaS platforms", "Netflix-style streaming", "Banking microservices", "IoT platforms"],
        "threat_model": {
            "Spoofing": "Rogue service impersonating legitimate microservice",
            "Tampering": "Request modification between services",
            "Repudiation": "No centralized audit log across services",
            "Information Disclosure": "Service A accesses Service B's data store directly",
        },
        "security_controls": ["mTLS for all inter-service communication", "JWT service-to-service tokens", "API Gateway for external traffic", "Per-service RBAC", "Centralized secrets management (Vault)", "Distributed tracing with security events"],
        "real_world": ["Netflix", "Uber", "Amazon", "Spotify"],
        "diagram": """
Internet → [API Gateway] → [Auth Service]
                        ↓
           [Service A] [Service B] [Service C]
                ↓           ↓           ↓
           [DB-A]       [DB-B]      [DB-C]
           mTLS everywhere | JWT tokens | Vault secrets""",
    },
    {
        "id": "AP-003", "name": "Zero Trust Architecture",
        "icon": "🛡️", "category": "Security", "colour": "#FF6B6B",
        "description": "Eliminates implicit trust — every request is authenticated and authorized regardless of network location. 'Never Trust, Always Verify.'",
        "advantages": ["Eliminates perimeter-based trust", "Limits lateral movement", "Works for remote/hybrid workforce", "Reduces insider threat risk"],
        "disadvantages": ["Significant architecture change", "Performance overhead on verification", "Complex identity management", "Cultural resistance"],
        "use_cases": ["Remote workforce platforms", "Cloud-native apps", "Government/military systems", "Financial services"],
        "threat_model": {
            "Spoofing": "Mitigated by continuous identity verification",
            "Elevation of Privilege": "Mitigated by least-privilege access per request",
            "Information Disclosure": "Mitigated by micro-segmentation",
            "Tampering": "Mitigated by integrity verification on every request",
        },
        "security_controls": ["Multi-factor authentication everywhere", "Device health verification", "Just-in-time access provisioning", "Micro-segmentation", "Continuous monitoring and re-verification", "Encrypt all traffic regardless of location"],
        "real_world": ["Google BeyondCorp", "Microsoft Zero Trust", "Cloudflare Access", "Okta"],
        "diagram": """
Identity Provider (MFA)
        ↓
[Policy Engine] ← Device Health + Context
        ↓
[Policy Enforcement Point]
        ↓ (verified, minimal access)
[Resource] — every request re-evaluated""",
    },
    {
        "id": "AP-004", "name": "Secure MVC Pattern",
        "icon": "🎮", "category": "Structural", "colour": "#AB47BC",
        "description": "Model-View-Controller with security controls embedded at each layer: input validation in View, business rules in Controller, data integrity in Model.",
        "advantages": ["Security integrated into familiar MVC", "Clear responsibility assignment", "Testable security controls", "Framework support (Django, Spring)"],
        "disadvantages": ["Security can still be bypassed if developer skips checks", "No inherent defense-in-depth", "Fat controller anti-pattern risk"],
        "use_cases": ["Web applications", "Admin portals", "Content management systems"],
        "threat_model": {
            "Tampering": "View accepts unvalidated input → Controller processes malicious data",
            "Spoofing": "Controller skips authentication → Model accessed without auth",
            "Information Disclosure": "Model returns more data than View should display",
        },
        "security_controls": ["Input validation in View (whitelist)", "CSRF tokens in forms", "Authentication middleware in Controller", "Authorization at Controller level", "Output encoding in View templates", "Parameterized queries in Model"],
        "real_world": ["Django", "Ruby on Rails", "ASP.NET MVC", "Laravel"],
        "diagram": """
User → [View: Input Validation + CSRF + Output Encoding]
              ↓
       [Controller: Auth + Authz + Business Rules]
              ↓
       [Model: Parameterized Queries + Data Integrity]
              ↓
       [Database: Encryption at Rest]""",
    },
    {
        "id": "AP-005", "name": "Event-Driven Secure Architecture",
        "icon": "⚡", "category": "Distributed", "colour": "#FFEE58",
        "description": "Components communicate through secure, authenticated events via a message broker. Events are signed, encrypted, and audited.",
        "advantages": ["Decoupled services — reduced attack surface", "Immutable event log for audit trail", "Asynchronous — resilient to DoS", "Events signed for non-repudiation"],
        "disadvantages": ["Eventual consistency complicates security decisions", "Message broker becomes a high-value target", "Complex debugging", "Poison message attacks"],
        "use_cases": ["Financial transaction systems", "Audit-heavy compliance systems", "Real-time fraud detection", "IoT data pipelines"],
        "threat_model": {
            "Tampering": "Event payload modified in transit",
            "Repudiation": "Producer denies publishing event",
            "Spoofing": "Malicious producer injects fake events",
            "Denial of Service": "Event queue flooded with messages",
        },
        "security_controls": ["Event signing (HMAC/digital signature)", "Event encryption in transit and at rest", "Producer authentication (mTLS/OAuth)", "Consumer authorization (topic-level ACLs)", "Dead letter queue for suspicious events", "Rate limiting on event publication"],
        "real_world": ["Apache Kafka with TLS+SASL", "AWS EventBridge", "Azure Event Hub", "Google Pub/Sub"],
        "diagram": """
[Producer A] →(signed+encrypted event)→ [Message Broker]
[Producer B] →                                    ↓
                                     [Consumer A] [Consumer B]
                                     (verify signature → process)
                                     ↓
                              [Immutable Audit Log]""",
    },
    {
        "id": "AP-006", "name": "Defense in Depth",
        "icon": "🏰", "category": "Security", "colour": "#FF8C00",
        "description": "Multiple independent security layers — if one fails, others continue to protect. Based on military 'castle defense' concept.",
        "advantages": ["No single point of security failure", "Attacker must breach multiple layers", "Slows attackers, increases detection time", "Regulatory compliance friendly"],
        "disadvantages": ["Higher cost and complexity", "Potential for false sense of security", "Performance overhead of multiple checks"],
        "use_cases": ["Banking systems", "Healthcare platforms", "Government systems", "Critical infrastructure"],
        "threat_model": {
            "All STRIDE": "Each layer addresses different threat categories independently",
        },
        "security_controls": ["Perimeter firewall (Layer 1)", "WAF — Web Application Firewall (Layer 2)", "API Gateway with rate limiting (Layer 3)", "Application-level authentication (Layer 4)", "Business logic authorization (Layer 5)", "Database access control (Layer 6)", "Encryption at rest (Layer 7)", "Monitoring & alerting (Layer 8)"],
        "real_world": ["PCI-DSS compliant systems", "HIPAA healthcare platforms", "Military/government portals"],
        "diagram": """
Internet
   ↓ [Firewall / DDoS Protection]
   ↓ [WAF — OWASP Rules]
   ↓ [API Gateway — Rate Limiting + Auth]
   ↓ [Application — RBAC + Input Validation]
   ↓ [Service Layer — Business Rules]
   ↓ [Database — Parameterized + Encrypted]
   ↓ [Storage — AES-256 at Rest]
   + [SIEM — Monitoring All Layers]""",
    },
    {
        "id": "AP-007", "name": "Secure API Gateway Pattern",
        "icon": "🚪", "category": "Infrastructure", "colour": "#29B6F6",
        "description": "A centralized entry point that enforces authentication, rate limiting, input validation, logging, and SSL termination for all API traffic.",
        "advantages": ["Single enforcement point for security policies", "Consistent auth across all services", "Centralized rate limiting and DDoS protection", "Easy to audit and monitor"],
        "disadvantages": ["Single point of failure if not HA", "Potential bottleneck", "Complexity for simple apps"],
        "use_cases": ["Public APIs", "Mobile backends", "Third-party integrations", "Multi-tenant SaaS"],
        "threat_model": {
            "Spoofing": "Unauthenticated API calls → Gateway enforces JWT/API key",
            "Denial of Service": "API flooding → Gateway rate limiting",
            "Tampering": "Request modification → Gateway validates schemas",
            "Elevation of Privilege": "Direct backend access → Gateway is sole entry point",
        },
        "security_controls": ["JWT/OAuth 2.0 enforcement", "Rate limiting (per IP, per user, per endpoint)", "API key management", "Request schema validation", "SSL/TLS termination", "IP allowlisting/blocklisting", "Threat intelligence integration"],
        "real_world": ["Kong Gateway", "AWS API Gateway", "Azure API Management", "NGINX Plus"],
        "diagram": """
Client → HTTPS → [API Gateway]
                      ↓ (authenticated + rate-limited)
         [Service A] [Service B] [Service C]
         
Gateway handles: JWT validation, rate limiting,
SSL termination, logging, threat detection""",
    },
    {
        "id": "AP-008", "name": "Broker Security Pattern",
        "icon": "🔀", "category": "Distributed", "colour": "#00C853",
        "description": "A broker mediates between clients and servers, handling authentication, authorization, and routing. Clients never directly access servers.",
        "advantages": ["Decouples clients from servers", "Broker enforces all security policies", "Easy to add/remove servers transparently", "Single point for access control"],
        "disadvantages": ["Broker becomes high-value target", "Performance bottleneck risk", "Single point of failure"],
        "use_cases": ["Distributed systems", "Enterprise middleware", "Service directories", "Legacy integration"],
        "threat_model": {
            "Spoofing": "Client impersonates another client to broker",
            "Tampering": "Message modified before broker forwards",
            "Denial of Service": "Broker overwhelmed → all services down",
        },
        "security_controls": ["Client authentication at broker", "Message signing and verification", "Broker high availability (clustering)", "Encrypted broker-to-server channels", "ACL-based routing rules"],
        "real_world": ["Apache ActiveMQ", "RabbitMQ", "IBM MQ", "CORBA systems"],
        "diagram": """
[Client A] ──authenticated──→ [Security Broker]
[Client B] ──                         ↓ (routes + enforces ACL)
                         [Server A] [Server B] [Server C]""",
    },
    {
        "id": "AP-009", "name": "Service Mesh Security",
        "icon": "🕸️", "category": "Infrastructure", "colour": "#EF5350",
        "description": "Infrastructure layer that handles service-to-service communication with automatic mTLS, observability, and traffic policies.",
        "advantages": ["Automatic mTLS — no code changes needed", "Centralized policy management", "Fine-grained traffic control", "Built-in observability"],
        "disadvantages": ["Operational complexity", "Resource overhead (sidecar proxies)", "Steep learning curve"],
        "use_cases": ["Kubernetes microservices", "Cloud-native platforms", "Zero-trust implementations"],
        "threat_model": {
            "Spoofing": "Service identity automatically verified via mTLS certificates",
            "Tampering": "All traffic encrypted end-to-end between services",
            "Information Disclosure": "Traffic policies prevent unauthorized service access",
        },
        "security_controls": ["Automatic mTLS certificate rotation", "L7 traffic policies (allow/deny per route)", "Circuit breaking", "Distributed tracing", "Envoy proxy security", "Certificate authority integration"],
        "real_world": ["Istio", "Linkerd", "Consul Connect", "AWS App Mesh"],
        "diagram": """
[Service A + Envoy Sidecar] ←mTLS→ [Service B + Envoy Sidecar]
         ↕ policy                           ↕ policy
[Control Plane: Istiod — certificate management + policies]""",
    },
    {
        "id": "AP-010", "name": "Secure Client-Server Architecture",
        "icon": "💻", "category": "Structural", "colour": "#FF6B35",
        "description": "Classic client-server model with explicit security at every communication layer: TLS, authentication, authorization, and input validation.",
        "advantages": ["Clear security boundary between client and server", "Well-understood trust model", "Simple to audit", "Wide tooling support"],
        "disadvantages": ["Server is the primary attack target", "Client trust is difficult to establish", "Thick clients increase attack surface"],
        "use_cases": ["Web applications", "Desktop applications", "Banking portals", "Enterprise apps"],
        "threat_model": {
            "Spoofing": "Client sends forged identity",
            "Tampering": "Request tampered in transit",
            "Repudiation": "Client denies actions",
            "Information Disclosure": "Server exposes excessive data",
        },
        "security_controls": ["TLS 1.3 for all communications", "Certificate pinning on mobile clients", "Server-side validation (never trust client)", "JWT/session token authentication", "CORS policy enforcement", "Security headers (HSTS, CSP, X-Frame-Options)"],
        "real_world": ["All web applications", "Banking mobile apps", "Enterprise portals"],
        "diagram": """
[Browser/Mobile Client]
   ↕ TLS 1.3 + Certificate Pinning
[Web Server — HTTPS + Security Headers]
   ↕ Internal Auth Token
[Application Server — Input Validation + RBAC]
   ↕ Parameterized SQL
[Database Server — Encrypted + Access Control]""",
    },
    {
        "id": "AP-011", "name": "CQRS Security Pattern",
        "icon": "✂️", "category": "Structural", "colour": "#26C6DA",
        "description": "Command Query Responsibility Segregation — separate read and write paths. Security policies applied independently to each, limiting blast radius.",
        "advantages": ["Read model can be highly restricted", "Write model fully audited", "Reduced attack surface per operation type", "Event sourcing provides natural audit log"],
        "disadvantages": ["Eventual consistency", "Increased complexity", "Data duplication", "Harder to reason about system state"],
        "use_cases": ["Financial systems", "Audit-heavy applications", "High-read/low-write systems", "E-commerce order processing"],
        "threat_model": {
            "Tampering": "Write commands validated strictly before processing",
            "Repudiation": "Event store provides immutable command history",
            "Information Disclosure": "Read model exposes only necessary fields per role",
            "Elevation of Privilege": "Command handler enforces strict authorization checks",
        },
        "security_controls": ["Command authorization (who can issue which commands)", "Query authorization (what data each role can read)", "Command validation (schema + business rules)", "Immutable event store (write-once audit)", "Separate credentials for read vs write stores", "Rate limiting on commands separately from queries"],
        "real_world": ["Event-sourced banking systems", "Microsoft Azure architecture", "Domain-driven design systems"],
        "diagram": """
[Client]
  ├→ Command → [Command Handler: strict authz + validate] → [Write Store] → [Event Store]
  └→ Query  → [Query Handler: read-only authz] → [Read Store (projection)]""",
    },
    {
        "id": "AP-012", "name": "Hexagonal Architecture Security",
        "icon": "⬡", "category": "Structural", "colour": "#7E57C2",
        "description": "Ports & Adapters — business logic is completely isolated from infrastructure. Security adapters can be swapped without touching core logic.",
        "advantages": ["Business logic unaffected by infrastructure security changes", "Easy to test security adapters independently", "Swap auth providers without changing core", "Clear boundaries prevent security logic leakage"],
        "disadvantages": ["More files and indirection", "Steeper learning curve", "Overkill for simple applications"],
        "use_cases": ["Complex domain applications", "Systems requiring multiple auth providers", "Long-lived enterprise applications", "Systems with strict testability requirements"],
        "threat_model": {
            "All STRIDE": "Security adapters handle each threat at port boundaries",
            "Elevation of Privilege": "Core domain has no knowledge of infrastructure — can't be manipulated via infra attacks",
        },
        "security_controls": ["Security adapters at all ports (REST, DB, messaging)", "Domain model contains no auth/infra code", "Each adapter independently auditable", "Dependency injection for security services", "Port-level input validation", "Separate security adapter test suite"],
        "real_world": ["Domain-driven design implementations", "Spring Hexagonal (Java)", "Clean Architecture (Uncle Bob)"],
        "diagram": """
         [REST Adapter: Auth+Validate] [GraphQL Adapter: Auth+Validate]
                      ↓                          ↓
               [Input Port (Interface)]
                      ↓
              [Core Domain Logic]  ← no infra, no security dependencies
                      ↓
               [Output Port (Interface)]
                      ↓
         [DB Adapter: Encrypted]   [Event Adapter: Signed]""",
    },
]


def show() -> None:
    inject_css()
    page_header("🏛️", "Architecture Pattern Library",
                "12 detailed security-centric architectural patterns with threat models and diagrams.")

    # Stats row
    cats = list({p["category"] for p in ARCH_PATTERNS})
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Patterns", len(ARCH_PATTERNS))
    m2.metric("Categories", len(cats))
    m3.metric("Security-First", sum(1 for p in ARCH_PATTERNS if p["category"] == "Security"))
    m4.metric("Structural", sum(1 for p in ARCH_PATTERNS if p["category"] == "Structural"))

    section_heading("Browse & Filter")
    f1, f2, f3 = st.columns(3)
    sel_cat = f1.selectbox("Category", ["All"] + sorted(cats))
    search  = f2.text_input("Search", placeholder="pattern name or keyword…")
    view_mode = f3.radio("View", ["Cards", "Detailed"], horizontal=True)

    filtered = ARCH_PATTERNS
    if sel_cat != "All":
        filtered = [p for p in filtered if p["category"] == sel_cat]
    if search:
        s = search.lower()
        filtered = [p for p in filtered if
                    s in p["name"].lower() or s in p["description"].lower() or
                    any(s in uc.lower() for uc in p["use_cases"])]

    st.markdown(f"**Showing {len(filtered)} of {len(ARCH_PATTERNS)} patterns**")
    st.markdown("<br>", unsafe_allow_html=True)

    if view_mode == "Cards":
        # Grid of cards — 2 per row
        for i in range(0, len(filtered), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j >= len(filtered):
                    break
                p = filtered[i + j]
                with col:
                    adv_list = "".join(f"<li style='color:#9ca3af;font-size:0.8rem;'>{a}</li>"
                                       for a in p["advantages"][:3])
                    st.markdown(f"""
<div style="background:linear-gradient(135deg,#161b22,#1a2332);
            border:1px solid {p['colour']}44; border-top:3px solid {p['colour']};
            border-radius:14px; padding:20px; margin-bottom:16px;
            box-shadow: 0 4px 20px {p['colour']}11;">
  <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
    <span style="font-size:1.8rem;">{p['icon']}</span>
    <div>
      <div style="color:{p['colour']}; font-weight:800; font-size:0.95rem;">{p['name']}</div>
      <div style="color:#6b7280; font-size:0.75rem;">{p['id']} · {p['category']}</div>
    </div>
  </div>
  <p style="color:#9ca3af; font-size:0.82rem; line-height:1.5; margin:0 0 10px 0;">{p['description'][:120]}…</p>
  <div style="color:#6b7280; font-size:0.75rem; font-weight:600; text-transform:uppercase; margin-bottom:6px;">Key Advantages</div>
  <ul style="padding-left:14px; margin:0;">{adv_list}</ul>
</div>
""", unsafe_allow_html=True)
                    if st.button(f"View Details — {p['name']}", key=f"detail_{p['id']}",
                                 use_container_width=True):
                        st.session_state[f"show_pattern_{p['id']}"] = True

    else:  # Detailed view
        for p in filtered:
            col_icon = p["colour"]
            with st.expander(f"{p['icon']} **{p['name']}** — {p['category']}", expanded=False):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**ID:** `{p['id']}`")
                c2.markdown(f"**Category:** {p['category']}")
                c3.markdown(f"**Colour:** <span style='color:{col_icon}'>●</span> {col_icon}",
                            unsafe_allow_html=True)

                st.markdown(f"**Description:** {p['description']}")
                st.markdown("<br>", unsafe_allow_html=True)

                t1, t2, t3, t4, t5 = st.tabs(
                    ["⚖️ Pros & Cons", "📋 Use Cases", "🎯 Threat Model", "🛡️ Security Controls", "💻 Diagram"])

                with t1:
                    ca, cd = st.columns(2)
                    with ca:
                        st.markdown("**✅ Advantages**")
                        for a in p["advantages"]:
                            st.markdown(f"• {a}")
                    with cd:
                        st.markdown("**⚠️ Disadvantages**")
                        for d in p["disadvantages"]:
                            st.markdown(f"• {d}")

                with t2:
                    st.markdown("**🏭 Real-World Examples**")
                    for rw in p["real_world"]:
                        st.markdown(f"• {rw}")
                    st.markdown("**📋 Ideal Use Cases**")
                    for uc in p["use_cases"]:
                        st.markdown(f"• {uc}")

                with t3:
                    st.markdown("**STRIDE Threats for this Pattern:**")
                    stride_colours = {
                        "Spoofing": "#FF6B6B", "Tampering": "#FFA726",
                        "Repudiation": "#FFEE58", "Information Disclosure": "#AB47BC",
                        "InformationDisclosure": "#AB47BC",
                        "Denial of Service": "#29B6F6", "DenialOfService": "#29B6F6",
                        "Elevation of Privilege": "#EF5350", "ElevationOfPrivilege": "#EF5350",
                        "All STRIDE": "#FF2D2D",
                    }
                    for threat, detail in p["threat_model"].items():
                        colour = stride_colours.get(threat, "#74B9FF")
                        st.markdown(f"""
<div style="background:#161b22; border-left:3px solid {colour};
            padding:8px 12px; margin:6px 0; border-radius:0 8px 8px 0;">
  <span style="color:{colour}; font-weight:700; font-size:0.85rem;">{threat}</span><br>
  <span style="color:#9ca3af; font-size:0.82rem;">{detail}</span>
</div>
""", unsafe_allow_html=True)

                with t4:
                    for ctrl in p["security_controls"]:
                        st.markdown(f"🔒 {ctrl}")

                with t5:
                    st.code(p["diagram"], language="text")

    # Category summary table
    st.markdown("<br>", unsafe_allow_html=True)
    section_heading("Category Summary")
    import pandas as pd
    cat_rows = []
    for cat in sorted(set(p["category"] for p in ARCH_PATTERNS)):
        ps = [p for p in ARCH_PATTERNS if p["category"] == cat]
        cat_rows.append({
            "Category": cat,
            "Count": len(ps),
            "Patterns": ", ".join(p["name"] for p in ps),
        })
    st.dataframe(pd.DataFrame(cat_rows), use_container_width=True, hide_index=True)
