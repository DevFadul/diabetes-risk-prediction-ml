from pathlib import Path
from dataclasses import dataclass
import numpy as np
import streamlit as st

# --------- page setup (boot the Risk Check screen) ----------
st.set_page_config(page_title="Risk Check | AI Diabetes Doctor", layout="wide")


# --------- load global CSS (pull in the shared UI styling) ----------
def load_css():
    """
    Loads the main app stylesheet.
    CSS lives at: app/ui/assets/style.css
    This file is: app/ui/pages/2_Risk_Check.py
    """
    ui_root = Path(__file__).resolve().parent.parent   # -> .../app/ui
    css_path = ui_root / "assets" / "style.css"

    if css_path.exists():
        with css_path.open() as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f" CSS file not found at: {css_path}")


load_css()

# --------- theme toggle (syncing with Overview page) ----------
if "light_mode" not in st.session_state:
    st.session_state["light_mode"] = False

light_mode = st.toggle("Light mode", key="light_mode")

# --------- extra light-mode patches (the real theme tweak lives here) ----------
if st.session_state["light_mode"]:
    st.markdown(
        """
        <style>
        /* global background + text flip */
        html, body, .stApp {
            background-color: #f4f4f5 !important;
            color: #020617 !important;
        }

        /* risk-check cards + form boxes */
        .info-box,
        [data-testid="stForm"] {
            background: #ffffff !important;
            border-color: #e5e7eb !important;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08) !important;
        }

        /* section title look */
        .section-title { 
            color: #020617 !important; 
        }

        /* labels tweak */
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label { 
            color: #111827 !important; 
        }

        /* input boxes restyle */
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox select {
            background: #f9fafb !important;
            color: #111827 !important;
            border-color: #d4d4d8 !important;
        }

        /* -------------------------------------------------
           biggest fix: make form buttons match in light mode
           (Predict + Basic Info buttons)
        ------------------------------------------------- */
        [data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
            background: #111827 !important;
            border-color: #111827 !important;
            color: #ffffff !important; 
            border-radius: 28px !important;
            font-weight: 600 !important;
        }

        /* force every inner element to stay white */
        [data-testid="stForm"] [data-testid="stFormSubmitButton"] button * {
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------- mode switching (basic vs advanced UI) ----------
if "mode" not in st.session_state:
    st.session_state.mode = "basic"


# ------------------------- input models (just clean data containers) -------------------------
@dataclass
class BasicInput:
    age: int
    gender: str
    height: float
    weight: float
    family_history: bool
    activity: str


@dataclass
class AdvancedInput:
    glucose: float
    bp: float
    insulin: float
    skin: float
    bmi: float
    pregnancies: int


# ------------------------- tiny mock ML scoring -------------------------
def basic_model(x: BasicInput):
    score = 0
    score += (x.age - 35) * 0.01
    score += 0.2 if x.family_history else 0
    if x.activity == "Low":
        score += 0.1
    if x.activity == "High":
        score -= 0.05
    prob = 1 / (1 + np.exp(-score))
    return float(np.clip(prob, 0.01, 0.99))


def advanced_model(x: AdvancedInput):
    score = 0
    score += (x.glucose - 90) * 0.02
    score += (x.bmi - 25) * 0.02
    score += (x.bp - 80) * 0.01
    score += x.pregnancies * 0.03
    prob = 1 / (1 + np.exp(-score))
    return float(np.clip(prob, 0.01, 0.99))


# ================================================================
#                         BASIC MODE UI
# ================================================================
if st.session_state.mode == "basic":

    st.markdown("<h2 class='section-title'>Basic information</h2>", unsafe_allow_html=True)

    # whole basic-flow UI lives inside this form
    with st.form("basic_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", 18, 100, 30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            height = st.number_input("Height (cm)", 100.0, 220.0, 170.0)

        with col2:
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
            family_history_str = st.selectbox("Family history of diabetes", ["No", "Yes"])
            activity = st.selectbox("Physical Activity", ["Low", "Moderate", "High"])

        bmi_calc = weight / ((height / 100) ** 2)
        st.caption(f"Estimated BMI from height/weight: **{bmi_calc:.1f}**")

        # === button row (Predict on left, switch to Advanced on right) ===
        btn_col_left, btn_col_right = st.columns([1, 1])

        with btn_col_left:
            basic_submit = st.form_submit_button(
                "Predict",
                use_container_width=True,   # stretch button full-width in its column
            )

        with btn_col_right:
            to_advanced = st.form_submit_button(
                "Advanced clinical values",
                use_container_width=True,   # same trick so both stay equal-sized
            )

    # handle Predict + mode switching
    if basic_submit:
        data = BasicInput(
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            family_history=(family_history_str == "Yes"),
            activity=activity,
        )
        prob = basic_model(data)
        st.success(f"Basic Risk Estimate: **{prob*100:.1f}%**")

    if to_advanced:
        st.session_state.mode = "advanced"
        st.rerun()


# ================================================================
#                       ADVANCED MODE UI
# ================================================================
else:
    st.markdown(
        "<h2 class='section-title'>Advanced clinical values (optional)</h2>",
        unsafe_allow_html=True,
    )

    with st.form("advanced_form"):
        colA, colB = st.columns(2)

        with colA:
            glucose = st.number_input("Glucose (mg/dL)", 60.0, 250.0, 100.0)
            insulin = st.number_input("Insulin (µU/mL)", 0.0, 400.0, 80.0)
            pregnancies = st.number_input("Pregnancies", 0, 20, 0)

        with colB:
            bp = st.number_input("Blood Pressure (systolic)", 80.0, 200.0, 120.0)
            skin = st.number_input("Skin Thickness (mm)", 0.0, 80.0, 20.0)
            bmi = st.number_input("BMI", 10.0, 60.0, 26.0)

        # === button row (Predict vs switch back to Basic mode) ===
        btn_col_left, btn_col_right = st.columns([1, 1])

        with btn_col_left:
            adv_submit = st.form_submit_button(
                "Predict",
                use_container_width=True,
            )

        with btn_col_right:
            back_basic = st.form_submit_button(
                "Basic information",
                use_container_width=True,
            )

    if adv_submit:
        data = AdvancedInput(
            glucose=glucose,
            bp=bp,
            insulin=insulin,
            skin=skin,
            bmi=bmi,
            pregnancies=pregnancies,
        )
        prob = advanced_model(data)
        st.success(f"Advanced Risk Estimate: **{prob*100:.1f}%**")

    if back_basic:
        st.session_state.mode = "basic"
        st.rerun()
# ========= end of 2_Risk_Check.py =========