import streamlit as st
import pandas as pd
from salesforce_api import describe_object

def show_describe_object(sf):
    st.subheader("Describe Salesforce Object")
    object_name = st.text_input("Enter Salesforce Object API Name (e.g., Account)")
    if st.button("Describe Object"):
        result = describe_object(sf, object_name)
        if result['success']:
            fields = result['fields']
            df = pd.DataFrame(fields)
            st.dataframe(df)
        else:
            st.error(f"Failed to describe object: {result['message']}")
