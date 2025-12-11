import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

# Check login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/1.Login.py")
    st.stop()

st.title("Cybersecurity Dashboard")
st.write(f"User: {st.session_state.username} | Role: {st.session_state.role}")

# --- Load CSV ---
@st.cache_data
def load_data():
    # Project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    csv_path = os.path.join(project_root, "DATA", "cyber_incidents.csv")

    if not os.path.exists(csv_path):
        st.error(f"CSV file not found at {csv_path}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(csv_path)
        # YOUR CSV has: incident_id,timestamp,severity,category,status,description
        return df
    except Exception as e:
        st.error(f"Error reading CSV: {str(e)}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available. Check DATA/cyber_incidents.csv")
else:
    # Show debug info
    st.write(f"**Loaded {len(df)} records**")
    st.write(f"**Columns:** {list(df.columns)}")
    
    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        severity_filter = st.multiselect("Severity", df['severity'].unique())
        status_filter = st.multiselect("Status", df['status'].unique())
        category_filter = st.multiselect("Category", df['category'].unique())
    
    # Apply filters
    filtered_df = df.copy()
    if severity_filter:
        filtered_df = filtered_df[filtered_df['severity'].isin(severity_filter)]
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    if category_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
    
    # Metrics - Using YOUR CSV columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Incidents", len(filtered_df))
    with col2:
        open_incidents = len(filtered_df[filtered_df['status'] == 'Open'])
        st.metric("Open Incidents", open_incidents)
    with col3:
        critical_incidents = len(filtered_df[filtered_df['severity'] == 'Critical'])
        st.metric("Critical Incidents", critical_incidents)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Incidents by Category")
        if 'category' in filtered_df.columns:
            category_counts = filtered_df['category'].value_counts().reset_index()
            category_counts.columns = ['category', 'count']
            fig1 = px.bar(category_counts, x='category', y='count', title="Incidents by Category")
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Incidents by Severity")
        if 'severity' in filtered_df.columns:
            severity_counts = filtered_df['severity'].value_counts().reset_index()
            severity_counts.columns = ['severity', 'count']
            fig2 = px.pie(severity_counts, values='count', names='severity', title="Incidents by Severity")
            st.plotly_chart(fig2, use_container_width=True)
    
    # Phishing Analysis (for coursework requirement)
    st.subheader("Phishing Analysis")
    phishing_df = filtered_df[filtered_df['category'] == 'Phishing']
    if not phishing_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Phishing", len(phishing_df))
        with col2:
            open_phishing = len(phishing_df[phishing_df['status'] == 'Open'])
            st.metric("Open Phishing", open_phishing)
        with col3:
            recent_phishing = len(phishing_df[phishing_df['timestamp'] > '2025-01-01'])
            st.metric("2025 Phishing", recent_phishing)
    
    # Data table
    st.subheader("Incident Details")
    st.dataframe(filtered_df, use_container_width=True)

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("← Back to Home"):
        st.switch_page("app.py")
with col2:
    if st.button("IT Dashboard →"):
        st.switch_page("pages/3.IT_Operations_Dashboard.py")