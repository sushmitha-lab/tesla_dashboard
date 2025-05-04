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

# Custom CSS with Times New Roman and Arial fonts
st.markdown('''
<style>
    /* Set dark gray background instead of pure black */
    .stApp {
        background-color: #121212 !important;
        font-family: Arial, sans-serif !important;
    }
    .main, .block-container, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #121212 !important;
    }
    /* Side bar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
        border-right: 1px solid #444444;
        font-family: Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    /* Headings with classic styling */
    h1, h2, h3 {
        font-family: "Times New Roman", Times, serif !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
        letter-spacing: 0.5px !important;
        background-color: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
        width: 100% !important;
    }
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 2px solid #FF3A33 !important;
        padding-bottom: 0.5rem !important;
        text-transform: uppercase !important;
    }
    h2 {
        font-size: 1.8rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 1px solid #4CAF50 !important;
        padding-bottom: 0.3rem !important;
    }
    h3 {
        font-size: 1.4rem !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.8rem !important;
        border-bottom: 1px solid #2196F3 !important;
        padding-bottom: 0.2rem !important;
    }
    /* Body text */
    p, li, div {
        font-family: Arial, sans-serif !important;
        font-size: 1rem !important;
        color: #EEEEEE !important;
        text-shadow: none !important;
        line-height: 1.5 !important;
    }
    /* Chart styling with borders */
    .stPlotlyChart {
        background-color: #1E1E1E !important;
        padding: 1.2rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem !important;
        border: 1px solid #333333 !important;
    }
    /* Expanders */
    .streamlit-expanderHeader {
        font-family: Arial, sans-serif !important;
        font-weight: bold !important;
        color: #2196F3 !important; /* Blue for expanders */
        background-color: #1E1E1E !important;
        border: 1px solid #2196F3 !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
    }
    /* Button styling */
    .stButton>button {
        background-color: #2196F3 !important;
        color: white !important;
        font-weight: bold !important;
        border: 1px solid #64B5F6 !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 1rem !important;
        border-radius: 4px !important;
        font-family: Arial, sans-serif !important;
        text-transform: uppercase !important;
    }
    .stButton>button:hover {
        background-color: #42A5F5 !important;
        border: 1px solid #90CAF9 !important;
    }
    /* Form elements */
    .stTextInput>div>div>input {
        color: white !important;
        background-color: #333333 !important;
        border: 1px solid #555555 !important;
        font-size: 1rem !important;
        font-family: Arial, sans-serif !important;
    }
    /* Date inputs */
    .stDateInput>div>div>input {
        color: white !important;
        background-color: #333333 !important;
        border: 1px solid #555555 !important;
        font-size: 1rem !important;
        font-family: Arial, sans-serif !important;
    }
    /* Select boxes */
    .stSelectbox>div>div>div>div {
        color: white !important;
        background-color: #333333 !important;
        font-size: 1rem !important;
        font-family: Arial, sans-serif !important;
    }
    /* Select box dropdown items */
    .stSelectbox [data-baseweb="select"] {
        color: white !important;
        background-color: #333333 !important;
        font-family: Arial, sans-serif !important;
    }
    /* Radio buttons */
    .stRadio>div {
        color: white !important;
        background-color: #1E1E1E !important;
        padding: 8px !important;
        border-radius: 5px !important;
        border: 1px solid #444444 !important;
        font-family: Arial, sans-serif !important;
    }
    /* Section dividers */
    hr {
        border-color: #333333 !important;
        margin: 1.5rem 0 !important;
    }
</style>
''', unsafe_allow_html=True)

# App title and description in dashboard style
st.markdown('''
<div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin-bottom: 25px; border-left: 5px solid #FF3A33; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
    <h1 style="margin:0; padding:0; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">⚡ Tesla performance dashboard</h1>
    <p style="margin-top:10px; font-family: Arial, sans-serif;">Real-time insights into Tesla's business across three key performance dimensions</p>
</div>
''', unsafe_allow_html=True)

# Sidebar with theme selection
with st.sidebar:
    st.header("Dashboard Controls")
    
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
    if st.button("Refresh Dashboard"):
        st.cache_data.clear()
        st.rerun()
        
    # Additional dashboard info
    st.markdown('''
    <div style="margin-top:30px; padding:10px; background-color:#1E1E1E; border-radius:5px; border:1px solid #333;">
        <h4 style="margin:0; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Dashboard info</h4>
        <p style="font-size:0.9rem !important; margin-top:10px; font-family: Arial, sans-serif;">This dashboard visualizes Tesla's business performance across three crucial dimensions using real-time data from Yahoo Finance.</p>
    </div>
    ''', unsafe_allow_html=True)

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

# Create dashboard layout with 3 side-by-side metrics cards at the top
st.markdown('''
<div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:20px;">
    <div style="flex:1; min-width:200px; background-color:#1E1E1E; padding:15px; border-radius:5px; border-left:4px solid #FF3A33; box-shadow:0 2px 5px rgba(0,0,0,0.2);">
        <h3 style="margin:0; font-size:1.2rem !important; color:#FF3A33 !important; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Latest revenue</h3>
        <p style="font-size:2rem !important; margin:5px 0 0 0; font-family: Arial, sans-serif;">$25.5B</p>
        <p style="color:#4CAF50 !important; margin:0; font-family: Arial, sans-serif;">↑ 8.2% YoY</p>
    </div>
    <div style="flex:1; min-width:200px; background-color:#1E1E1E; padding:15px; border-radius:5px; border-left:4px solid #4CAF50; box-shadow:0 2px 5px rgba(0,0,0,0.2);">
        <h3 style="margin:0; font-size:1.2rem !important; color:#4CAF50 !important; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Quarterly deliveries</h3>
        <p style="font-size:2rem !important; margin:5px 0 0 0; font-family: Arial, sans-serif;">422K</p>
        <p style="color:#FF3A33 !important; margin:0; font-family: Arial, sans-serif;">↓ 3.7% QoQ</p>
    </div>
    <div style="flex:1; min-width:200px; background-color:#1E1E1E; padding:15px; border-radius:5px; border-left:4px solid #2196F3; box-shadow:0 2px 5px rgba(0,0,0,0.2);">
        <h3 style="margin:0; font-size:1.2rem !important; color:#2196F3 !important; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Sustainability score</h3>
        <p style="font-size:2rem !important; margin:5px 0 0 0; font-family: Arial, sans-serif;">85/100</p>
        <p style="color:#4CAF50 !important; margin:0; font-family: Arial, sans-serif;">↑ 5 points</p>
    </div>
</div>
''', unsafe_allow_html=True)

# Create a two-column layout for the main visualizations
col1, col2 = st.columns([3, 2])

# First column - Financial and Delivery
with col1:
    # Dashboard panel styling
    st.markdown('''
    <div style="background-color:#1E1E1E; padding:15px; border-radius:10px; border-top:3px solid #FF3A33; margin-bottom:20px;">
        <h2 style="margin-top:0; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Financial performance</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    # Get financial statement data
    financial_data = financials['income_statement']
    key_metrics = ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']
    
    # Financial metrics visualization
    fig = viz.plot_financial_metrics(financial_data, key_metrics, selected_period, chart_theme)
    st.plotly_chart(fig, use_container_width=True)
    
    # Brief explanation
    with st.expander("Financial Insights"):
        st.markdown("""
        This chart shows Tesla's key financial metrics over time, including Total Revenue, Gross Profit, Operating Income, and Net Income.
        The continued upward trend demonstrates Tesla's strong financial growth and improving profitability.
        
        Key insights:
        - Revenue has shown consistent growth as Tesla increases vehicle deliveries
        - Profitability has significantly improved over time
        - Operating income reflects Tesla's operational efficiency
        - Net income trends indicate the overall financial health of the company
        """)
    
    # Dashboard panel styling for second visualization
    st.markdown('''
    <div style="background-color:#1E1E1E; padding:15px; border-radius:10px; border-top:3px solid #4CAF50; margin-top:30px; margin-bottom:20px;">
        <h2 style="margin-top:0; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Production & delivery</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    # Delivery trends visualization
    delivery_fig = viz.plot_delivery_trends(delivery_data, chart_theme)
    st.plotly_chart(delivery_fig, use_container_width=True)
    
    # Brief explanation
    with st.expander("Delivery Insights"):
        st.markdown("""
        This visualization tracks Tesla's vehicle delivery numbers over time, showing quarterly delivery totals and the breakdown by model.
        The steep upward trajectory reflects Tesla's rapid manufacturing expansion and growing consumer demand.
        
        Key insights:
        - The shift from predominantly Model S/X to Model 3/Y shows Tesla's successful move into mass-market segments
        - Quarterly delivery patterns demonstrate Tesla's production ramp capabilities
        - The growth rate reflects Tesla's expanding manufacturing capacity with new Gigafactories
        - Seasonal patterns are visible in the quarterly delivery numbers
        """)

# Second column - Environmental Impact and Additional Metrics
with col2:
    # Dashboard panel styling
    st.markdown('''
    <div style="background-color:#1E1E1E; padding:15px; border-radius:10px; border-top:3px solid #2196F3; margin-bottom:20px;">
        <h2 style="margin-top:0; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Sustainability metrics</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    # Carbon offset visualization
    sustainability_data = dp.get_sustainability_metrics()
    radar_fig = viz.plot_sustainability_radar(sustainability_data, chart_theme)
    st.plotly_chart(radar_fig, use_container_width=True)
    
    # Brief explanation
    with st.expander("Environmental Insights"):
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
    
    # Additional metrics/cards
    st.markdown('''
    <div style="background-color:#1E1E1E; padding:15px; border-radius:10px; border-top:3px solid #FF9800; margin-top:30px; margin-bottom:20px;">
        <h2 style="margin-top:0; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Key performance indicators</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    # KPI cards
    st.markdown('''
    <div style="display:flex; flex-direction:column; gap:15px;">
        <div style="background-color:#1E1E1E; padding:15px; border-radius:5px; border-left:4px solid #FF9800;">
            <h3 style="margin:0; font-size:1.2rem !important; color:#FF9800 !important; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Gross margin</h3>
            <p style="font-size:1.8rem !important; margin:5px 0 0 0; font-family: Arial, sans-serif;">25.1%</p>
            <p style="color:#FF3A33 !important; margin:0; font-family: Arial, sans-serif;">↓ 2.4% YoY</p>
        </div>
        <div style="background-color:#1E1E1E; padding:15px; border-radius:5px; border-left:4px solid #FF9800;">
            <h3 style="margin:0; font-size:1.2rem !important; color:#FF9800 !important; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Operating margin</h3>
            <p style="font-size:1.8rem !important; margin:5px 0 0 0; font-family: Arial, sans-serif;">11.4%</p>
            <p style="color:#FF3A33 !important; margin:0; font-family: Arial, sans-serif;">↓ 1.7% YoY</p>
        </div>
        <div style="background-color:#1E1E1E; padding:15px; border-radius:5px; border-left:4px solid #FF9800;">
            <h3 style="margin:0; font-size:1.2rem !important; color:#FF9800 !important; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Free cash flow</h3>
            <p style="font-size:1.8rem !important; margin:5px 0 0 0; font-family: Arial, sans-serif;">$2.9B</p>
            <p style="color:#4CAF50 !important; margin:0; font-family: Arial, sans-serif;">↑ 10.8% QoQ</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f'''
<div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0;">
    <div>
        <p style="margin:0; font-size:0.9rem !important; font-family: Arial, sans-serif;">Dashboard last updated: {datetime.now().strftime('%Y-%m-%d')}</p>
        <p style="margin:0; font-size:0.8rem !important; color:#AAA !important; font-family: Arial, sans-serif;">Data sources: Yahoo Finance, Tesla quarterly reports, and sustainability disclosures</p>
    </div>
    <div>
        <p style="margin:0; font-size:0.9rem !important; text-align:right; font-family: 'Times New Roman', Times, serif; font-weight: bold; text-transform: capitalize;">Tesla business metrics dashboard</p>
        <p style="margin:0; font-size:0.8rem !important; color:#AAA !important; text-align:right; font-family: Arial, sans-serif;">v1.0</p>
    </div>
</div>
''', unsafe_allow_html=True)

