import streamlit as st
import plotly.graph_objects as go

def render_metric_card(title, value, change, change_pct):
    """
    Renders a metric card with proper coloring for up/down.
    """
    delta_color = "normal"
    if change > 0:
        delta_color = "normal" # Streamlit handles green for positive
    elif change < 0:
        delta_color = "inverse" # Streamlit handles red for negative
        
    st.metric(
        label=title,
        value=f"₹{value:,.2f}" if "USD/INR" not in title else f"{value:,.2f}",
        delta=f"{change:,.2f} ({change_pct:.2f}%)",
        delta_color=delta_color
    )

def plot_price_chart(df, ticker_name, y_col='Close', currency_symbol=''):
    """
    Plots an interactive line chart using Plotly.
    """
    if df.empty:
        st.warning(f"No historical data available for {ticker_name}")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[y_col],
        mode='lines',
        name=ticker_name,
        line=dict(width=2)
    ))
    
    fig.update_layout(
        title=f"{ticker_name} Price Trend ({currency_symbol})",
        xaxis_title="Date",
        yaxis_title=f"Price ({currency_symbol})",
        template="plotly_dark",
        margin=dict(l=0, r=0, t=30, b=0),
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_sentiment_gauge(score, verdict):
    """
    visualize sentiment score using a gauge chart.
    Score is -1 to 1.
    """
    # Map -1..1 to 0..100 for gauge convenience? Or just keep raw.
    # Let's use a gauge chart.
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Geopolitical Sentiment ({verdict})"},
        delta = {'reference': 0}, # Benchmark is 0 (Neutral)
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [-1, -0.05], 'color': "red"},
                {'range': [-0.05, 0.05], 'color': "gray"},
                {'range': [0.05, 1], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "yellow", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)
