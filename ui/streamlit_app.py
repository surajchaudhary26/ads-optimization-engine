import streamlit as st
from ui.config import APP_TITLE, APP_SUBTITLE
from ui.layout import render_header, render_input_section, render_results
from ui.api import decide_ads

st.set_page_config(layout="wide")

render_header(APP_TITLE, APP_SUBTITLE)

payload = render_input_section()

if st.button("Optimize Ads"):
    with st.spinner("Running optimization..."):
        try:
            response = decide_ads(payload)
            if response["success"]:
                render_results(response)
            else:
                st.error(response["error"])
        except Exception as e:
            st.error("Unable to reach backend service")
