from pathlib import Path
import streamlit as st

# --- page boot: spinning up the About screen ---
st.set_page_config(page_title="About • GlucoSense", layout="wide")


# --- load global CSS so this page stays on-brand with the rest of the app ---
def load_css():
    ui_root = Path(__file__).resolve().parent.parent   # -> sliding up into .../app/ui
    css_path = ui_root / "assets" / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


load_css()

# --- shared light/dark toggle (same state used across all pages) ---
if "light_mode" not in st.session_state:
    st.session_state["light_mode"] = False

top_left, top_right = st.columns([0.8, 0.2])

with top_right:
    light_mode = st.toggle("Light mode", value=st.session_state["light_mode"])

st.session_state["light_mode"] = light_mode

# --- light-mode CSS override (basically repainting the UI on the fly) ---
if light_mode:
    st.markdown(
        """
<style>
html, body, .stApp {
    background-color: #ffffff !important;
    color: #0f172a !important;
}

.top-bar {
    background: #e5f0ff !important;
    border-color: #cbd5e1 !important;
    box-shadow: 0 8px 18px rgba(148,163,184,0.4) !important;
}

.brand-name { color: #0f172a !important; }
.brand-subtitle { color: #2563eb !important; }

.brand-badge {
    background: #2563eb !important;
    color: #e5f1ff !important;
}

.hero-title,
.hero-title-text,
.info-text,
.how-title,
.how-heading,
.how-text {
    color: #0f172a !important;
}

.info-box,
.how-box {
    background: #f4f7ff !important;
    border-color: #cbd5e1 !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08) !important;
}

.disclaimer-box {
    background: rgba(249,115,22,0.07) !important;
    color: #9a3412 !important;
    border-color: #fb923c !important;
}

[data-testid="stSwitch"] label {
    color: #0f172a !important;
}

/* making the text inside About boxes readable in light mode */
.info-box h2,
.info-box p,
.info-box li {
    color: #020617 !important;
}

/* bullet colors in lists */
.info-box ul li::marker {
    color: #020617 !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )

# --- page header block: title + subtitle ---
st.markdown(
"""
<div style="
    width:100%;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    margin-top:30px;
    margin-bottom:25px;
">

  <h1 style="
      font-size:48px;
      font-weight:900;
      color:inherit;
      margin-bottom:6px;
      text-align:center !important;
  ">
      About GlucoSense
  </h1>

  <p style="
    font-size:20px;
    opacity:0.85;
    margin-top:-10px;
    text-align:left !important;
    margin-left:-25px;   /* tiny manual shift because the boss asked for it */
">
    AI-powered early diabetes risk assistant
</p>

</div>
""",
    unsafe_allow_html=True,
)

# --- box 1: breaking down what the app actually does ---
st.markdown(
"""
<div class="info-box">
  <h2 style="margin-top:0;"> What This App Does</h2>

  <ul style="margin-top:10px; line-height:1.7;">
    <li>Helps you check your diabetes risk early before symptoms appear.</li>
    <li>Uses a machine-learning model trained on real medical data.</li>
    <li>Analyzes patterns in glucose, BMI, age, blood pressure, and lifestyle factors.</li>
    <li>Gives a simple result: <b>higher</b> or <b>lower</b> risk.</li>
    <li>Explains the <b>top factors</b> that influenced your score.</li>
  </ul>
</div>
""",
    unsafe_allow_html=True,
)

# --- box 2: why any of this even matters ---
st.markdown(
"""
<div class="info-box">
  <h2>Why This Matters</h2>

  <p style="margin-top:10px;">
    Early detection can prevent long-term complications.
    Knowing your risk today helps you protect your health tomorrow.
  </p>

  <ul style="margin-top:10px; line-height:1.7;">
    <li>Spot risks sooner instead of waiting for symptoms.</li>
    <li>Understand which habits and numbers matter most.</li>
    <li>Make informed decisions with your doctor.</li>
    <li>Track improvements over time as your lifestyle changes.</li>
  </ul>
</div>
""",
    unsafe_allow_html=True,
)

# --- box 3: what users should actually do after they get a score ---
st.markdown(
"""
<div class="info-box">
  <h2>What To Do With Your Result</h2>

  <p style="margin-top:10px;">
    This app does <b>not</b> diagnose diabetes. It's strictly an educational early-warning tool.
    If you pull a high-risk score, you might wanna:
  </p>

  <ul style="margin-top:10px; line-height:1.7;">
    <li>Talk with a doctor or healthcare professional.</li>
    <li>Check your blood sugar levels.</li>
    <li>Upgrade your diet, exercise, sleep, and stress habits.</li>
  </ul>

  <p style="margin-top:14px;">
    Your health data stays private and is only used to generate your result.
  </p>

  <p style="margin-top:18px; font-weight:700; text-align:center;">
    Awareness • Prevention • Action
  </p>
</div>
""",
    unsafe_allow_html=True,
)
