import streamlit as st
import pandas as pd
from ui.styles import label_badge


def render_input_section():
    st.header("Input")

    with st.container():
        total_budget = st.number_input(
            "Total Budget",
            min_value=1.0,
            value=300.0,
            help="Maximum total cost allowed for selecting ads"
        )

        ad_count = st.number_input(
            "Number of Ads",
            min_value=1,
            max_value=10,
            value=4,
            step=1,
            help="How many ads you want to evaluate"
        )

        st.divider()

        ads = []
        for i in range(int(ad_count)):
            st.subheader(f"Ad {i + 1}")

            col1, col2, col3 = st.columns(3)

            ad_id = col1.text_input(
                f"Ad ID",
                value=f"ad_{i+1}",
                key=f"ad_id_{i}"
            )

            cost = col2.number_input(
                "Cost",
                min_value=1.0,
                value=50.0,
                key=f"cost_{i}"
            )

            priority = col3.selectbox(
                "Priority",
                options=[1, 2, 3],
                index=1,
                key=f"priority_{i}"
            )

            col4, col5 = st.columns(2)

            clicks = col4.number_input(
                "Clicks",
                min_value=0,
                value=100,
                key=f"clicks_{i}"
            )

            conversions = col5.number_input(
                "Conversions",
                min_value=0,
                value=10,
                key=f"conversions_{i}"
            )

            ads.append({
                "ad_id": ad_id,
                "cost": cost,
                "priority": priority,
                "clicks": clicks,
                "conversions": conversions
            })

            st.divider()

    return total_budget, ads


def render_output_section(response: dict):
    st.header("Output")

    with st.container():
        col1, col2, col3 = st.columns(3)

        col1.metric("Strategy Used", response["strategy"])
        col2.metric("Total Cost Used", response["total_cost"])
        col3.metric("Remaining Budget", response["remaining_budget"])

        st.divider()

        rows = []
        for ad in response["selected_ads"]:
            rows.append({
                "Rank": ad["rank"],
                "Ad ID": ad["ad_id"],
                "Label": f'{label_badge(ad["label"])} - {ad["label"]}',
                "Cost": ad["cost"],
                "Priority": ad["priority"],
                "ML Score": ad["ml_score"],
                "Final Score": ad["final_score"],
                "Reason": ad["reason"]
            })

        df = pd.DataFrame(rows).sort_values("Rank")
        st.dataframe(df, use_container_width=True)
