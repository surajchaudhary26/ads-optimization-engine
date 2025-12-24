import streamlit as st
from config import APP_TITLE, APP_SUBTITLE, BACKEND_URL
from layout import render_header, render_input_section, render_results
from api import call_backend

st.set_page_config(
    page_title="Ads Optimization Engine",
    layout="centered"
)

render_header(APP_TITLE, APP_SUBTITLE)

payload = render_input_section()

if st.button("🚀 Optimize Ads"):
    with st.spinner("Optimizing ads using ML..."):
        try:
            response = call_backend(payload, BACKEND_URL)

            if response["success"]:
                render_results(response)
            else:
                st.error(response["error"])

        except Exception as e:
            st.error("Unable to reach backend service. Please try again later.")
