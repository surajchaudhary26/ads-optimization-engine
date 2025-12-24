import streamlit as st

def render_header(title: str, subtitle: str):
    st.title(title)
    st.caption(subtitle)


def render_input_section():
    st.subheader("Input Configuration")
    st.markdown(
        "Configure your total budget and add as many ads as needed. "
        "Each ad will be evaluated by the backend ML engine."
    )

    total_budget = st.number_input(
        "Total Budget",
        min_value=1.0,
        value=500.0,
        help="Maximum total spend allowed across all selected ads",
        key="total_budget"
    )

    st.divider()

    # Dynamic ads
    ads = []
    ad_count = st.number_input(
        "Number of Ads",
        min_value=1,
        max_value=20,
        value=4,
        help="Select how many ads you want to evaluate",
        key="ad_count"
    )

    for i in range(ad_count):
        with st.expander(f"Ad {i+1}", expanded=(i == 0)):
            ads.append({
                "ad_id": st.text_input(
                    "Ad ID",
                    value=f"ad_{i+1}",
                    help="Unique identifier for this ad",
                    key=f"ad_id_{i}"
                ),
                "cost": st.number_input(
                    "Cost",
                    min_value=1.0,
                    value=50.0,
                    help="Cost required to run this ad",
                    key=f"cost_{i}"
                ),
                "priority": st.selectbox(
                    "Business Priority",
                    [1, 2, 3],
                    index=1,
                    help="3 = highest priority, 1 = lowest",
                    key=f"priority_{i}"
                ),
                "clicks": st.number_input(
                    "Clicks",
                    min_value=0,
                    value=100,
                    help="Historical click count",
                    key=f"clicks_{i}"
                ),
                "conversions": st.number_input(
                    "Conversions",
                    min_value=0,
                    value=10,
                    help="Successful conversions from clicks",
                    key=f"conversions_{i}"
                ),
            })

    return {
        "total_budget": total_budget,
        "ads": ads
    }


def render_results(response: dict):
    st.subheader("Optimization Results")

    col1, col2 = st.columns(2)
    col1.metric("Total Cost Used", response["total_cost"])
    col2.metric("Remaining Budget", response["remaining_budget"])

    st.divider()

    for ad in response["selected_ads"]:
        with st.expander(f"Rank {ad['rank']} — {ad['label']}"):
            st.markdown(f"**Ad ID:** {ad['ad_id']}")
            st.markdown(f"**Final Score:** `{ad['final_score']}`")
            st.markdown(f"**ML Score:** `{ad['ml_score']}`")
            st.markdown("🧠 **Why selected?**")
            st.info(ad["reason"])
