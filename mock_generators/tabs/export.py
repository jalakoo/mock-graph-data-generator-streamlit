import streamlit as st

def export_tab():
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/export.gif")
    with col2:
        st.write("Export generated data and download.")
    st.markdown("--------")

    ec1, ec2 = st.columns(2)
    with ec1:
        st.write("Export generated data")
        st.button("Export")