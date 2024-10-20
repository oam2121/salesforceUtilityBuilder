import streamlit as st
import pandas as pd
from salesforce_api import retrieve_records, create_record, update_record, delete_record

def show_query_builder(sf):
    query_action = st.sidebar.selectbox(
        "Query Actions",
        ['Fetch Records', 'Create Record', 'Update Record', 'Delete Record']
    )

    if query_action == 'Fetch Records':
        st.subheader("SOQL Query Runner")
        query = st.text_area("Enter SOQL Query", "SELECT Id, Name FROM Account LIMIT 10")
        if st.button("Run Query"):
            records = retrieve_records(sf, query)
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df)
            else:
                st.error("No records fetched or query failed.")

    elif query_action == 'Create Record':
        st.subheader("Create Record")
        sobject = st.text_input("Salesforce Object Type (e.g., Account)")
        record_details = st.text_area("Enter record details in dictionary format", "{}")
        if st.button("Create Record"):
            record_data = eval(record_details)
            result = create_record(sf, sobject, record_data)
            if result['success']:
                st.success(f"Record created successfully. ID: {result['id']}")
            else:
                st.error(f"Failed to create record: {result['message']}")

    elif query_action == 'Update Record':
        st.subheader("Update Record")
        sobject = st.text_input("Salesforce Object Type (e.g., Account)")
        record_id = st.text_input("Record ID")
        update_details = st.text_area("Enter update details in dictionary format", "{}")
        if st.button("Update Record"):
            update_data = eval(update_details)
            result = update_record(sf, sobject, record_id, update_data)
            if result['success']:
                st.success("Record updated successfully.")
            else:
                st.error(f"Failed to update record: {result['message']}")

    elif query_action == 'Delete Record':
        st.subheader("Delete Record")
        sobject = st.text_input("Salesforce Object Type (e.g., Account)")
        record_id = st.text_input("Record ID")
        if st.button("Delete Record"):
            result = delete_record(sf, sobject, record_id)
            if result['success']:
                st.success("Record deleted successfully.")
            else:
                st.error(f"Failed to delete record: {result['message']}")
