import streamlit as st
import json
import os
from simple_salesforce import Salesforce
from streamlit_option_menu import option_menu

# Importing module functions
from query_builder import show_query_builder
from data_import_export import show_data_import_export
from describe_object import show_describe_object
from search_salesforce import show_search_salesforce
from data_visualizations import visualize_data
from scheduled_jobs import view_scheduled_jobs
from audit_logs import view_audit_logs
from authentication import authenticate_salesforce_with_user

USER_DATA_FILE = 'user_data.json'

# Function to save user data
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f)

# Function to load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Registration page (in the main area, not the sidebar)
def register():
    st.title("Register")
    username = st.text_input("Salesforce Username")
    password = st.text_input("Salesforce Password", type="password")
    security_token = st.text_input("Salesforce Security Token", type="password")
    client_id = st.text_input("Salesforce Client ID")
    client_secret = st.text_input("Salesforce Client Secret", type="password")
    domain = st.selectbox("Salesforce Domain", ["login", "test"])
    pin = st.text_input("Set a 6-digit PIN", type="password", max_chars=6)

    if st.button("Register"):
        if len(pin) == 6 and pin.isdigit():
            user_data = {
                'username': username,
                'password': password,
                'security_token': security_token,
                'client_id': client_id,
                'client_secret': client_secret,
                'domain': domain,
                'pin': pin
            }
            save_user_data(user_data)
            st.success("Registration successful! Please login.")
            st.session_state['is_authenticated'] = False
        else:
            st.error("PIN must be 6 digits.")

# Login page (in the main area, not the sidebar)
def login():
    st.title("Login")
    user_data = load_user_data()
    if not user_data:
        st.error("No registered user found. Please register first.")
        return

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    pin = st.text_input("Enter your 6-digit PIN", type="password", max_chars=6)

    if st.button("Login"):
        if username == user_data.get('username') and password == user_data.get('password') and pin == user_data.get('pin'):
            st.session_state['is_authenticated'] = True
            st.session_state['salesforce'] = authenticate_salesforce_with_user(user_data)
            st.success("Login successful!")
            st.rerun()  # Rerun to refresh state
        else:
            st.error("Invalid credentials or PIN.")

# Logout function
def logout():
    st.session_state['is_authenticated'] = False
    st.session_state['salesforce'] = None
    st.rerun()

def main():
    if 'is_authenticated' not in st.session_state:
        st.session_state['is_authenticated'] = False

    # Sidebar: Only visible when logged in
    if st.session_state['is_authenticated']:
        with st.sidebar:
            st.title("Navigate")
            selected_module = option_menu("Main Menu", ["Home", "Query Builder", "Data Import/Export", "Describe Object",
                                                        "Search Salesforce", "Data Visualizations", "Scheduled Jobs Viewer", "Audit Logs Viewer"],
                                          icons=["house", "wrench", "upload", "book", "search", "bar-chart", "clock", "journal-whills"],
                                          menu_icon="cast", default_index=0)

            st.button("Logout", on_click=logout)

        # Load the selected module and pass the Salesforce instance
        sf = st.session_state.get('salesforce')
        modules = {
            'Home': lambda: st.subheader("Welcome to Salesforce Developer Utility"),
            'Query Builder': show_query_builder,
            'Data Import/Export': show_data_import_export,
            'Describe Object': show_describe_object,
            'Search Salesforce': show_search_salesforce,
            'Data Visualizations': visualize_data,
            'Scheduled Jobs Viewer': view_scheduled_jobs,
            'Audit Logs Viewer': view_audit_logs
        }

        # Run the selected module with Salesforce instance
        if selected_module == 'Home':
            modules[selected_module]()  # No need to pass sf for the Home module
        else:
            module_function = modules[selected_module]
            module_function(sf)  # Pass sf for all other modules
    
    # Main area: Show login/register if not authenticated
    else:
        options = ["Login", "Register"]
        activity = st.selectbox("Choose an action", options)

        if activity == "Login":
            login()
        elif activity == "Register":
            register()


if __name__ == "__main__":
    main()
