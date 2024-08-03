import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import datetime
from PIL import Image

# Set page config
st.set_page_config(layout="wide", page_title="Chatbot User Engagement Analytics")

# Load and display Ryde Council NSW logo
logo = Image.open("assets/ryde_council_logo.png")
st.image(logo, width=200)

# Generate dummy data
def generate_dummy_data():
    np.random.seed(42)
    
    # User data
    user_data = pd.DataFrame({
        'user_id': range(1000),
        'login_date': [datetime.date(2024, 8, 1) + datetime.timedelta(days=np.random.randint(0, 30)) for _ in range(1000)],
        'session_duration': np.random.randint(60, 600, 1000),
        'age_group': np.random.choice(['18-24', '25-34', '35-44', '45-54', '55+'], 1000),
        'qr_scan': np.random.choice([True, False], 1000, p=[0.8, 0.2])
    })
    
    # Query data
    categories = ['Council Services', 'Development & Planning', 'Environment & Waste', 'Community & Events', 'Transport & Parking']
    questions = [
        "How can I report illegal dumping in my neighborhood?",
        "What's the process for objecting to a development application?",
        "Council's Future Vision",
        "How do I contact the councillor?",
        "What youth programs are available during school holidays?",
        "How can I book a community hall for an event?",
        "What's the council doing about traffic congestion on Victoria Road?",
        "How can I get involved in local environmental initiatives?",
        "When will the next council meeting be held and can I attend?",
        "What support services are available for seniors in Ryde?",
        "How do I register my pet with the council?",
        "What are the rules for tree removal on private property?",
        "How can I report a missed garbage collection?",
        "What's the process for starting a new business in Ryde?",
        "How do I appeal a parking fine?"
    ]
    query_data = pd.DataFrame({
        'user_id': np.random.choice(user_data['user_id'], 2000),
        'category': np.random.choice(categories, 2000),
        'question': np.random.choice(questions, 2000),
        'response_time': np.random.uniform(0.5, 3, 2000),
        'error': np.random.choice([True, False], 2000, p=[0.03, 0.97]),
    })
    
    # Grievance data
    grievance_types = ['Infrastructure', 'Environmental', 'Safety', 'Community Services', 'Planning & Development']
    grievances = [
        'Pothole on Main Street', 'Overflowing bins in Central Park', 'Broken streetlight on Elm Avenue',
        'Noise complaint about late-night construction', 'Request for more bike lanes',
        'Graffiti on public building', 'Dangerous tree limb overhanging walkway',
        'Request for additional disability parking spaces', 'Concerns about new high-rise development',
        'Inadequate flood prevention measures', 'Lack of youth programs in community center',
        'Speeding vehicles in school zone', 'Poor maintenance of public toilets',
        'Request for more frequent bus services', 'Illegal dumping in nature reserve'
    ]
    grievance_data = pd.DataFrame({
        'user_id': np.random.choice(user_data['user_id'], 500),
        'type': np.random.choice(grievance_types, 500),
        'grievance': np.random.choice(grievances, 500),
        'lodged_date': [datetime.date(2024, 8, 1) + datetime.timedelta(days=np.random.randint(0, 30)) for _ in range(500)]
    })
    
    return user_data, query_data, grievance_data

# Load dummy data
user_data, query_data, grievance_data = generate_dummy_data()

# Dashboard title
st.title("Chatbot User Engagement Analytics")

# Create tabs
tab1, tab2 = st.tabs(["User Engagement", "Grievance Tracking"])

with tab1:
    # User Engagement Overview
    st.header("User Engagement Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Logins", len(user_data))
    with col2:
        st.metric("Unique Users", user_data['user_id'].nunique())
    with col3:
        avg_duration = user_data['session_duration'].mean()
        st.metric("Avg. Session Duration", f"{avg_duration:.0f}s")
    with col4:
        return_rate = (user_data['user_id'].value_counts() > 1).mean()
        st.metric("Return User Rate", f"{return_rate:.1%}")

    st.markdown("---")

    # Query Distribution
    st.subheader("Query Distribution and Top FAQs by Chatbot Users")
    col1, col2 = st.columns(2)

    with col1:
        query_dist = query_data['category'].value_counts().sort_values(ascending=True)
        fig = px.bar(x=query_dist.values, y=query_dist.index, orientation='h',
                     labels={'x': 'Number of Queries', 'y': 'Category'},
                     color=query_dist.values,
                     color_continuous_scale=px.colors.sequential.Viridis,
                     title="Query Categories")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<h3 style='text-align: center;'><b>Top 10 FAQs</b></h3>", unsafe_allow_html=True)
        top_faqs = query_data['question'].value_counts().head(10).reset_index()
        top_faqs.columns = ['Query', '# of times asked']
        
        # Create a custom HTML table with alternating row colors and right-aligned "# of times asked"
        html_table = "<table style='width:100%; border-collapse: collapse;'>"
        html_table += "<tr><th style='text-align: left; padding: 8px;'>Query</th><th style='text-align: right; padding: 8px;'># of times asked</th></tr>"
        
        for i, (_, row) in enumerate(top_faqs.iterrows()):
            bg_color = "#f0f2f6" if i % 2 == 0 else "white"
            html_table += f"<tr style='background-color: {bg_color};'>"
            html_table += f"<td style='text-align: left; padding: 8px;'>{row['Query']}</td>"
            html_table += f"<td style='text-align: right; padding: 8px;'>{row['# of times asked']:,}</td>"
            html_table += "</tr>"
        
        html_table += "</table>"
        
        st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("---")

    # Chatbot Performance and QR Code Performance
    st.subheader("Chatbot and QR Code Performance")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg. Response Time", f"{query_data['response_time'].mean():.2f}s")
    with col2:
        st.metric("Error Rate", f"{(query_data['error'].mean() * 100):.2f}%")
    with col3:
        qr_scans = user_data['qr_scan'].sum()
        scan_rate = qr_scans / len(user_data)
        st.metric("QR Code Scans", qr_scans)
        st.metric("Scan-to-Login Rate", f"{scan_rate:.1%}")

    st.markdown("---")

    # User Demographics
    st.subheader("User Demographics")
    age_dist = user_data['age_group'].value_counts().sort_index()
    fig = px.bar(x=age_dist.index, y=age_dist.values, 
                 title="Age Distribution",
                 labels={'x': 'Age Group', 'y': 'Number of Users'},
                 color=age_dist.index,
                 color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Grievance Tracking")
    
    # Grievance Types
    st.subheader("Grievance Types")
    grievance_types = grievance_data['type'].value_counts().sort_values(ascending=True)
    fig = px.bar(x=grievance_types.values, y=grievance_types.index, orientation='h',
                 labels={'x': 'Number of Grievances', 'y': 'Type'},
                 color=grievance_types.values,
                 color_continuous_scale=px.colors.sequential.Viridis,
                 title="Grievance Types")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Top Grievances
    st.subheader("Top Grievances")
    top_grievances = grievance_data['grievance'].value_counts().head(10)
    fig = px.bar(x=top_grievances.values, y=top_grievances.index,
                 labels={'x': 'Number of Occurrences', 'y': 'Grievance'},
                 color=top_grievances.values,
                 color_continuous_scale=px.colors.sequential.Viridis,
                 title="Top 10 Specific Grievances")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Grievances Over Time
    st.subheader("Grievances Over Time")
    grievance_time = grievance_data.groupby('lodged_date').size().reset_index(name='count')
    fig = px.line(grievance_time, x='lodged_date', y='count', title="Daily Grievances")
    st.plotly_chart(fig, use_container_width=True)

# Date filter
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(user_data['login_date'].min(), user_data['login_date'].max()),
    min_value=user_data['login_date'].min(),
    max_value=user_data['login_date'].max()
)

# Apply date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    user_data = user_data[(user_data['login_date'] >= start_date) & (user_data['login_date'] <= end_date)]
    query_data = query_data[query_data['user_id'].isin(user_data['user_id'])]
    grievance_data = grievance_data[(grievance_data['lodged_date'] >= start_date) & (grievance_data['lodged_date'] <= end_date)]

st.sidebar.info("Note: This is a prototype using dummy data. Adjust the date range to see how the dashboard updates.")