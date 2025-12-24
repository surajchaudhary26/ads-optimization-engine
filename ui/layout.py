import streamlit as st

# ---------------- HEADER ----------------
def render_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.divider()


# ---------------- INPUT SECTION ----------------
def render_input_section():
    st.subheader("📥 Input Configuration")
    st.write(
        "Provide your **total budget** and details of each advertisement. "
        "You can add **any number of ads**. The system will select the most optimal ones."
    )

    budget = st.number_input(
        "💰 Total Budget",
        min_value=1.0,
        value=500.0,
        help="Total amount you are willing to spend across all ads"
    )

    st.divider()
    st.subheader("📢 Advertisements")

    # Session state for dynamic ads
    if "ads" not in st.session_state:
        st.session_state.ads = [
            {
                "ad_id": "ad_1",
                "cost": 50.0,
                "priority": 2,
                "clicks": 120,
                "conversions": 15,
            }
        ]

    # Render each ad
    for idx, ad in enumerate(st.session_state.ads):
        with st.expander(f"Ad #{idx + 1}", expanded=True):

            ad["ad_id"] = st.text_input(
                "Ad ID",
                value=ad["ad_id"],
                key=f"ad_id_{idx}",
                help="Unique identifier for this ad (e.g., ad_facebook_01)"
            )

            ad["cost"] = st.number_input(
                "Cost",
                min_value=1.0,
                value=ad["cost"],
                key=f"cost_{idx}",
                help="How much this ad costs to run"
            )

            ad["priority"] = st.selectbox(
                "Business Priority",
                [1, 2, 3],
                index=ad["priority"] - 1,
                key=f"priority_{idx}",
                help="1 = Low priority, 3 = High priority"
            )

            ad["clicks"] = st.number_input(
                "Clicks",
                min_value=0,
                value=ad["clicks"],
                key=f"clicks_{idx}",
                help="Number of clicks this ad received historically"
            )

            ad["conversions"] = st.number_input(
                "Conversions",
                min_value=0,
                value=ad["conversions"],
                key=f"conversions_{idx}",
                help="Number of successful conversions from this ad"
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("❌ Remove Ad", key=f"remove_{idx}"):
                    st.session_state.ads.pop(idx)
                    st.rerun()

    st.divider()

    if st.button("➕ Add New Ad"):
        st.session_state.ads.append(
            {
                "ad_id": f"ad_{len(st.session_state.ads) + 1}",
                "cost": 50.0,
                "priority": 2,
                "clicks": 100,
                "conversions": 10,
            }
        )
        st.rerun()

    return {
        "total_budget": budget,
        "ads": st.session_state.ads
    }


# ---------------- RESULT SECTION ----------------
def render_results(response):
    st.divider()
    st.subheader("📊 Optimization Results")

    col1, col2 = st.columns(2)
    col1.metric("Total Cost Used", response["total_cost"])
    col2.metric("Remaining Budget", response["remaining_budget"])

    st.divider()

    for ad in response["selected_ads"]:
        with st.expander(f"🏆 Rank {ad['rank']} — {ad['label']}"):
            st.markdown(f"""
            **Ad ID:** `{ad['ad_id']}`  
            **Cost:** {ad['cost']}  
            **Priority:** {ad['priority']}  
            **ML Score:** {ad['ml_score']}  
            **Final Score:** {ad['final_score']}  

            🧠 **Why selected?**  
            {ad['reason']}
            """)
