import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from ui.config import APP_TITLE, APP_SUBTITLE
from ui.api import call_decide_ads
from ui.layout import render_input_section, render_output_section


st.set_page_config(
    page_title=APP_TITLE,
    layout="wide"
)

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.divider()

total_budget, ads = render_input_section()

st.divider()

if st.button("Decide Best Ads", type="primary"):
    payload = {
        "total_budget": total_budget,
        "ads": ads
    }

    with st.spinner("Optimizing ads using backend decision engine..."):
        try:
            response = call_decide_ads(payload)

            if response.get("success"):
                render_output_section(response)
            else:
                st.error(response.get("error", "Unknown error"))

        except Exception:
            st.error("Unable to reach backend service. Please try again later.")
