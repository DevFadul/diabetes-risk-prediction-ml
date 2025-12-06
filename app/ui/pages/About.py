import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="My History | AI Diabetes Doctor", page_icon="📈")

st.title("My History")

st.write(
    "This page will later read your past predictions from SQLite. "
    "For now we show a small demo history."
)

dates = pd.date_range(end=pd.Timestamp.today(), periods=8)
risks = np.array([0.18, 0.22, 0.25, 0.3, 0.27, 0.24, 0.26, 0.23])

df = pd.DataFrame({"date": dates, "risk": risks})
df.set_index("date", inplace=True)

st.line_chart(df, height=260)

st.markdown(
    """
Each point represents one risk check.

Later we will:

- store (user_id, timestamp, features, probability) in SQLite  
- filter by user_id  
- draw this chart using the real data.
"""
)
