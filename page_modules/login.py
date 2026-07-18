"""
User Login / Registration system — session-based with hashed passwords.
Simple but functional auth without external dependencies.
"""
from __future__ import annotations
import hashlib
import hmac
import os
import sqlite3
import secrets
from pathlib import Path
from typing import Optional, Tuple
import streamlit as st
from page_modules.shared_styles import inject_css

DB_PATH = Path("database/users.db")

# ── DB layer ──────────────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_user_db() -> None:
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                username     TEXT UNIQUE NOT NULL,
                email        TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt         TEXT NOT NULL,
                role         TEXT DEFAULT 'student',
                full_name    TEXT DEFAULT '',
                created_at   TEXT DEFAULT (datetime('now')),
                last_login   TEXT
            )
        """)
        conn.commit()
        # Seed demo users if table is empty
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            _seed_demo_users(conn)


def _hash_password(password: str, salt: str) -> str:
    key = (password + salt).encode("utf-8")
    return hashlib.sha256(key).hexdigest()


def _seed_demo_users(conn: sqlite3.Connection) -> None:
    demo_users = [
        ("admin", "admin@example.com", "Admin@123", "admin", "Administrator"),
        ("student1", "student1@example.com", "Student@123", "student", "Alice Johnson"),
        ("faculty1", "faculty@example.com", "Faculty@123", "faculty", "Prof. Smith"),
    ]
    for uname, email, pwd, role, name in demo_users:
        salt = secrets.token_hex(16)
        ph = _hash_password(pwd, salt)
        conn.execute(
            "INSERT INTO users (username, email, password_hash, salt, role, full_name) VALUES (?,?,?,?,?,?)",
            (uname, email, ph, salt, role, name)
        )
    conn.commit()


def authenticate(username: str, password: str) -> Optional[dict]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    if not row:
        return None
    expected = _hash_password(password, row["salt"])
    if not hmac.compare_digest(expected, row["password_hash"]):
        return None
    with _get_conn() as conn:
        conn.execute("UPDATE users SET last_login = datetime('now') WHERE id = ?", (row["id"],))
        conn.commit()
    return dict(row)


def register_user(username: str, email: str, password: str,
                  full_name: str, role: str = "student") -> Tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    try:
        salt = secrets.token_hex(16)
        ph = _hash_password(password, salt)
        with _get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, salt, role, full_name) VALUES (?,?,?,?,?,?)",
                (username, email, ph, salt, role, full_name)
            )
            conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already taken."
        return False, "Email already registered."
    except Exception as e:
        return False, f"Registration failed: {e}"


# ── Session helpers ───────────────────────────────────────────────────────────

def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)


def current_user() -> Optional[dict]:
    return st.session_state.get("user_info")


def logout() -> None:
    for key in ["logged_in", "user_info"]:
        st.session_state.pop(key, None)


# ── UI ────────────────────────────────────────────────────────────────────────

def show() -> None:
    inject_css()
    init_user_db()

    if is_logged_in():
        _show_profile()
        return

    st.markdown("""
<style>
.login-card {
    background: linear-gradient(135deg, rgba(15,52,96,0.95) 0%, rgba(22,33,62,0.98) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 20px;
    padding: 36px 40px;
    max-width: 480px;
    margin: 0 auto;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,212,255,0.05);
}
.login-logo { font-size: 3rem; text-align: center; margin-bottom: 8px; }
.login-title { color: #00D4FF; font-size: 1.6rem; font-weight: 800; text-align: center; margin-bottom: 4px; }
.login-sub { color: #9ca3af; font-size: 0.9rem; text-align: center; margin-bottom: 24px; }
</style>
""", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown('<div class="login-logo">🔐</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Security Architecture Framework</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Sign in to access all features</div>', unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔑 Sign In", "📝 Register"])

        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    user = authenticate(username, password)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["user_info"] = user
                        st.success(f"Welcome back, {user['full_name'] or user['username']}! 🎉")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

            # Demo accounts info
            st.markdown("""
<div style="background:#161b22; border:1px solid #30363d; border-radius:10px;
            padding:14px; margin-top:16px;">
  <div style="color:#00D4FF; font-weight:700; font-size:0.85rem; margin-bottom:8px;">
    🧪 Demo Accounts
  </div>
  <div style="color:#9ca3af; font-size:0.82rem; line-height:1.8;">
    👑 Admin: <code>admin</code> / <code>Admin@123</code><br>
    🎓 Student: <code>student1</code> / <code>Student@123</code><br>
    👨‍🏫 Faculty: <code>faculty1</code> / <code>Faculty@123</code>
  </div>
</div>
""", unsafe_allow_html=True)

        with tab_register:
            with st.form("register_form"):
                full_name = st.text_input("Full Name", placeholder="Your full name")
                reg_email = st.text_input("Email", placeholder="your@email.com")
                reg_user  = st.text_input("Username", placeholder="Choose a username")
                reg_pass  = st.text_input("Password", type="password",
                                          placeholder="Min 8 characters")
                reg_pass2 = st.text_input("Confirm Password", type="password",
                                          placeholder="Repeat your password")
                reg_role  = st.selectbox("Role", ["student", "faculty"])
                reg_submit = st.form_submit_button("Create Account", use_container_width=True,
                                                   type="primary")

            if reg_submit:
                if reg_pass != reg_pass2:
                    st.error("Passwords do not match.")
                elif not all([full_name, reg_email, reg_user, reg_pass]):
                    st.error("All fields are required.")
                else:
                    ok, msg = register_user(reg_user, reg_email, reg_pass, full_name, reg_role)
                    if ok:
                        st.success(msg + " You can now sign in.")
                    else:
                        st.error(msg)


def _show_profile() -> None:
    from page_modules.shared_styles import page_header, section_heading
    page_header("👤", "My Profile", "Your account information and activity.")

    user = current_user()
    if not user:
        return

    role_colour = {"admin": "#FF2D2D", "faculty": "#FF8C00", "student": "#00C853"}.get(
        user.get("role", "student"), "#74B9FF")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f3460,#16213e);
            border:1px solid #1e3a5f; border-radius:16px; padding:24px; text-align:center;">
  <div style="font-size:4rem; margin-bottom:12px;">👤</div>
  <div style="color:#00D4FF; font-weight:800; font-size:1.2rem;">
    {user.get('full_name') or user['username']}
  </div>
  <div style="background:{role_colour}22; color:{role_colour}; border:1px solid {role_colour};
              padding:4px 16px; border-radius:20px; font-size:0.8rem; font-weight:700;
              margin-top:8px; display:inline-block; text-transform:uppercase;">
    {user.get('role', 'student')}
  </div>
</div>
""", unsafe_allow_html=True)

    with c2:
        section_heading("Account Details")
        details = [
            ("Username", user.get("username", "—")),
            ("Email", user.get("email", "—")),
            ("Full Name", user.get("full_name") or "—"),
            ("Role", user.get("role", "student").title()),
            ("Member Since", user.get("created_at", "—")[:10] if user.get("created_at") else "—"),
            ("Last Login", user.get("last_login", "—")[:16].replace("T", " ") if user.get("last_login") else "—"),
        ]
        for label, value in details:
            st.markdown(f"**{label}:** {value}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Sign Out", type="secondary"):
        logout()
        st.rerun()
