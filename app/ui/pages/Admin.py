import streamlit as st

st.set_page_config(page_title="Model Stats | AI Diabetes Doctor", page_icon="📊")

st.title("Model statistics")

st.write(
    "Here you can show the evaluation results of your ML model. "
    "Right now this page uses fixed demo numbers – replace them with the real ones from your training notebook."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accuracy", "0.86")
with col2:
    st.metric("Precision", "0.81")
with col3:
    st.metric("Recall", "0.79")
with col4:
    st.metric("AUC", "0.90")

st.markdown("---")
st.markdown(
    """
You can also paste:

- Confusion matrix as an image  
- Feature importance bar chart  
- Short explanation of your chosen algorithm.

This page is perfect for your **report/demo**.
"""
)
