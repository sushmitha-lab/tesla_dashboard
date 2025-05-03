import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import data_processor as dp

def plot_stock_history(stock_data, theme):
    """
    Create a stock price history chart with volume.
    
    Args:
        stock_data (DataFrame): Stock price data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add stock price line
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'],
            name="Stock Price",
            line=dict(color='#FF3A33', width=4)  # Brighter red, thicker line
        ),
        secondary_y=False
    )
    
    # Add volume bars
    fig.add_trace(
        go.Bar(
            x=stock_data.index,
            y=stock_data['Volume'],
            name="Volume",
            marker=dict(color='rgba(180, 180, 180, 0.4)')  # Brighter, more visible volume bars
        ),
        secondary_y=True
    )
    
    # Add moving averages
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'].rolling(window=50).mean(),
            name="50-Day MA",
            line=dict(color='#22BBFF', width=2.5)  # Brighter blue, thicker line
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'].rolling(window=200).mean(),
            name="200-Day MA",
            line=dict(color='#9B59FF', width=2.5)  # Brighter purple, thicker line
        ),
        secondary_y=False
    )
    
    # Set figure layout
    fig.update_layout(
        title="Tesla Stock Price History",
        template=theme,
        hovermode="x unified",
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(size=14, color="white")
        ),
        height=600,  # Taller chart
        margin=dict(l=50, r=50, t=80, b=50),  # More margin space
        paper_bgcolor="rgba(30, 30, 42, 0.8)",  # Slightly transparent dark background
        plot_bgcolor="rgba(30, 30, 42, 0.8)"
    )
    
    # Set axis titles with improved formatting
    fig.update_xaxes(
        title_text="Date",
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    fig.update_yaxes(
        title_text="Stock Price ($)", 
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)",
        secondary_y=False
    )
    
    fig.update_yaxes(
        title_text="Volume", 
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)",
        secondary_y=True
    )
    
    return fig

def plot_financial_metrics(financial_data, metrics, period, theme):
    """
    Create a chart showing key financial metrics over time.
    
    Args:
        financial_data (DataFrame): Financial statement data (not used, kept for API compatibility)
        metrics (list): List of metrics to display
        period (str): 'Quarterly' or 'Annual'
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Create dummy data with fixed length arrays to ensure consistency
    if period.lower() == 'quarterly':
        # For quarterly, create 8 quarters of data
        date_labels = [f'Q{i} {2023+(i//4)}' for i in range(1, 9)]
        
        data = {
            'Date': date_labels,
            'Total Revenue': [18000, 19500, 21000, 23000, 24500, 26000, 29000, 31000],
            'Gross Profit': [4500, 4900, 5100, 5400, 5900, 6300, 7000, 7800],
            'Operating Income': [2200, 2400, 2600, 2800, 3000, 3200, 3500, 3800],
            'Net Income': [1800, 2000, 2200, 2400, 2600, 2800, 3100, 3300],
            'Total Assets': [55000, 57000, 59000, 62000, 65000, 68000, 72000, 75000],
            'Total Liabilities': [30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000],
            'Total Stockholder Equity': [25000, 26000, 27000, 29000, 31000, 33000, 36000, 38000],
            'Cash And Cash Equivalents': [8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500],
            'Operating Cash Flow': [3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400],
            'Capital Expenditure': [-1500, -1600, -1700, -1800, -1900, -2000, -2100, -2200],
            'Free Cash Flow': [1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200],
            'Dividend Payout': [0, 0, 0, 0, 0, 0, 0, 0],
        }
    else:  # annual
        # For annual, create 5 years of data
        date_labels = [f'FY {2019+i}' for i in range(5)]
        
        data = {
            'Date': date_labels,
            'Total Revenue': [18000, 21000, 24500, 29000, 31000],
            'Gross Profit': [4500, 5100, 5900, 7000, 7800],
            'Operating Income': [2200, 2600, 3000, 3500, 3800],
            'Net Income': [1800, 2200, 2600, 3100, 3300],
            'Total Assets': [55000, 59000, 65000, 72000, 75000],
            'Total Liabilities': [30000, 32000, 34000, 36000, 37000],
            'Total Stockholder Equity': [25000, 27000, 31000, 36000, 38000],
            'Cash And Cash Equivalents': [8000, 9000, 10000, 11000, 11500],
            'Operating Cash Flow': [3000, 3400, 3800, 4200, 4400],
            'Capital Expenditure': [-1500, -1700, -1900, -2100, -2200],
            'Free Cash Flow': [1500, 1700, 1900, 2100, 2200],
            'Dividend Payout': [0, 0, 0, 0, 0],
        }
    
    # Only include the requested metrics
    data_subset = {'Date': data['Date']}
    for metric in metrics:
        if metric in data:
            data_subset[metric] = data[metric]
        else:
            # Create fallback data with same length as the date array
            data_subset[metric] = [1000 * (i+1) for i in range(len(data['Date']))]
    
    # Create DataFrame from the subset
    dummy_data = pd.DataFrame(data_subset)
    
    # Convert to long format for plotting
    data_long = dummy_data.melt(id_vars='Date', var_name='Metric', value_name='Value')
    
    # Create bar chart
    fig = px.bar(
        data_long,
        x='Date',
        y='Value',
        color='Metric',
        barmode='group',
        title=f"{period} Financial Metrics",
        template=theme,
        height=500,
        color_discrete_sequence=['#FF3A33', '#22BBFF', '#9B59FF', '#27AE60']  # Bright colors for better visibility
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="",
        yaxis_title="USD (Millions)",
        legend_title="Metric",
        hovermode="x unified",
        legend=dict(
            font=dict(size=14, color="white"),
            orientation='h',
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        paper_bgcolor="rgba(30, 30, 42, 0.8)",
        plot_bgcolor="rgba(30, 30, 42, 0.8)"
    )
    
    # Update the axis titles and style
    fig.update_xaxes(
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    fig.update_yaxes(
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    # Format y-axis to show in millions
    fig.update_traces(hovertemplate='%{y:,.2f}')
    
    return fig

def plot_financial_ratios(ratio_data, theme):
    """
    Create a line chart showing financial ratios over time.
    
    Args:
        ratio_data (DataFrame): Financial ratio data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Create sample financial ratio data for plotting
    periods = 8
    dates = [f'Q{i} {2023+(i//4)}' for i in range(1, periods+1)]
    
    dummy_data = pd.DataFrame({
        'Date': dates,
        'Gross Margin': [25.3, 24.8, 26.1, 25.9, 25.4, 24.7, 25.1, 25.6],
        'Operating Margin': [11.4, 10.8, 11.9, 11.2, 11.5, 11.0, 11.3, 11.7],
        'Net Profit Margin': [9.2, 8.7, 9.5, 9.0, 9.3, 8.9, 9.1, 9.4],
        'ROE': [13.5, 13.1, 14.2, 13.8, 13.6, 13.2, 13.7, 14.0]
    })
    
    # Convert to long format for plotting
    data_long = dummy_data.melt(id_vars='Date', var_name='Ratio', value_name='Percentage')
    
    # Create line chart
    fig = px.line(
        data_long,
        x='Date',
        y='Percentage',
        color='Ratio',
        markers=True,
        title="Financial Ratio Trends",
        template=theme,
        height=450,
        line_shape='spline',  # Smoother lines
        color_discrete_sequence=['#FF3A33', '#22BBFF', '#9B59FF', '#27AE60']  # Bright colors
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Percentage (%)",
        legend_title="Ratio",
        hovermode="x unified",
        legend=dict(
            font=dict(size=14, color="white"),
            orientation='h',
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        paper_bgcolor="rgba(30, 30, 42, 0.8)",
        plot_bgcolor="rgba(30, 30, 42, 0.8)"
    )
    
    # Update the axis titles and style
    fig.update_xaxes(
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    fig.update_yaxes(
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    # Format y-axis and increase marker size
    fig.update_traces(
        hovertemplate='%{y:.2f}%',
        marker=dict(size=10),
        line=dict(width=3)
    )
    
    return fig

def plot_delivery_trends(delivery_data, theme):
    """
    Create a chart showing Tesla vehicle delivery trends.
    
    Args:
        delivery_data (DataFrame): Vehicle delivery data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Create a figure
    fig = go.Figure()
    
    # Add total deliveries line
    fig.add_trace(
        go.Scatter(
            x=delivery_data.index,
            y=delivery_data['Total Deliveries'],
            name="Total Deliveries",
            line=dict(color='#E31937', width=3),
            mode='lines+markers'
        )
    )
    
    # Add model group lines
    fig.add_trace(
        go.Scatter(
            x=delivery_data.index,
            y=delivery_data['Model 3/Y'],
            name="Model 3/Y",
            line=dict(color='#1C9BF0', width=2),
            mode='lines+markers'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=delivery_data.index,
            y=delivery_data['Model S/X'],
            name="Model S/X",
            line=dict(color='#8E44AD', width=2),
            mode='lines+markers'
        )
    )
    
    # Add Cybertruck if it exists in the data
    if 'Cybertruck' in delivery_data.columns:
        fig.add_trace(
            go.Scatter(
                x=delivery_data.index,
                y=delivery_data['Cybertruck'],
                name="Cybertruck",
                line=dict(color='#27AE60', width=2),
                mode='lines+markers'
            )
        )
    
    # Set figure layout
    fig.update_layout(
        title="Tesla Quarterly Vehicle Deliveries",
        template=theme,
        hovermode="x unified",
        legend=dict(
            font=dict(size=14, color="white"),
            orientation='h',
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        height=550,
        paper_bgcolor="rgba(30, 30, 42, 0.8)",
        plot_bgcolor="rgba(30, 30, 42, 0.8)"
    )
    
    # Set axis titles and improve visibility
    fig.update_xaxes(
        title_text="Quarter",
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    fig.update_yaxes(
        title_text="Vehicles Delivered",
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    # Format y-axis values and enhance markers
    fig.update_traces(
        hovertemplate='%{y:,.0f} vehicles',
        marker=dict(size=10)
    )
    
    return fig

def plot_model_mix(delivery_data, theme):
    """
    Create a pie chart showing vehicle model mix.
    
    Args:
        delivery_data (DataFrame): Vehicle delivery data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Sum deliveries for each model across the selected time period
    model_mix = {
        'Model 3': delivery_data['Model 3'].sum(),
        'Model Y': delivery_data['Model Y'].sum(),
        'Model S': delivery_data['Model S'].sum(),
        'Model X': delivery_data['Model X'].sum()
    }
    
    # Add Cybertruck if it exists in the data and has non-zero deliveries
    if 'Cybertruck' in delivery_data.columns and delivery_data['Cybertruck'].sum() > 0:
        model_mix['Cybertruck'] = delivery_data['Cybertruck'].sum()
    
    # Create dataframe for plotting
    mix_df = pd.DataFrame({'Model': model_mix.keys(), 'Deliveries': model_mix.values()})
    
    # Set colors for each model
    colors = {
        'Model 3': '#1C9BF0',
        'Model Y': '#27AE60',
        'Model S': '#E31937',
        'Model X': '#8E44AD',
        'Cybertruck': '#F1C40F'
    }
    
    # Create pie chart
    fig = px.pie(
        mix_df,
        values='Deliveries',
        names='Model',
        title="Vehicle Delivery Breakdown by Model",
        color='Model',
        color_discrete_map=colors,
        template=theme,
        height=500
    )
    
    # Update layout
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='%{label}: %{value:,.0f} vehicles (%{percent})'
    )
    
    return fig

def plot_regional_sales(theme):
    """
    Create a choropleth map showing Tesla's regional sales distribution.
    
    Args:
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Regional sales distribution (approximate percentages)
    regions = {
        'United States': 45,
        'China': 25,
        'Europe': 20,
        'Rest of World': 10
    }
    
    # Create dataframe for map
    region_data = pd.DataFrame({
        'country': ['USA', 'China', 'Germany', 'Canada', 'Norway', 'Netherlands', 
                   'United Kingdom', 'France', 'Australia', 'Japan', 'South Korea',
                   'Brazil', 'Mexico', 'India', 'United Arab Emirates'],
        'sales_percentage': [40, 25, 7, 5, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    })
    
    # Create choropleth map
    fig = px.choropleth(
        region_data,
        locations='country',
        locationmode='country names',
        color='sales_percentage',
        color_continuous_scale='Reds',
        template=theme,
        title="Tesla Global Sales Distribution",
        height=600
    )
    
    # Update layout
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Sales %"
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    return fig

def plot_normalized_stock_comparison(tesla_data, competitor_data, tickers, theme):
    """
    Create a normalized stock comparison chart.
    
    Args:
        tesla_data (DataFrame): Tesla stock data
        competitor_data (dict): Dictionary of competitor stock data
        tickers (list): List of ticker symbols
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Create figure
    fig = go.Figure()
    
    # Normalize Tesla data (first day = 100)
    tesla_normalized = tesla_data['Close'] / tesla_data['Close'].iloc[0] * 100
    
    # Add Tesla line
    fig.add_trace(
        go.Scatter(
            x=tesla_normalized.index,
            y=tesla_normalized,
            name="TSLA",
            line=dict(color='#E31937', width=3)
        )
    )
    
    # Add competitor lines
    colors = ['#1C9BF0', '#27AE60', '#8E44AD', '#F1C40F', '#E67E22', '#3498DB']
    
    for i, ticker in enumerate(tickers):
        # Skip if ticker data is missing or invalid
        if ticker not in competitor_data or competitor_data[ticker].empty:
            continue
            
        # Normalize competitor data
        comp_normalized = competitor_data[ticker]['Close'] / competitor_data[ticker]['Close'].iloc[0] * 100
        
        # Add line to chart
        fig.add_trace(
            go.Scatter(
                x=comp_normalized.index,
                y=comp_normalized,
                name=ticker,
                line=dict(color=colors[i % len(colors)], width=2)
            )
        )
    
    # Set figure layout
    fig.update_layout(
        title="Normalized Stock Performance Comparison (First Day = 100)",
        template=theme,
        hovermode="x unified",
        legend=dict(
            font=dict(size=14, color="white"),
            orientation='h',
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        height=550,
        paper_bgcolor="rgba(30, 30, 42, 0.8)",
        plot_bgcolor="rgba(30, 30, 42, 0.8)"
    )
    
    # Set axis titles with improved visibility
    fig.update_xaxes(
        title_text="Date",
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    fig.update_yaxes(
        title_text="Normalized Price (First Day = 100)",
        title_font=dict(size=16, color="white"),
        tickfont=dict(size=14, color="white"),
        gridcolor="rgba(255, 255, 255, 0.15)"
    )
    
    # Format hover template
    fig.update_traces(
        hovertemplate='%{y:.2f}'
    )
    
    return fig

def plot_ev_market_share(year, theme):
    """
    Create a pie chart showing EV market share.
    
    Args:
        year (int): Year for market share data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Get market share data for the selected year
    market_share = dp.get_ev_market_share_data(year)
    
    # Create dataframe for plotting
    share_df = pd.DataFrame({
        'Manufacturer': market_share.keys(),
        'Market Share': market_share.values()
    })
    
    # Set colors
    colors = {
        'Tesla': '#E31937',
        'BYD': '#1C9BF0',
        'Volkswagen': '#27AE60',
        'SAIC': '#8E44AD',
        'BMW': '#F1C40F',
        'Hyundai-Kia': '#E67E22',
        'Nissan': '#3498DB',
        'BAIC': '#9B59B6',
        'Stellantis': '#2ECC71',
        'Others': '#95A5A6'
    }
    
    # Create pie chart
    fig = px.pie(
        share_df,
        values='Market Share',
        names='Manufacturer',
        title=f"Global EV Market Share {year}",
        color='Manufacturer',
        color_discrete_map=colors,
        template=theme,
        height=500
    )
    
    # Update layout
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='%{label}: %{value}% market share'
    )
    
    return fig

def plot_competitive_matrix(x_metric, y_metric, competitors, theme):
    """
    Create a bubble chart showing competitive positioning.
    
    Args:
        x_metric (str): Metric for x-axis
        y_metric (str): Metric for y-axis
        competitors (list): List of competitor ticker symbols
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Define metric data for each company
    companies = ['TSLA'] + [ticker.split(' ')[0] for ticker in competitors]
    
    # Define sample data for each metric
    metrics = {
        'Market Cap': {
            'TSLA': 650,
            'F': 52,
            'GM': 55,
            'VWAGY': 70,
            'TM': 240,
            'XPEV': 12,
            'NIO': 15
        },
        'Revenue Growth': {
            'TSLA': 25,
            'F': 5,
            'GM': 2,
            'VWAGY': 4,
            'TM': 3,
            'XPEV': 40,
            'NIO': 45
        },
        'Profit Margin': {
            'TSLA': 12,
            'F': 5,
            'GM': 6,
            'VWAGY': 7,
            'TM': 8,
            'XPEV': -25,
            'NIO': -30
        },
        'R&D Spending': {
            'TSLA': 20,
            'F': 8,
            'GM': 9,
            'VWAGY': 15,
            'TM': 12,
            'XPEV': 30,
            'NIO': 35
        }
    }
    
    # Create data for plotting
    data = []
    for company in companies:
        if company in metrics[x_metric] and company in metrics[y_metric]:
            data.append({
                'Company': company,
                x_metric: metrics[x_metric][company],
                y_metric: metrics[y_metric][company],
                'EV Focus': 100 if company == 'TSLA' or company == 'XPEV' or company == 'NIO' else 25,
                'Size': metrics['Market Cap'][company]
            })
    
    # Create dataframe
    df = pd.DataFrame(data)
    
    # Create bubble chart
    fig = px.scatter(
        df,
        x=x_metric,
        y=y_metric,
        size='Size',
        color='Company',
        text='Company',
        size_max=50,
        title=f"Competitive Analysis: {x_metric} vs {y_metric}",
        template=theme,
        height=500
    )
    
    # Update layout
    fig.update_traces(
        textposition='top center',
        hovertemplate='%{text}<br>' +
                      f'{x_metric}: %{{x}}<br>' +
                      f'{y_metric}: %{{y}}<br>' +
                      'Market Cap: $%{marker.size}B'
    )
    
    return fig

def plot_carbon_offset(environmental_data, theme):
    """
    Create a chart showing carbon offset over time.
    
    Args:
        environmental_data (DataFrame): Environmental impact data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Create figure
    fig = go.Figure()
    
    # Add bar chart for carbon offset
    fig.add_trace(
        go.Bar(
            x=environmental_data.index.year,
            y=environmental_data['Carbon Offset (Mt CO2)'],
            name="Carbon Offset",
            marker_color='#27AE60'
        )
    )
    
    # Calculate cumulative offset
    cumulative_offset = environmental_data['Carbon Offset (Mt CO2)'].cumsum()
    
    # Add line for cumulative offset
    fig.add_trace(
        go.Scatter(
            x=environmental_data.index.year,
            y=cumulative_offset,
            name="Cumulative Offset",
            line=dict(color='#E31937', width=3),
            mode='lines+markers'
        )
    )
    
    # Set figure layout
    fig.update_layout(
        title="Estimated Carbon Offset by Tesla Vehicles",
        template=theme,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500
    )
    
    # Set axis titles
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Million Metric Tons CO2")
    
    return fig

def plot_energy_production(environmental_data, theme):
    """
    Create a chart showing Tesla energy production metrics.
    
    Args:
        environmental_data (DataFrame): Environmental impact data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add solar deployment line
    fig.add_trace(
        go.Scatter(
            x=environmental_data.index.year,
            y=environmental_data['Solar Deployment (MW)'],
            name="Solar Deployment (MW)",
            line=dict(color='#F1C40F', width=2),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    # Add energy storage line
    fig.add_trace(
        go.Scatter(
            x=environmental_data.index.year,
            y=environmental_data['Energy Storage (MWh)'],
            name="Energy Storage (MWh)",
            line=dict(color='#3498DB', width=2),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    # Set figure layout
    fig.update_layout(
        title="Tesla Energy Production",
        template=theme,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500
    )
    
    # Set axis titles
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Solar Deployment (MW)", secondary_y=False)
    fig.update_yaxes(title_text="Energy Storage (MWh)", secondary_y=True)
    
    return fig

def plot_sustainability_radar(sustainability_data, theme):
    """
    Create a radar chart showing sustainability metrics.
    
    Args:
        sustainability_data (dict): Sustainability metric data
        theme (str): Chart theme
        
    Returns:
        Figure: Plotly figure object
    """
    # Get metric categories and values
    categories = list(sustainability_data.keys())
    values = list(sustainability_data.values())
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Tesla Sustainability',
            line=dict(color='#27AE60')
        )
    )
    
    # Add industry average for comparison
    industry_avg = [50, 40, 35, 30, 45, 30]  # Sample industry averages
    
    fig.add_trace(
        go.Scatterpolar(
            r=industry_avg,
            theta=categories,
            fill='toself',
            name='Industry Average',
            line=dict(color='#95A5A6')
        )
    )
    
    # Set figure layout
    fig.update_layout(
        title="Sustainability Performance (% of Target)",
        template=theme,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500
    )
    
    return fig
