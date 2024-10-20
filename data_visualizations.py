import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

def visualize_data(sf):
    st.subheader("Salesforce Data Visualizations")

    # Store the query input and other stateful components in session state
    if 'soql_query' not in st.session_state:
        st.session_state.soql_query = ""
    if 'records' not in st.session_state:
        st.session_state.records = None
    if 'chart_type' not in st.session_state:
        st.session_state.chart_type = "Bar Chart"  # Set a default chart type only if not present

    # Allow the user to input a SOQL query and store it in session state
    soql_query = st.text_area("Enter SOQL Query for Visualization", st.session_state.soql_query)
    st.session_state.soql_query = soql_query  # Update session state when user inputs query

    # Button to fetch and display data
    if st.button("Run Query"):
        try:
            # Retrieve records using the user-provided SOQL query
            results = sf.query(soql_query)
            records = results.get('records', [])

            if records:
                # Clean and convert the records into a pandas DataFrame
                df = pd.json_normalize(records)
                st.session_state.records = df  # Store the DataFrame in session state

                st.success(f"Query successful. {len(df)} records fetched.")
                st.write(df.head())  # Display the first few rows for user reference

            else:
                st.error("No records returned.")
                st.session_state.records = None

        except Exception as e:
            st.error(f"Failed to execute query: {str(e)}")
            st.session_state.records = None

    # If records are available, display the visualization options
    if st.session_state.records is not None:
        df = st.session_state.records

        # Allow the user to choose the chart type
        chart_type = st.selectbox("Select Chart Type", ['Bar Chart', 'Pie Chart', 'Line Chart'], index=0, key='chart_type')

        # Allow users to dynamically select fields for x, y, or labels based on the available DataFrame columns
        st.write("Choose fields for visualization:")

        if chart_type == 'Bar Chart':
            x_axis = st.selectbox("Select X-Axis", df.columns, key='bar_x')
            y_axis = st.selectbox("Select Y-Axis", df.columns, key='bar_y')

            # Create and display the Bar Chart
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
            st.plotly_chart(fig)

        elif chart_type == 'Pie Chart':
            labels = st.selectbox("Select Labels", df.columns, key='pie_labels')

            # Dynamically identify the column name of the numeric field (usually 'expr0' for COUNT)
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

            if numeric_columns:
                values = st.selectbox("Select Values", numeric_columns, key='pie_values')

                # Create and display the Pie Chart
                try:
                    fig, ax = plt.subplots()
                    ax.pie(df[values], labels=df[labels], autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error creating pie chart: {str(e)}")
            else:
                st.error("No numeric fields available for values in the pie chart.")

        elif chart_type == 'Line Chart':
            x_axis = st.selectbox("Select X-Axis", df.columns, key='line_x')
            y_axis = st.selectbox("Select Y-Axis", df.columns, key='line_y')

            # Create and display the Line Chart
            fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
            st.plotly_chart(fig)

    else:
        st.warning("No data available for visualization. Please enter a query and run it.")
