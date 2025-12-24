import streamlit as st
import requests
import pandas as pd

# =============================
# CONFIGURATION
# =============================
import os

API_URL = os.getenv(
    "ADS_API_URL",
    "http://127.0.0.1:8000/decide-ads"
)

st.set_page_config(
    page_title="Ads Optimization Engine",
    layout="wide"
)

# =============================
# HELPER: EXPLANATION LOGIC
# =============================
def explain_ad(row, rank):
    reasons = []

    if row["priority"] == 3:
        reasons.append("high business priority")
    elif row["priority"] == 2:
        reasons.append("medium business priority")
    else:
        reasons.append("low business priority")

    if row["cost"] <= 100:
        reasons.append("low cost")
    elif row["cost"] <= 200:
        reasons.append("moderate cost")
    else:
        reasons.append("high cost")

    if row["ml_score"] > 50:
        reasons.append("strong ML predicted value")
    elif row["ml_score"] > 20:
        reasons.append("average ML predicted value")
    else:
        reasons.append("low ML predicted value")

    if rank == 1:
        label = "Best choice"
    elif rank == 2:
        label = "Good choice"
    else:
        label = "Acceptable choice"

    return f"{label} because of " + ", ".join(reasons)


# =============================
# PAGE HEADER
# =============================
st.title("Ads Optimization Engine")
st.caption(
    "This application helps select the most valuable ads under a fixed budget "
    "using machine learning and business rules."
)

st.divider()

# =============================
# SESSION STATE
# =============================
if "ads" not in st.session_state:
    st.session_state.ads = []

# =============================
# INPUT SECTION
# =============================
st.header("Input Section")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Budget Configuration")

    total_budget = st.number_input(
        "Total available budget",
        min_value=1,
        value=300,
        step=10,
        help="Maximum amount you are willing to spend on ads"
    )

    st.info(
        "The system will select ads such that the total cost does not exceed this budget."
    )

with right_col:
    st.subheader("Add Advertisement")

    with st.form("add_ad_form"):
        ad_id = st.text_input(
            "Ad ID",
            placeholder="Example: ad_101"
        )

        cost = st.number_input(
            "Ad cost",
            min_value=1,
            value=50,
            help="Cost required to run this ad"
        )

        priority = st.selectbox(
            "Business priority",
            [1, 2, 3],
            help="3 = highest importance, 1 = lowest importance"
        )

        clicks = st.number_input(
            "Clicks",
            min_value=0,
            value=100,
            help="Number of users who clicked the ad"
        )

        conversions = st.number_input(
            "Conversions",
            min_value=0,
            value=10,
            help="Number of users who completed the desired action"
        )

        submit_ad = st.form_submit_button("Add ad")

        if submit_ad:
            if not ad_id:
                st.error("Ad ID is required")
            else:
                st.session_state.ads.append({
                    "ad_id": ad_id,
                    "cost": cost,
                    "priority": priority,
                    "clicks": clicks,
                    "conversions": conversions
                })
                st.success(f"Ad '{ad_id}' added successfully")

st.divider()

# =============================
# INPUT PREVIEW
# =============================
st.subheader("Ads Provided as Input")

if st.session_state.ads:
    st.dataframe(
        pd.DataFrame(st.session_state.ads),
        use_container_width=True
    )
else:
    st.warning("No ads added yet")

st.divider()

# =============================
# RUN OPTIMIZATION
# =============================
st.header("Run Optimization")

if st.button("Decide Ads"):
    if not st.session_state.ads:
        st.error("Please add at least one ad before running optimization")
    else:
        payload = {
            "total_budget": total_budget,
            "ads": st.session_state.ads
        }

        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()

                st.success("Optimization completed successfully")

                # =============================
                # OUTPUT SECTION
                # =============================
                st.divider()
                st.header("Output Section")

                summary_col, _ = st.columns([1, 2])

                with summary_col:
                    st.subheader("Result Summary")
                    st.write(f"Strategy used: {result['strategy']}")
                    st.write(f"Total cost used: {result['total_cost']}")
                    st.write(f"Remaining budget: {result['remaining_budget']}")

                if result["selected_ads"]:
                    st.subheader("Selected Ads (Ranked and Explained)")

                    df = pd.DataFrame(result["selected_ads"])
                    df["rank"] = range(1, len(df) + 1)

                    df["reason"] = df.apply(
                        lambda row: explain_ad(row, row["rank"]),
                        axis=1
                    )

                    df = df[
                        [
                            "rank",
                            "ad_id",
                            "cost",
                            "priority",
                            "ml_score",
                            "final_score",
                            "reason"
                        ]
                    ]

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    st.info(
                        "Ads are ordered from best to worst based on overall value. "
                        "Higher-ranked ads provide better value relative to cost, priority, and ML prediction."
                    )
                else:
                    st.warning("No ads could be selected within the given budget")

            else:
                st.error(response.json().get("detail", "Backend returned an error"))

        except Exception as e:
            st.error(f"Unable to connect to backend: {e}")

st.divider()

# =============================
# RESET
# =============================
if st.button("Reset all inputs"):
    st.session_state.ads = []
    st.success("All input data has been cleared")
