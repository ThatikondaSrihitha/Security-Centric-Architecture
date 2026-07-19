"""
Adaptive Quiz Engine — security architecture quizzes with scoring and feedback.
"""
from __future__ import annotations
import random
import streamlit as st
from page_modules.shared_styles import inject_css, page_header, section_heading

QUESTION_BANK = [
    # STRIDE
    {
        "id": "Q001", "category": "STRIDE", "difficulty": "Easy",
        "question": "What does the 'S' in STRIDE stand for?",
        "options": ["Serialization", "Spoofing", "Scanning", "Sniffing"],
        "answer": "Spoofing",
        "explanation": "STRIDE: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.",
    },
    {
        "id": "Q002", "category": "STRIDE", "difficulty": "Easy",
        "question": "Which STRIDE category is addressed by implementing audit logging?",
        "options": ["Spoofing", "Tampering", "Repudiation", "Denial of Service"],
        "answer": "Repudiation",
        "explanation": "Repudiation threats involve denying having performed an action. Audit logs provide non-repudiation by creating tamper-resistant records.",
    },
    {
        "id": "Q003", "category": "STRIDE", "difficulty": "Medium",
        "question": "An attacker intercepts and modifies an unencrypted API request between services. Which STRIDE category is this?",
        "options": ["Spoofing", "Tampering", "Information Disclosure", "Elevation of Privilege"],
        "answer": "Tampering",
        "explanation": "Tampering involves unauthorized modification of data. An attacker modifying data in transit is a classic tampering attack, mitigated by TLS/encryption.",
    },
    {
        "id": "Q004", "category": "STRIDE", "difficulty": "Medium",
        "question": "A regular user exploits a missing authorization check to access admin functions. Which STRIDE category?",
        "options": ["Spoofing", "Repudiation", "Denial of Service", "Elevation of Privilege"],
        "answer": "Elevation of Privilege",
        "explanation": "EoP occurs when a user gains more access than authorized. Missing authorization checks directly enable privilege escalation.",
    },
    {
        "id": "Q005", "category": "STRIDE", "difficulty": "Hard",
        "question": "In STRIDE, which threat is mitigated by BOTH encryption in transit AND authentication?",
        "options": ["Spoofing only", "Tampering only", "Information Disclosure only", "Spoofing and Tampering"],
        "answer": "Spoofing and Tampering",
        "explanation": "Authentication prevents spoofing (impersonation). Encryption prevents tampering (modification in transit). Both controls working together are stronger than either alone.",
    },
    # DREAD
    {
        "id": "Q006", "category": "DREAD", "difficulty": "Easy",
        "question": "What does DREAD stand for?",
        "options": [
            "Damage, Reproducibility, Exploitability, Affected Users, Discoverability",
            "Detection, Response, Escalation, Analysis, Defense",
            "Data, Risk, Evaluation, Attack, Defense",
            "Damage, Risk, Exposure, Attack, Detection",
        ],
        "answer": "Damage, Reproducibility, Exploitability, Affected Users, Discoverability",
        "explanation": "DREAD is a risk scoring model: each factor scored 0-10, final score = average of all 5.",
    },
    {
        "id": "Q007", "category": "DREAD", "difficulty": "Medium",
        "question": "A SQL injection vulnerability has: Damage=9, Reproducibility=8, Exploitability=7, Affected Users=10, Discoverability=6. What is the DREAD score?",
        "options": ["7.5", "8.0", "8.5", "9.0"],
        "answer": "8.0",
        "explanation": "(9+8+7+10+6)/5 = 40/5 = 8.0. This is a HIGH risk score requiring immediate remediation.",
    },
    {
        "id": "Q008", "category": "DREAD", "difficulty": "Medium",
        "question": "A DREAD score of 3.5 would be classified as which risk level?",
        "options": ["Critical", "High", "Medium", "Low"],
        "answer": "Low",
        "explanation": "DREAD classification: 0-3 = Low, 4-6 = Medium, 7-9 = High, 10 = Critical. Score 3.5 falls in Low range.",
    },
    # Architecture Patterns
    {
        "id": "Q009", "category": "Architecture", "difficulty": "Easy",
        "question": "Which architectural pattern is based on 'Never Trust, Always Verify'?",
        "options": ["Layered Architecture", "Zero Trust Architecture", "Microservices", "Event-Driven"],
        "answer": "Zero Trust Architecture",
        "explanation": "Zero Trust Architecture eliminates implicit trust. Every request is verified regardless of network location — even internal requests.",
    },
    {
        "id": "Q010", "category": "Architecture", "difficulty": "Easy",
        "question": "What is the primary security benefit of the CQRS pattern?",
        "options": [
            "Faster performance",
            "Separate security policies for read and write operations",
            "Easier testing",
            "Reduced code complexity",
        ],
        "answer": "Separate security policies for read and write operations",
        "explanation": "CQRS separates read (Query) and write (Command) paths, allowing different security controls, permissions, and audit trails for each.",
    },
    {
        "id": "Q011", "category": "Architecture", "difficulty": "Medium",
        "question": "In Hexagonal Architecture, where should security controls (authentication, validation) be placed?",
        "options": [
            "In the core domain logic",
            "In the database layer only",
            "In the adapters at port boundaries",
            "In a separate security service",
        ],
        "answer": "In the adapters at port boundaries",
        "explanation": "Hexagonal Architecture places security in adapters (ports), keeping the core domain pure business logic. This makes security independently testable and swappable.",
    },
    {
        "id": "Q012", "category": "Architecture", "difficulty": "Hard",
        "question": "Which pattern is BEST for limiting blast radius when one microservice is compromised?",
        "options": ["Layered Architecture", "Service Mesh with mTLS + micro-segmentation", "Monolithic with Defense in Depth", "Broker Pattern"],
        "answer": "Service Mesh with mTLS + micro-segmentation",
        "explanation": "Service Mesh provides automatic mTLS between services and fine-grained traffic policies. Micro-segmentation prevents lateral movement — if Service A is breached, it cannot reach Service B unless explicitly allowed.",
    },
    # OWASP
    {
        "id": "Q013", "category": "OWASP", "difficulty": "Easy",
        "question": "What is the #1 vulnerability in OWASP Top 10 2021?",
        "options": ["Injection", "Broken Authentication", "Broken Access Control", "Security Misconfiguration"],
        "answer": "Broken Access Control",
        "explanation": "A01:2021 Broken Access Control moved to #1 in the 2021 update, up from #5 in 2017. 94% of apps tested had some form of broken access control.",
    },
    {
        "id": "Q014", "category": "OWASP", "difficulty": "Medium",
        "question": "A developer stores a user's uploaded filename directly in a database query. Which OWASP category is most at risk?",
        "options": ["A02 Cryptographic Failures", "A03 Injection", "A05 Security Misconfiguration", "A10 SSRF"],
        "answer": "A03 Injection",
        "explanation": "Unsanitized user input used directly in queries enables injection attacks. A03:2021 Injection covers SQL, NoSQL, OS command, and other injection types.",
    },
    {
        "id": "Q015", "category": "OWASP", "difficulty": "Hard",
        "question": "Which OWASP Top 10 category covers the risk of using a component with a known vulnerability (e.g., Log4j)?",
        "options": ["A02 Cryptographic Failures", "A05 Security Misconfiguration", "A06 Vulnerable and Outdated Components", "A08 Software Integrity Failures"],
        "answer": "A06 Vulnerable and Outdated Components",
        "explanation": "A06:2021 specifically addresses using components (libraries, frameworks, OS) with known vulnerabilities. Log4Shell (Log4j) is a prime example.",
    },
    # Secure Coding
    {
        "id": "Q016", "category": "Secure Coding", "difficulty": "Easy",
        "question": "What is the safest way to store user passwords?",
        "options": ["MD5 hash", "SHA-256 hash", "bcrypt or Argon2id", "AES encryption"],
        "answer": "bcrypt or Argon2id",
        "explanation": "bcrypt and Argon2id are slow password-hashing algorithms with built-in salting, designed to resist brute-force attacks. MD5/SHA-256 are fast hashes not suitable for passwords.",
    },
    {
        "id": "Q017", "category": "Secure Coding", "difficulty": "Medium",
        "question": "What is the primary defense against SQL injection?",
        "options": ["Input length validation", "Parameterized queries / prepared statements", "HTML encoding", "HTTPS"],
        "answer": "Parameterized queries / prepared statements",
        "explanation": "Parameterized queries separate SQL code from data. User input is treated as data, never as executable SQL — this completely prevents SQL injection.",
    },
    {
        "id": "Q018", "category": "Secure Coding", "difficulty": "Hard",
        "question": "A JWT token uses the 'none' algorithm. What is the security implication?",
        "options": [
            "The token is compressed",
            "The token signature is skipped — anyone can forge a valid token",
            "The token uses the strongest available algorithm",
            "The token is encrypted",
        ],
        "answer": "The token signature is skipped — anyone can forge a valid token",
        "explanation": "The 'none' algorithm removes signature verification. Attackers can modify JWT payload (e.g., set admin=true) and the server will accept it. Always whitelist specific algorithms (HS256, RS256).",
    },
    # Risk & Security Concepts
    {
        "id": "Q019", "category": "Risk", "difficulty": "Easy",
        "question": "Using the formula Risk = Likelihood × Impact, what is the risk score for Likelihood=4, Impact=5?",
        "options": ["9", "20", "25", "1"],
        "answer": "20",
        "explanation": "Risk Score = 4 × 5 = 20. On a scale of 1-25, this would be classified as Critical (17-25).",
    },
    {
        "id": "Q020", "category": "Risk", "difficulty": "Medium",
        "question": "What does 'Defense in Depth' mean in security architecture?",
        "options": [
            "Using the deepest encryption available",
            "Multiple independent security layers so failure of one doesn't compromise the system",
            "Defending against the most complex attacks",
            "A single strong perimeter defense",
        ],
        "answer": "Multiple independent security layers so failure of one doesn't compromise the system",
        "explanation": "Defense in Depth applies multiple independent security controls. An attacker must breach all layers — firewall, WAF, authentication, authorization, encryption — to succeed.",
    },
]


def _get_quiz_questions(category: str, difficulty: str, count: int) -> list:
    pool = QUESTION_BANK
    if category != "All":
        pool = [q for q in pool if q["category"] == category]
    if difficulty != "All":
        pool = [q for q in pool if q["difficulty"] == difficulty]
    if not pool:
        return []
    count = min(count, len(pool))
    return random.sample(pool, count)


def show() -> None:
    inject_css()
    page_header("Security Architecture Quiz",
                "Adaptive quizzes on STRIDE, DREAD, Architecture Patterns, OWASP, and Secure Coding.")

    # Stats
    cats = list({q["category"] for q in QUESTION_BANK})
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Questions", len(QUESTION_BANK))
    m2.metric("Categories", len(cats))
    m3.metric("Difficulty Levels", 3)
    m4.metric("Your Best Score", f"{st.session_state.get('quiz_best_score', 0)}/10")

    tab1, tab2 = st.tabs(["🎮 Take Quiz", "📊 Score History"])

    with tab1:
        section_heading("Quiz Configuration")

        c1, c2, c3 = st.columns(3)
        sel_cat = c1.selectbox("Topic", ["All"] + sorted(cats))
        sel_diff = c2.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])
        sel_count = c3.slider("Number of Questions", 3, min(10, len(QUESTION_BANK)), 5)

        if st.button("🚀 Start New Quiz", type="primary", use_container_width=True):
            questions = _get_quiz_questions(sel_cat, sel_diff, sel_count)
            if not questions:
                st.warning("No questions match your filters. Try different settings.")
            else:
                st.session_state["quiz_questions"] = questions
                st.session_state["quiz_answers"] = {}
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_score"] = 0
                st.rerun()

        # Quiz in progress
        if "quiz_questions" in st.session_state and st.session_state["quiz_questions"]:
            questions = st.session_state["quiz_questions"]
            submitted = st.session_state.get("quiz_submitted", False)

            if not submitted:
                section_heading(f"Quiz — {len(questions)} Questions")
                st.markdown(f"""
<div style="background:#0f2d5c; border:1px solid #1e3a5f; border-radius:10px;
            padding:12px 16px; margin-bottom:16px;">
  <span style="color:#9ca3af; font-size:0.85rem;">
    📋 Answer all questions then click Submit.
    Topic: <b style="color:#00D4FF">{sel_cat}</b> |
    Difficulty: <b style="color:#00D4FF">{sel_diff}</b>
  </span>
</div>
""", unsafe_allow_html=True)

                answers = st.session_state.get("quiz_answers", {})
                for i, q in enumerate(questions):
                    diff_colour = {"Easy": "#00C853", "Medium": "#FFD700", "Hard": "#FF2D2D"}.get(q["difficulty"], "#aaa")
                    st.markdown(f"""
<div style="background:#161b22; border:1px solid #30363d; border-radius:12px;
            padding:16px 20px; margin:12px 0;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
    <span style="color:#9ca3af; font-size:0.8rem;">Question {i+1} of {len(questions)} · {q['category']}</span>
    <span style="background:{diff_colour}22; color:{diff_colour}; border:1px solid {diff_colour};
                 padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:700;">
      {q['difficulty']}
    </span>
  </div>
  <div style="color:#e5e7eb; font-size:1rem; font-weight:600;">{q['question']}</div>
</div>
""", unsafe_allow_html=True)

                    selected = st.radio(
                        f"q{i}",
                        q["options"],
                        key=f"q_{q['id']}",
                        label_visibility="collapsed",
                    )
                    answers[q["id"]] = selected
                    st.session_state["quiz_answers"] = answers
                    st.markdown("<br>", unsafe_allow_html=True)

                answered = len([v for v in answers.values() if v])
                st.markdown(f"**{answered}/{len(questions)} answered**")

                if st.button("✅ Submit Quiz", type="primary", use_container_width=True,
                             disabled=(answered < len(questions))):
                    score = sum(
                        1 for q in questions
                        if answers.get(q["id"]) == q["answer"]
                    )
                    st.session_state["quiz_submitted"] = True
                    st.session_state["quiz_score"] = score
                    # Track history
                    hist = st.session_state.get("quiz_history", [])
                    hist.append({"score": score, "total": len(questions),
                                 "category": sel_cat, "difficulty": sel_diff})
                    st.session_state["quiz_history"] = hist
                    best = st.session_state.get("quiz_best_score", 0)
                    if score > best:
                        st.session_state["quiz_best_score"] = score
                    st.rerun()

            else:
                # Results
                questions = st.session_state["quiz_questions"]
                answers = st.session_state.get("quiz_answers", {})
                score = st.session_state.get("quiz_score", 0)
                total = len(questions)
                pct = round(score / total * 100)

                result_colour = "#FF2D2D" if pct < 50 else "#FFD700" if pct < 75 else "#00C853"
                grade = "F" if pct < 50 else "C" if pct < 65 else "B" if pct < 80 else "A" if pct < 95 else "A+"
                message = {
                    "F": "Keep studying! Review the explanations below carefully.",
                    "C": "Getting there! Focus on the questions you missed.",
                    "B": "Good work! A few more practice runs and you'll ace it.",
                    "A": "Excellent! Strong understanding of security architecture.",
                    "A+": "Outstanding! Expert-level knowledge demonstrated.",
                }[grade]

                st.markdown(f"""
<div style="background:#161b22; border:2px solid {result_colour};
            border-radius:20px; padding:32px; text-align:center; margin-bottom:24px;">
  <div style="font-size:3.5rem; font-weight:900; color:{result_colour};">{score}/{total}</div>
  <div style="font-size:2rem; font-weight:700; color:{result_colour}; margin:8px 0;">{pct}% — Grade {grade}</div>
  <div style="color:#9ca3af; font-size:0.95rem;">{message}</div>
</div>
""", unsafe_allow_html=True)

                section_heading("Question Review")
                for i, q in enumerate(questions):
                    user_ans = answers.get(q["id"], "")
                    correct = user_ans == q["answer"]
                    icon = "✅" if correct else "❌"
                    bg = "#0d2d1a" if correct else "#2d0f0f"
                    border = "#00C853" if correct else "#FF2D2D"

                    with st.expander(f"{icon} Q{i+1}: {q['question'][:60]}…", expanded=not correct):
                        st.markdown(f"""
<div style="background:{bg}; border-left:4px solid {border}; padding:12px; border-radius:0 8px 8px 0; margin:8px 0;">
  <div>Your answer: <b style="color:{'#00C853' if correct else '#FF6B6B'}">{user_ans or 'Not answered'}</b></div>
  {"" if correct else f'<div style="margin-top:4px;">Correct answer: <b style="color:#00C853">{q["answer"]}</b></div>'}
</div>
""", unsafe_allow_html=True)
                        st.markdown(f"**💡 Explanation:** {q['explanation']}")

                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state["quiz_questions"] = []
                    st.session_state["quiz_submitted"] = False
                    st.rerun()

    with tab2:
        section_heading("Your Quiz History")
        hist = st.session_state.get("quiz_history", [])
        if not hist:
            st.info("Complete a quiz to see your history here.")
        else:
            import pandas as pd
            rows = [{"Attempt": i + 1, "Score": f"{h['score']}/{h['total']}",
                     "Percentage": f"{round(h['score']/h['total']*100)}%",
                     "Category": h["category"], "Difficulty": h["difficulty"]}
                    for i, h in enumerate(hist)]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.metric("Best Score", f"{st.session_state.get('quiz_best_score', 0)} correct")
