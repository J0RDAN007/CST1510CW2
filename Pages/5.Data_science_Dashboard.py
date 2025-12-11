import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Data Science Dashboard", layout="wide")

# Check login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/1.Login.py")
    st.stop()

st.title("Data Science Dashboard")
st.write(f"User: {st.session_state.username} | Role: {st.session_state.role}")

# You can create a sample dataset CSV or use existing data
# For now, let's create sample data in the code

st.write("## Dataset Management")

# Create sample data
datasets = pd.DataFrame({
    'dataset_name': ['Network Logs', 'User Activity', 'System Metrics', 'Security Events', 'Application Logs'],
    'source_department': ['IT', 'IT', 'Operations', 'Security', 'Development'],
    'file_size_mb': [250, 120, 85, 300, 75],
    'row_count': [1000000, 500000, 250000, 1500000, 300000],
    'quality_score': [85, 92, 78, 88, 95],
    'is_archived': [0, 0, 1, 0, 1],
    'last_accessed': ['2024-01-10', '2024-01-09', '2024-01-05', '2024-01-10', '2024-01-03']
})

# Analysis
st.subheader("Dataset Analysis")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Datasets", len(datasets))
    st.metric("Total Data Size", f"{datasets['file_size_mb'].sum():.0f} MB")

with col2:
    st.metric("Average Quality Score", f"{datasets['quality_score'].mean():.1f}%")
    st.metric("Archived Datasets", f"{datasets['is_archived'].sum()}")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data by Department")
    dept_counts = datasets['source_department'].value_counts().reset_index()
    dept_counts.columns = ['source_department', 'count']
    fig1 = px.bar(dept_counts, x='source_department', y='count')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Dataset Quality Distribution")
    fig2 = px.histogram(datasets, x='quality_score', nbins=10)
    st.plotly_chart(fig2, use_container_width=True)

# Data table
st.subheader("Dataset Details")
st.dataframe(datasets, use_container_width=True)

# Recommendations
st.subheader("Recommendations")
st.write("1. Archive System Metrics (lowest quality score: 78%)")
st.write("2. Compress Network Logs (largest dataset: 250MB)")
st.write("3. Backup Security Events (critical operational data)")

# Navigation
st.markdown("---")
if st.button("← Back to Home"):
    st.switch_page("app.py")