import streamlit as st

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Tesla's Key Performance Metrics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

import utils
import data_processor as dp
import visualizations as viz

# Custom CSS to improve appearance with full black background and white headings
st.markdown('''
<style>
    /* Force full black background */
    .stApp {
        background-color: #000000 !important;
    }
    .main, .block-container, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    /* Side bar styling */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    /* Very visible white headings with contrast enhancement */
    h1, h2, h3 {
        font-weight: 900 !important; /* Extra bold */
        color: #FFFFFF !important; /* Pure white headings */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8); /* Shadow for contrast */
        letter-spacing: 0.5px; /* Slightly spaced letters */
    }
    h1 {
        font-size: 3rem !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 2px solid #FFFFFF;
        padding-bottom: 0.5rem;
    }
    h2 {
        font-size: 2.4rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 1px solid #555555;
        padding-bottom: 0.3rem;
    }
    h3 {
        font-size: 1.8rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
    }
    /* Text styling */
    p, li, div {
        font-size: 1.1rem !important;
        color: #FAFAFA !important;
    }
    /* Chart styling */
    .stPlotlyChart {
        background-color: #111111 !important;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        margin-bottom: 2rem !important;
        border: 1px solid #333333;
    }
    /* Make expanders more visible */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #00FF00 !important; /* Bright green for expanders */
        background-color: #111111 !important;
        border: 1px solid #333333;
        border-radius: 4px;
        padding: 0.5rem !important;
    }
    /* Button styling */
    .stButton>button {
        background-color: #444444 !important;
        color: white !important;
        font-weight: bold;
        border: 1px solid #666666 !important;
    }
    .stButton>button:hover {
        background-color: #666666 !important;
        border: 1px solid #888888 !important;
    }
    /* Force text inputs to have visible text */
    .stTextInput>div>div>input {
        color: white !important;
        background-color: #222222 !important;
    }
    /* Ensure select boxes have visible text */
    .stSelectbox>div>div>div>div {
        color: white !important;
        background-color: #222222 !important;
    }
</style>
''', unsafe_allow_html=True)

# App title and description
st.title("⚡ Tesla's Key Performance Metrics")
st.markdown("""This dashboard highlights Tesla's business performance through three impactful visualizations covering financial performance, 
production data, and environmental impact.
""")

# Sidebar with theme selection
with st.sidebar:
    st.header("Visualization Settings")
    
    # Date range selector
    st.subheader("Time Period")
    today = datetime.now()
    default_start = today - timedelta(days=365*5)  # 5 years ago by default
    start_date = st.date_input("Start Date", value=default_start)
    end_date = st.date_input("End Date", value=today)
    
    # Period selector for financial metrics
    st.subheader("Financial Analysis Period")
    period_options = ["Quarterly", "Annual"]
    selected_period = st.radio("Select Period", period_options)
    
    # Chart theme selection
    st.subheader("Chart Style")
    chart_theme = st.selectbox("Select Theme", ["plotly_dark", "plotly", "plotly_white"])

    # Data refresh button
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Load all required data
@st.cache_data(ttl=3600)
def load_tesla_data(start_date, end_date):
    return dp.get_stock_data("TSLA", start_date, end_date)

@st.cache_data(ttl=3600)
def load_financial_statements(period="quarterly"):
    return dp.get_financial_statements("TSLA", period)

@st.cache_data(ttl=3600)
def load_delivery_data():
    return dp.get_tesla_delivery_data()

@st.cache_data(ttl=3600)
def load_environmental_data():
    return dp.get_environmental_impact_data()

# Load data with loading indicators
with st.spinner("Loading data..."):
    # Load Tesla stock data
    tesla_data = load_tesla_data(start_date, end_date)
    
    # Load financial statements
    period_param = "quarterly" if selected_period == "Quarterly" else "annual"
    financials = load_financial_statements(period_param)
    
    # Load delivery data
    delivery_data = load_delivery_data()
    
    # Load environmental data
    environmental_data = dp.get_environmental_impact_data()

# Display the three key visualizations
st.header("1. Financial Performance: Key Metrics")

# Get financial statement data
financial_data = financials['income_statement']
key_metrics = ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']

# Financial metrics visualization
fig = viz.plot_financial_metrics(financial_data, key_metrics, selected_period, chart_theme)
st.plotly_chart(fig, use_container_width=True)

# Brief explanation
with st.expander("Financial Performance Insights"):
    st.markdown("""
    This chart shows Tesla's key financial metrics over time, including Total Revenue, Gross Profit, Operating Income, and Net Income.
    The continued upward trend demonstrates Tesla's strong financial growth and improving profitability.
    
    Key insights:
    - Revenue has shown consistent growth as Tesla increases vehicle deliveries
    - Profitability has significantly improved over time
    - Operating income reflects Tesla's operational efficiency
    - Net income trends indicate the overall financial health of the company
    """)

# Second visualization - Production & Delivery
st.header("2. Production & Delivery: Vehicle Delivery Trends")

# Delivery trends visualization
delivery_fig = viz.plot_delivery_trends(delivery_data, chart_theme)
st.plotly_chart(delivery_fig, use_container_width=True)

# Brief explanation
with st.expander("Production & Delivery Insights"):
    st.markdown("""
    This visualization tracks Tesla's vehicle delivery numbers over time, showing quarterly delivery totals and the breakdown by model.
    The steep upward trajectory reflects Tesla's rapid manufacturing expansion and growing consumer demand.
    
    Key insights:
    - The shift from predominantly Model S/X to Model 3/Y shows Tesla's successful move into mass-market segments
    - Quarterly delivery patterns demonstrate Tesla's production ramp capabilities
    - The growth rate reflects Tesla's expanding manufacturing capacity with new Gigafactories
    - Seasonal patterns are visible in the quarterly delivery numbers
    """)

# Third visualization - Environmental Impact
st.header("3. Environmental Impact: Carbon Offset & Sustainability")

# Carbon offset visualization
sustainability_data = dp.get_sustainability_metrics()
radar_fig = viz.plot_sustainability_radar(sustainability_data, chart_theme)
st.plotly_chart(radar_fig, use_container_width=True)

# Brief explanation
with st.expander("Environmental Impact Insights"):
    st.markdown("""
    This radar chart displays Tesla's various sustainability metrics, showing the company's performance across multiple environmental dimensions.
    Higher values indicate better performance in each sustainability category.
    
    Key insights:
    - Battery Recycling shows Tesla's commitment to circular resource use
    - Renewable Energy Use reflects Tesla's clean energy commitment in manufacturing
    - Water Recycling demonstrates factory water conservation efforts
    - Sustainable Materials shows progress in reducing the environmental impact of vehicle components
    - Carbon Footprint Reduction indicates Tesla's overall climate impact improvement
    """)

# Footer
st.markdown("---")
st.markdown(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d')}")
st.caption("Data sources: Yahoo Finance, Tesla quarterly reports, and sustainability disclosures")


# Footer
st.markdown("---")
st.markdown(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d')}")
st.caption("Data sources: Yahoo Finance, Tesla quarterly reports, and sustainability disclosures")
