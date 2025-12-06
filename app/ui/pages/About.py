import streamlit as st

# Page Config
st.set_page_config(page_title="About • GlucoSense", layout="wide")

# Title Section
st.markdown(
    """
    <div style="text-align:center; padding-top:15px;">
        <h1 style="font-size: 44px; margin-bottom: 0;">About GlucoSense</h1>
        <p style="font-size:18px; opacity:0.8; margin-top:4px;">
            AI-powered Diabetes Early Risk Detection & Personalized Health Insights
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# Main Summary Card
st.markdown(
    """
    <div style="
        background-color:#1f1f1f;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
        margin-bottom: 30px;
    ">
        <h2 style="margin-top:0;">What is GlucoSense?</h2>
        <p style="font-size:17px; line-height:1.7; opacity:0.9;">
            GlucoSense is an AI-driven application designed to help users detect early signs 
            of diabetes by analyzing health metrics using ML models to produce accurate, 
            real-time predictions and personalized wellness recommendations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Feature Cards
st.markdown("<h2>Core Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="background-color:#1f1f1f; padding:20px; border-radius:18px; box-shadow:0 6px 16px rgba(0,0,0,0.3); height:100%;">
            <h3>⚕️ Diabetes Risk Check</h3>
            <p style="opacity:0.85; line-height:1.6;">Analyze lifestyle & health data to detect diabetes risk in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="background-color:#1f1f1f; padding:20px; border-radius:18px; box-shadow:0 6px 16px rgba(0,0,0,0.3); height:100%;">
            <h3>📊 Model Insights</h3>
            <p style="opacity:0.85; line-height:1.6;">Understand how the AI model makes predictions with clear visuals.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="background-color:#1f1f1f; padding:20px; border-radius:18px; box-shadow:0 6px 16px rgba(0,0,0,0.3); height:100%;">
            <h3>🎯 Personalized Guidance</h3>
            <p style="opacity:0.85; line-height:1.6;">Receive lifestyle recommendations tailored to your health profile.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# Developer Section
st.markdown(
    """
    <div style="
        background-color:#1f1f1f;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    ">
        <h2>About the Developer</h2>
        <p style="opacity:0.9; font-size:17px; line-height:1.7;">
            GlucoSense was developed by [Your Name], a passionate software developer and AI enthusiast 
            dedicated to leveraging technology for better health outcomes. With expertise in machine learning 
            and web development, [Your Name] aims to create accessible tools that empower individuals to take 
            control of their health.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
