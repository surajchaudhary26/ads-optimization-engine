import streamlit as st
import requests
from typing import List, Dict

# =========================================================
# CONFIGURATION
# =========================================================

BACKEND_URL = "https://ads-optimization-engine.onrender.com/decide-ads"

st.set_page_config(
    page_title="Ads Optimization Engine",
    layout="wide"
)

# =========================================================
# PROJECT INTRODUCTION
# =========================================================

st.title("Ads Optimization Engine")

st.markdown(
    """
### What is this project?

This system helps you **select the best advertisements under a fixed budget**.

Instead of manually choosing ads, the engine:
- Evaluates **cost, business priority, clicks, and conversions**
- Applies **machine-learning signals + business rules**
- Ranks ads and explains **why** each ad is selected

The goal is simple:
> **Spend less, prioritize better ads, and make decisions transparently.**
"""
)

st.divider()

# =========================================================
# CAMPAIGN CONFIGURATION
# =========================================================

st.subheader("Campaign Setup")

total_budget = st.number_input(
    label="Total Campaign Budget",
    min_value=1,
    value=500,
    step=50,
    help="Maximum total amount you want to spend across all ads"
)

ad_count = st.number_input(
    label="Number of Ads to Evaluate",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

st.divider()

# =========================================================
# AD INPUT SECTION
# =========================================================

st.subheader("Ad Details")

st.markdown(
    """
Provide realistic values for each advertisement.
These inputs directly influence ranking and selection.
"""
)

ads: List[Dict] = []

for i in range(ad_count):
    with st.expander(f"Ad {i + 1}", expanded=True):

        ad_id = st.text_input(
            label="Ad Identifier",
            value=f"ad_{i + 1}",
            help="A unique ID or name for this ad",
            key=f"ad_id_{i}"
        )

        cost = st.number_input(
            label="Cost",
            min_value=1,
            value=50,
            step=5,
            help="Budget required to run this ad",
            key=f"cost_{i}"
        )

        priority = st.selectbox(
            label="Business Priority",
            options=[1, 2, 3],
            index=2,
            help="3 = High priority, 2 = Medium, 1 = Low",
            key=f"priority_{i}"
        )

        clicks = st.number_input(
            label="Estimated Clicks",
            min_value=0,
            value=100,
            step=10,
            help="Expected or historical clicks",
            key=f"clicks_{i}"
        )

        conversions = st.number_input(
            label="Conversions",
            min_value=0,
            value=10,
            step=1,
            help="Successful outcomes from clicks",
            key=f"conversions_{i}"
        )

        ads.append(
            {
                "ad_id": ad_id,
                "cost": int(cost),
                "priority": int(priority),
                "clicks": int(clicks),
                "conversions": int(conversions),
            }
        )

st.divider()

# =========================================================
# SUBMIT & BACKEND CALL
# =========================================================

if st.button("Run Optimization", type="primary"):

    payload = {
        "total_budget": int(total_budget),
        "ads": ads
    }

    st.subheader("Request Payload")
    st.json(payload)

    try:
        with st.spinner("Evaluating ads and optimizing budget..."):
            response = requests.post(
                BACKEND_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

        if response.status_code != 200:
            st.error("Backend returned an error")
            st.code(response.text)
            st.stop()

        result = response.json()

    except requests.exceptions.RequestException as e:
        st.error("Failed to connect to backend service")
        st.exception(e)
        st.stop()

    if not result.get("success", False):
        st.error("Optimization failed")
        st.json(result)
        st.stop()

    # =========================================================
    # RESULTS
    # =========================================================

    st.success("Optimization completed successfully")

    st.subheader("Summary")

    col1, col2 = st.columns(2)
    col1.metric("Total Cost Used", result["total_cost"])
    col2.metric("Remaining Budget", result["remaining_budget"])

    st.divider()

    st.subheader("Recommended Ads (Ranked)")

    for ad in result["selected_ads"]:
        with st.expander(f"Rank {ad['rank']} — {ad['label']}", expanded=True):
            st.write(f"Ad ID: {ad['ad_id']}")
            st.write(f"Cost: {ad['cost']}")
            st.write(f"Priority: {ad['priority']}")
            st.write(f"ML Score: {ad['ml_score']}")
            st.write(f"Final Score: {ad['final_score']}")
            st.info(ad["reason"])

    st.divider()

    st.subheader("Raw Backend Response")
    st.json(result)
