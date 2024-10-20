import streamlit as st
import pandas as pd

def show_search_salesforce(sf):
    st.subheader("Search Salesforce using SOSL")
    search_query = st.text_area("Enter SOSL Query (e.g., FIND {Test} IN ALL FIELDS RETURNING Account(Name))", "FIND {Test} IN ALL FIELDS RETURNING Account(Name)")
    if st.button("Run Search"):
        results = search_salesforce(sf, search_query)
        if results['success']:
            if results['records']:
                df = pd.DataFrame([{'Type': rec.get('attributes', {}).get('type', 'N/A'), 
                                    'Name': rec.get('Name', 'N/A'), 
                                    'Id': rec.get('Id', 'N/A')} for rec in results['records']])
                st.dataframe(df)
            else:
                st.warning("No records found.")
        else:
            st.error(f"Search failed: {results['message']}")

def search_salesforce(sf, sosl_query):
    """Search Salesforce using SOSL (Salesforce Object Search Language)."""
    try:
        results = sf.search(sosl_query)
        if 'searchRecords' in results and len(results['searchRecords']) > 0:
            return {'success': True, 'records': results['searchRecords']}
        else:
            return {'success': True, 'records': [], 'message': 'No records found'}
    except Exception as e:
        return {'success': False, 'message': str(e)}
