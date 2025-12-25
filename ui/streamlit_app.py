import streamlit as st
import requests

# ================= CONFIG =================
BACKEND_URL = "http://127.0.0.1:8000/decide-ads"
# Render backend ke liye:
# BACKEND_URL = "https://ads-optimization-engine.onrender.com/decide-ads"

st.set_page_config(
    page_title="Ads Optimization Engine",
    layout="wide"
)

# ================= HEADER =================
st.title("Ads Optimization Engine")
st.caption("Explainable ML-driven Ad Selection System")

st.markdown(
    """
This tool helps you **select the most effective advertisements** within a fixed budget.

### What you do:
- Enter campaign budget  
- Provide ad details  

### What the system does:
- Uses ML + business rules  
- Ranks ads  
- Explains *why* an ad is recommended  
"""
)

st.divider()

# ================= INPUT SECTION =================
st.subheader("1️⃣ Campaign Configuration")

total_budget = st.number_input(
    "Total Campaign Budget",
    min_value=1.0,
    value=500.0,
    help="Maximum total amount you want to spend on ads"
)

ad_count = st.number_input(
    "Number of Ads",
    min_value=1,
    value=1,
    step=1,
    help="How many ads you want to evaluate"
)

st.divider()

# ================= AD DETAILS =================
st.subheader("2️⃣ Ad Details")
st.caption(
    "Provide information for each ad. These details help the ML engine "
    "estimate performance, importance, and cost efficiency."
)

ads = []

for i in range(ad_count):
    with st.expander(f"Ad {i + 1}", expanded=True):

        st.markdown("**🆔 Ad Identifier**")
        st.caption("A unique name or ID to identify this advertisement.")
        ad_id = st.text_input(
            "Ad ID",
            value=f"ad_{i+1}",
            key=f"ad_id_{i}"
        )

        st.markdown("**💰 Ad Cost**")
        st.caption("How much budget is required to run this ad.")
        cost = st.number_input(
            "Cost",
            min_value=1.0,
            value=50.0,
            key=f"cost_{i}"
        )

        st.markdown("**⭐ Business Priority**")
        st.caption(
            "How important this ad is for the business:\n\n"
            "- **3** → High priority\n"
            "- **2** → Medium priority\n"
            "- **1** → Low priority"
        )
        priority = st.selectbox(
            "Priority",
            [1, 2, 3],
            index=2,
            key=f"priority_{i}"
        )

        st.markdown("**👆 Clicks**")
        st.caption(
            "Estimated or historical number of clicks this ad receives.\n"
            "Higher clicks usually mean more user interest."
        )
        clicks = st.number_input(
            "Clicks",
            min_value=0,
            value=100,
            key=f"clicks_{i}"
        )

        st.markdown("**🎯 Conversions**")
        st.caption(
            "Number of successful outcomes from clicks "
            "(e.g., purchases, sign-ups)."
        )
        conversions = st.number_input(
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

# ================= SUBMIT =================
if st.button("🚀 Optimize Ads"):
    payload = {
        "total_budget": total_budget,
        "ads": ads
    }

    try:
        with st.spinner("Running optimization engine..."):
            response = requests.post(
                BACKEND_URL,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

    except Exception as e:
        st.error("Unable to reach backend service.")
        st.stop()

    if not result.get("success"):
        st.error(result.get("error", "Something went wrong"))
        st.stop()

    # ================= OUTPUT =================
    st.success("Optimization Completed Successfully")

    st.subheader("3️⃣ Summary")
    col1, col2 = st.columns(2)
    col1.metric("Total Cost Used", result["total_cost"])
    col2.metric("Remaining Budget", result["remaining_budget"])

    st.divider()

    st.subheader("4️⃣ Recommended Ads (Ranked)")

    for ad in result["selected_ads"]:
        with st.expander(f"Rank {ad['rank']} — {ad['label']}"):
            st.write(f"**Ad ID:** {ad['ad_id']}")
            st.write(f"**Cost:** {ad['cost']}")
            st.write(f"**Priority:** {ad['priority']}")
            st.write(f"**ML Score:** {ad['ml_score']}")
            st.write(f"**Final Score:** {ad['final_score']}")
            st.info(ad["reason"])

    st.divider()
    st.subheader("Raw Backend Response")
    st.json(result)
