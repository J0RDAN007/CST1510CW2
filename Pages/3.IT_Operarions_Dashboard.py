import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="IT Operations Dashboard", layout="wide")

# Check login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/1.Login.py")
    st.stop()

st.title("IT Operations Dashboard")
st.write(f"User: {st.session_state.username} | Role: {st.session_state.role}")

# Load CSV 
@st.cache_data
def load_data():
    # Project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    csv_path = os.path.join(project_root, "DATA", "it_tickets.csv")

    if not os.path.exists(csv_path):
        st.error(f"CSV file not found at {csv_path}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(csv_path)
        return df
    except pd.errors.EmptyDataError:
        st.error("CSV file is empty or corrupted. Check DATA/it_tickets.csv")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading CSV: {str(e)}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available. Please check:")
    st.write("1. Make sure `DATA/it_tickets.csv` exists")
    st.write("2. File should have this exact header line:")
    st.code("ticket_id,priority,description,status,assigned_to,created_at,resolution_time_hours")
    st.write("3. File should not be empty")
    st.stop()

# Show debug info
st.write(f"**Loaded {len(df)} records**")
st.write(f"**Columns:** {list(df.columns)}")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    priority_filter = st.multiselect("Priority", df['priority'].unique())
    status_filter = st.multiselect("Status", df['status'].unique())
    assigned_filter = st.multiselect("Assigned To", df['assigned_to'].unique())

# Apply filters
filtered_df = df.copy()
if priority_filter:
    filtered_df = filtered_df[filtered_df['priority'].isin(priority_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
if assigned_filter:
    filtered_df = filtered_df[filtered_df['assigned_to'].isin(assigned_filter)]

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Tickets", len(filtered_df))
with col2:
    open_tickets = len(filtered_df[filtered_df['status'] == 'Open'])
    st.metric("Open Tickets", open_tickets)
with col3:
    waiting_tickets = len(filtered_df[filtered_df['status'] == 'Waiting for User'])
    st.metric("Waiting for User", waiting_tickets)

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tickets by Priority")
    if 'priority' in filtered_df.columns:
        priority_counts = filtered_df['priority'].value_counts().reset_index()
        priority_counts.columns = ['priority', 'count']
        fig1 = px.bar(priority_counts, x='priority', y='count', title="Tickets by Priority")
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Tickets by Status")
    if 'status' in filtered_df.columns:
        status_counts = filtered_df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        fig2 = px.pie(status_counts, values='count', names='status', title="Tickets by Status")
        st.plotly_chart(fig2, use_container_width=True)

# Staff performance analysis
st.subheader("Staff Performance Analysis")
if 'assigned_to' in filtered_df.columns and 'resolution_time_hours' in filtered_df.columns:
    staff_perf = filtered_df.groupby('assigned_to').agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean'
    }).reset_index()
    staff_perf.columns = ['Staff', 'Ticket Count', 'Avg Resolution (hrs)']
    
    # Find staff with longest resolution time
    slowest_staff = staff_perf.loc[staff_perf['Avg Resolution (hrs)'].idxmax()]
    st.write(f"**Slowest Staff Member:** {slowest_staff['Staff']} (Avg: {slowest_staff['Avg Resolution (hrs)']:.1f} hours)")
    
    st.dataframe(staff_perf, use_container_width=True)

# Data table
st.subheader("Ticket Details")
st.dataframe(filtered_df, use_container_width=True)

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("← Cybersecurity Dashboard"):
        st.switch_page("pages/2.Cybersecurity_Dashboard.py")
with col2:
    if st.button("Data Science →"):
        st.switch_page("pages/5.Data_Science_Dashboard.py")
