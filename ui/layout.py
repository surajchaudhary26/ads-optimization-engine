import streamlit as st


def render_header(title: str, subtitle: str):
    st.title(title)
    st.caption(subtitle)


def render_input_section():
    st.subheader("Input Configuration")

    budget = st.number_input(
        "Total Budget",
        min_value=1.0,
        value=500.0,
        key="total_budget"
    )

    ads = []
    for i in range(1, 5):
        with st.expander(f"Ad {i}"):
            ads.append({
                "ad_id": st.text_input(
                    "Ad ID",
                    f"ad_{i}",
                    key=f"ad_id_{i}"
                ),
                "cost": st.number_input(
                    "Cost",
                    min_value=1.0,
                    value=50.0,
                    key=f"cost_{i}"
                ),
                "priority": st.selectbox(
                    "Priority",
                    [1, 2, 3],
                    index=1,
                    key=f"priority_{i}"
                ),
                "clicks": st.number_input(
                    "Clicks",
                    min_value=0,
                    value=100,
                    key=f"clicks_{i}"
                ),
                "conversions": st.number_input(
                    "Conversions",
                    min_value=0,
                    value=10,
                    key=f"conversions_{i}"
                ),
            })

    return {
        "total_budget": budget,
        "ads": ads
    }


def render_results(response):
    st.subheader("Optimization Results")

    st.metric("Total Cost Used", response["total_cost"])
    st.metric("Remaining Budget", response["remaining_budget"])

    for ad in response["selected_ads"]:
        with st.expander(f"Rank {ad['rank']} — {ad['label']}"):
            st.write(f"Ad ID: {ad['ad_id']}")
            st.write(f"Final Score: {ad['final_score']}")
            st.write(f"ML Score: {ad['ml_score']}")
            st.write(f"Reason: {ad['reason']}")
