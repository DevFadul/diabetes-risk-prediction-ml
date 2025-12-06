from pathlib import Path
import streamlit as st

# ========= app boot stuff (kick off the page) =========
st.set_page_config(
    page_title="GlucoSense | AI Diabetes Doctor",
    layout="wide",
)

# ========= css loader (yo we just pull in the global styles) =========
def load_css():
    root_path = Path(__file__).resolve().parent
    css_path = root_path / "assets" / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

# ========= reusable HTML chunks (UI pieces we drop in) =========

TOP_BAR_HTML = """
<div class="top-bar">
  <div class="brand">
    <span class="brand-name">GlucoSense</span>
    <span class="brand-subtitle">AI Diabetes Doctor</span>
  </div>
  <div class="brand-badge">
    Early-risk assistant · Not a medical device
  </div>
</div>
"""

# only change here: using a div instead of h1 (cleaner control)
HERO_TITLE_HTML = """
<div class="hero-title">
  <span class="hero-title-text">Check your diabetes risk in under a minute</span>
</div>
"""

LEFT_MAIN_HTML = """
<div class="info-box main-info">
  <p class="info-text">
    Enter your health numbers, get a clear risk score,
    and see which factors matter most for you.
  </p>
  <ul class="info-list">
    <li><span class="checkmark">✔</span> Instant risk estimate (Low / Medium / High)</li>
    <li><span class="checkmark">✔</span> SHAP explanation for each feature</li>
    <li><span class="checkmark">✔</span> Simple, actionable lifestyle tips</li>
    <li><span class="checkmark">✔</span> No name, no ID – just health data</li>
  </ul>
</div>
"""

HOW_HTML = """
<div class="how-box">
  <h3 class="how-title">How this app helps you</h3>
  <div class="how-columns">
    <div class="how-item">
      <div class="how-number">1.</div>
      <div>
        <p class="how-heading">Enter numbers</p>
        <p class="how-text">
          Age, BMI, glucose, blood pressure and a few lifestyle questions.
        </p>
      </div>
    </div>
    <div class="how-item">
      <div class="how-number">2.</div>
      <div>
        <p class="how-heading">Get a clear explanation</p>
        <p class="how-text">
          SHAP shows which features push your risk up or down.
        </p>
      </div>
    </div>
    <div class="how-item">
      <div class="how-number">3.</div>
      <div>
        <p class="how-heading">Plan next steps</p>
        <p class="how-text">
          Use the advice section to prepare questions for your doctor.
        </p>
      </div>
    </div>
  </div>
</div>
"""

DISCLAIMER_HTML = """
<div class="disclaimer-box">
  This tool is for educational purposes only.
  It does not replace a medical diagnosis or professional advice.
</div>
"""

# ========= theme state (light / dark toggle switch vibes) 

if "light_mode" not in st.session_state:
    st.session_state["light_mode"] = False

top_left, top_right = st.columns([0.8, 0.2])

with top_right:
    light_mode = st.toggle("Light mode", value=st.session_state["light_mode"])

st.session_state["light_mode"] = light_mode

# light-mode override: slap extra CSS on top of the base theme
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
</style>
        """,
        unsafe_allow_html=True,
    )

# layout rendering (dropping chunks on screen) =========

st.markdown(TOP_BAR_HTML, unsafe_allow_html=True)
st.markdown(HERO_TITLE_HTML, unsafe_allow_html=True)   # no st.write() gap here, clean stack

# main info card right under the hero
st.markdown(LEFT_MAIN_HTML, unsafe_allow_html=True)

# center CTA button — styling tied to key=start_risk_btn
start_clicked = st.button("start risk check", key="start_risk_btn")

# page hop into the risk-check flow
if start_clicked:
    st.switch_page("pages/2_Risk_Check.py")

st.markdown(HOW_HTML, unsafe_allow_html=True)
st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)
st.write("")
# ========= end of Overview.py =========