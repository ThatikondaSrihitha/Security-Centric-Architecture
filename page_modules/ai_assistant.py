"""
AI Assistant page — powered by Groq (free tier) with demo/mock fallback.
Supports: pattern explanations, threat analysis chat, architecture recommendations.
"""
from __future__ import annotations
import json
import os
import time
from typing import List, Dict, Any

import streamlit as st
from page_modules.shared_styles import inject_css, page_header, section_heading

# ── AI Backend (Groq preferred, mock fallback) ────────────────────────────────

def _groq_available() -> bool:
    try:
        api_key = st.session_state.get("groq_api_key") or os.environ.get("GROQ_API_KEY", "")
        return bool(api_key and api_key.strip())
    except Exception:
        return False


def _call_groq(messages: List[Dict], api_key: str) -> str:
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except ImportError:
        return _mock_response(messages[-1]["content"] if messages else "")
    except Exception as e:
        return f"⚠️ API error: {e}\n\n{_mock_response(messages[-1]['content'] if messages else '')}"


def _mock_response(user_input: str) -> str:
    """Intelligent mock responses for demo mode."""
    q = user_input.lower()

    if any(w in q for w in ["zero trust", "zero-trust"]):
        return """## Zero Trust Architecture

**Core Principle:** "Never trust, always verify" — every request is authenticated regardless of network location.

### Key Components:
1. **Identity Verification** — Multi-factor authentication for all users and services
2. **Micro-segmentation** — Network divided into small zones; lateral movement is blocked
3. **Least Privilege Access** — Users/services get only the minimum permissions needed
4. **Continuous Monitoring** — All traffic inspected in real-time

### Security Controls:
- Strong IAM (Identity & Access Management)
- End-to-end encryption (TLS 1.3+)
- Device health verification
- Just-in-time access provisioning

### Use Cases:
- Remote workforce security
- Cloud-native applications
- Hybrid environments

### Threats Mitigated:
- Insider threats
- Lateral movement attacks
- Credential theft exploitation

> **Example:** Google's BeyondCorp model eliminated VPN dependency by implementing Zero Trust for all internal services."""

    elif any(w in q for w in ["microservice", "microservices"]):
        return """## Microservices Security Pattern

**Overview:** Securing distributed services that communicate over networks.

### Key Security Challenges:
1. **Service-to-Service Authentication** — Each service must verify caller identity
2. **API Gateway Security** — Single entry point for auth, rate limiting, WAF
3. **Secrets Management** — No hardcoded credentials; use Vault or AWS Secrets Manager
4. **Network Policies** — Control which services can communicate

### Security Controls:
| Control | Implementation |
|---------|----------------|
| Auth | JWT / mTLS between services |
| Encryption | TLS on all inter-service calls |
| Access Control | RBAC at API Gateway + service level |
| Logging | Centralized with correlation IDs |

### STRIDE Threats in Microservices:
- **Spoofing** — A malicious service impersonates a legitimate one
- **Tampering** — Request modification between services
- **Information Disclosure** — Service A accessing Service B's data it shouldn't

### Best Practice:
Use a **Service Mesh** (Istio, Linkerd) to automatically handle mTLS, observability, and traffic policies."""

    elif any(w in q for w in ["stride", "threat model"]):
        return """## STRIDE Threat Modeling

STRIDE is a systematic framework for identifying security threats:

| Letter | Threat | Example | Mitigation |
|--------|--------|---------|------------|
| **S** | Spoofing | Fake login with stolen creds | MFA, strong auth |
| **T** | Tampering | Modifying API request payload | Input validation, HMAC |
| **R** | Repudiation | Denying a transaction occurred | Audit logs, digital signatures |
| **I** | Info Disclosure | Leaking PII via error messages | Error handling, encryption |
| **D** | Denial of Service | Flooding API with requests | Rate limiting, WAF |
| **E** | Elevation of Privilege | Regular user accessing admin | RBAC, least privilege |

### How to Apply STRIDE:
1. Draw a Data Flow Diagram (DFD)
2. For each element, ask: "Can it be Spoofed/Tampered/etc.?"
3. Rate each threat by likelihood and impact
4. Define mitigations
5. Verify mitigations are implemented

### Risk Formula:
`Risk Score = Likelihood (1-5) × Impact (1-5)`"""

    elif any(w in q for w in ["owasp", "top 10", "vulnerability"]):
        return """## OWASP Top 10 — 2021

The most critical web application security risks:

1. **A01 — Broken Access Control** 🔴 Critical
   - Users acting outside their permissions
   - Fix: RBAC, deny by default, validate on server

2. **A02 — Cryptographic Failures** 🔴 Critical
   - Weak encryption, plaintext sensitive data
   - Fix: TLS everywhere, strong algorithms (AES-256)

3. **A03 — Injection** 🔴 Critical
   - SQL, NoSQL, command injection
   - Fix: Parameterized queries, input validation

4. **A04 — Insecure Design** 🟠 High
   - Missing security controls by design
   - Fix: Threat modeling, secure design patterns

5. **A05 — Security Misconfiguration** 🟠 High
   - Default configs, unnecessary features enabled
   - Fix: Hardening guides, automated config checks

6. **A06 — Vulnerable Components** 🟠 High
   - Outdated dependencies with known CVEs
   - Fix: SCA tools (Snyk, Dependabot)

7. **A07 — Auth Failures** 🟠 High
   - Weak passwords, no MFA, session issues
   - Fix: Strong auth, session management

8. **A08 — Data Integrity Failures** 🟡 Medium
   - Insecure deserialization, unsigned updates
   - Fix: Digital signatures, integrity checks

9. **A09 — Security Logging Failures** 🟡 Medium
   - No audit trails, unmonitored logs
   - Fix: Centralized logging, alerting

10. **A10 — SSRF** 🟡 Medium
    - Server fetching attacker-controlled URLs
    - Fix: Allowlist outbound requests"""

    elif any(w in q for w in ["recommend", "suggest", "which pattern", "what pattern"]):
        return """## Architecture Pattern Recommendations

Based on your query, here are my recommendations:

### For a Web Application:
1. **Layered Architecture** — Clear separation (Presentation → Business → Data)
2. **Secure API Gateway** — Centralize auth, rate limiting, SSL termination
3. **Input Validation Pattern** — Validate at every layer boundary

### For Microservices:
1. **Service Mesh Security** — Istio for automatic mTLS
2. **Zero Trust Architecture** — Never trust network location
3. **CQRS** — Separate read/write to limit blast radius

### For High Security (Banking/Healthcare):
1. **Defense in Depth** — Multiple independent security layers
2. **Hexagonal Architecture** — Isolate business logic from infrastructure
3. **Event-Driven with Audit Trail** — Immutable event log for compliance

### Quick Decision Guide:
| Scenario | Recommended Pattern |
|----------|---------------------|
| Simple web app | Layered + Secure MVC |
| API-first | API Gateway + Zero Trust |
| Complex domain | Hexagonal + CQRS |
| IoT/Real-time | Event-Driven Secure |
| Enterprise | Defense in Depth + Zero Trust |"""

    elif any(w in q for w in ["dread", "risk score", "risk rating"]):
        return """## DREAD Risk Scoring

DREAD is a quantitative risk scoring methodology:

| Letter | Factor | Question | Scale |
|--------|--------|----------|-------|
| **D** | Damage | How bad is the damage if exploited? | 0-10 |
| **R** | Reproducibility | How easy to reproduce? | 0-10 |
| **E** | Exploitability | How easy to exploit? | 0-10 |
| **A** | Affected Users | How many users affected? | 0-10 |
| **D** | Discoverability | How easy to discover? | 0-10 |

### DREAD Score = (D + R + E + A + D) / 5

### Classification:
- **0-3**: Low Risk 🟢
- **4-6**: Medium Risk 🟡  
- **7-9**: High Risk 🟠
- **10**: Critical Risk 🔴

### Example — SQL Injection:
- Damage: 9 (full DB compromise)
- Reproducibility: 8 (easy to repeat)
- Exploitability: 7 (tools available)
- Affected Users: 10 (all users)
- Discoverability: 6 (scanners detect it)
- **DREAD Score: 8.0 — HIGH RISK**"""

    elif any(w in q for w in ["hello", "hi", "hey", "help"]):
        return """## Welcome to the AI Security Assistant! 🤖

I'm your intelligent security architecture mentor. I can help you with:

### 🎯 What I Can Explain:
- **Security Patterns** — Zero Trust, Microservices, CQRS, Hexagonal, Defense in Depth, etc.
- **Threat Modeling** — STRIDE, DREAD, Attack Trees, OWASP Top 10
- **Architecture Recommendations** — Best patterns for your use case
- **Security Controls** — Authentication, encryption, access control
- **Secure Coding** — Common vulnerabilities and fixes

### 💬 Try Asking Me:
- *"Explain Zero Trust Architecture"*
- *"What is STRIDE threat modeling?"*
- *"Recommend a pattern for a banking app"*
- *"How does DREAD risk scoring work?"*
- *"What are the OWASP Top 10?"*
- *"How do I secure microservices?"*

> **Tip:** Connect a Groq API key (free at console.groq.com) in the sidebar settings for full AI responses!"""

    else:
        return f"""## AI Security Architecture Response

Thank you for your question about: *"{user_input[:100]}"*

Here's what I can tell you about security architecture:

### General Security Principles:

**1. Security by Design**
- Integrate security from the start, not as an afterthought
- Use threat modeling (STRIDE/DREAD) during design phase
- Apply the principle of least privilege everywhere

**2. Defense in Depth**
- Never rely on a single security control
- Layer multiple independent defenses
- Assume breach mentality — what if the outer layer fails?

**3. Zero Trust**
- Verify every request, regardless of origin
- "Never trust, always verify"
- Micro-segment your network

**4. Secure Architecture Patterns**
- Layered Architecture for clear security boundaries
- API Gateway for centralized access control
- Service Mesh for automatic encryption between services

### Recommended Next Steps:
1. Run a STRIDE threat model on your architecture
2. Map threats to OWASP Top 10
3. Apply appropriate security patterns
4. Calculate DREAD risk scores for prioritization

> **Note:** For more specific answers, try asking about a specific pattern, threat type, or architecture. Or connect a Groq API key for full AI responses!"""


# ── Quick actions ─────────────────────────────────────────────────────────────

_QUICK_PROMPTS = [
    ("🔐", "Explain Zero Trust Architecture"),
    ("🎯", "How does STRIDE threat modeling work?"),
    ("🦠", "What are the OWASP Top 10 vulnerabilities?"),
    ("🔗", "How to secure microservices communication?"),
    ("📊", "Explain DREAD risk scoring"),
    ("🏗️", "Recommend pattern for a banking application"),
    ("🛡️", "What is Defense in Depth?"),
    ("⚙️", "How does CQRS improve security?"),
]


# ── Main page ─────────────────────────────────────────────────────────────────

def show() -> None:
    inject_css()

    # Glassmorphism header
    st.markdown("""
<style>
.ai-hero {
    background: linear-gradient(135deg, rgba(15,52,96,0.9) 0%, rgba(22,33,62,0.95) 50%, rgba(13,17,23,1) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 8px 40px rgba(0,212,255,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
}
.ai-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0,212,255,0.04) 0%, transparent 60%);
    animation: pulse 4s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}
.chat-bubble-user {
    background: linear-gradient(135deg, #0f3460, #1e5f99);
    border: 1px solid #1e3a5f;
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin: 8px 0 8px 20%;
    color: #e5e7eb;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.chat-bubble-ai {
    background: linear-gradient(135deg, #161b22, #1a2332);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 16px 16px 16px 4px;
    padding: 16px 20px;
    margin: 8px 20% 8px 0;
    color: #e5e7eb;
    font-size: 0.92rem;
    line-height: 1.7;
    box-shadow: 0 4px 20px rgba(0,212,255,0.08), inset 0 1px 0 rgba(0,212,255,0.05);
}
.quick-btn {
    background: linear-gradient(135deg, rgba(15,52,96,0.6), rgba(30,95,153,0.4));
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 10px;
    padding: 10px 14px;
    color: #9ca3af;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
    backdrop-filter: blur(10px);
}
</style>

<div class="ai-hero">
  <div style="display:flex; align-items:center; gap:16px;">
    <div style="font-size:3rem;">🤖</div>
    <div>
      <h1 style="color:#00D4FF; font-size:1.8rem; font-weight:800; margin:0 0 6px 0;">
        AI Security Architecture Assistant
      </h1>
      <p style="color:#9ca3af; margin:0; font-size:0.95rem;">
        Powered by Groq LLaMA 3 · Explains patterns · Recommends architectures · Analyzes threats
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Sidebar API key config ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔑 AI Configuration")
        api_key_input = st.text_input(
            "Groq API Key",
            value=st.session_state.get("groq_api_key", ""),
            type="password",
            help="Free at console.groq.com — get your key in 2 minutes",
            key="groq_key_input"
        )
        if api_key_input:
            st.session_state["groq_api_key"] = api_key_input

        if _groq_available():
            st.success("✅ Groq AI Connected")
        else:
            st.info("💡 Running in Demo Mode\nGet free key: console.groq.com")

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()

    # ── Initialize chat ────────────────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # ── Quick action buttons ───────────────────────────────────────────────
    section_heading("Quick Actions")
    cols = st.columns(4)
    for i, (icon, prompt) in enumerate(_QUICK_PROMPTS):
        with cols[i % 4]:
            if st.button(f"{icon} {prompt[:30]}…" if len(prompt) > 30 else f"{icon} {prompt}",
                         key=f"quick_{i}", use_container_width=True):
                st.session_state["chat_history"].append({"role": "user", "content": prompt})
                with st.spinner("🤖 Thinking..."):
                    if _groq_available():
                        api_key = st.session_state.get("groq_api_key", "")
                        system_msg = {
                            "role": "system",
                            "content": (
                                "You are an expert security architecture consultant and educator. "
                                "You specialize in STRIDE threat modeling, DREAD risk scoring, "
                                "secure architectural patterns (Zero Trust, Microservices, Layered, CQRS, "
                                "Hexagonal, Defense in Depth, API Gateway, Service Mesh, Event-Driven), "
                                "OWASP Top 10, and security best practices. "
                                "Provide clear, structured, educational responses with examples. "
                                "Use markdown formatting with headers, bullet points, and tables."
                            )
                        }
                        msgs = [system_msg] + [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state["chat_history"]
                        ]
                        response = _call_groq(msgs, api_key)
                    else:
                        response = _mock_response(prompt)
                st.session_state["chat_history"].append({"role": "assistant", "content": response})
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat history ──────────────────────────────────────────────────────
    section_heading("Conversation")

    if not st.session_state["chat_history"]:
        st.markdown("""
<div style="text-align:center; padding:40px 20px; background:#161b22; border:1px dashed #30363d; border-radius:16px;">
  <div style="font-size:3rem; margin-bottom:16px;">💬</div>
  <div style="color:#9ca3af; font-size:1rem;">
    Start a conversation by clicking a Quick Action above<br>or typing your question below.
  </div>
</div>
""", unsafe_allow_html=True)
    else:
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-bubble-user">👤 <b>You:</b> {msg["content"]}</div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble-ai">🤖 <b>AI Assistant:</b></div>',
                                unsafe_allow_html=True)
                    st.markdown(msg["content"])

    # ── Input box ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    section_heading("Ask a Question")

    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Your question",
            placeholder="e.g., 'Explain Zero Trust Architecture' or 'How to secure APIs?'",
            label_visibility="collapsed",
            key="chat_input"
        )
    with col_send:
        send_clicked = st.button("Send 🚀", type="primary", use_container_width=True)

    if send_clicked and user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("🤖 Generating response..."):
            if _groq_available():
                api_key = st.session_state.get("groq_api_key", "")
                system_msg = {
                    "role": "system",
                    "content": (
                        "You are an expert security architecture consultant and educator. "
                        "Specialize in STRIDE, DREAD, OWASP, secure patterns, threat modeling. "
                        "Give structured educational responses with markdown formatting."
                    )
                }
                msgs = [system_msg] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state["chat_history"]
                ]
                response = _call_groq(msgs, api_key)
            else:
                response = _mock_response(user_input.strip())
        st.session_state["chat_history"].append({"role": "assistant", "content": response})
        st.rerun()

    # ── Capabilities panel ────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    section_heading("AI Capabilities")
    c1, c2, c3 = st.columns(3)
    caps = [
        (c1, "🏗️", "#00D4FF", "Architecture Advisor",
         ["Explain 12+ security patterns", "Compare architectures", "Recommend for your use case",
          "Describe trade-offs"]),
        (c2, "🎯", "#FF8C00", "Threat Analyst",
         ["STRIDE threat explanation", "DREAD risk scoring", "OWASP Top 10 mapping",
          "Attack vector analysis"]),
        (c3, "📋", "#00C853", "Security Mentor",
         ["Secure coding guidance", "Mitigation strategies", "Best practice advice",
          "Real-world examples"]),
    ]
    for col, icon, colour, title, points in caps:
        with col:
            items_html = "".join(f"<li style='color:#9ca3af; font-size:0.82rem; margin:4px 0;'>{p}</li>"
                                  for p in points)
            st.markdown(f"""
<div style="background:#161b22; border:1px solid #30363d; border-top:3px solid {colour};
            border-radius:12px; padding:20px; height:200px;">
  <div style="font-size:1.8rem; margin-bottom:8px;">{icon}</div>
  <div style="color:{colour}; font-weight:700; font-size:0.9rem; margin-bottom:10px;">{title}</div>
  <ul style="padding-left:16px; margin:0;">{items_html}</ul>
</div>
""", unsafe_allow_html=True)
