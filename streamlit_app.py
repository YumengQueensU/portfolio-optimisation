import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Portfolio Strategy Comparison", layout="wide")

st.title("📈 Portfolio Strategy Explorer")
st.markdown("""
Explore different portfolio optimisation strategies based on historical ETF performance.
""")

# ===========================
# 1. Simulated input data
# ===========================
strategies = ['Markowitz', 'Risk Parity', 'Lasso', 'Random Forest', 'XGBoost', 'MLP', 'LSTM', 'GRU']
tickers = ['EEM', 'GLD', 'IWM', 'SPY', 'TLT']

# Example: Simulated weight dictionaries for each strategy
weights_dict = {
    'Markowitz': [0.15, 0.25, 0.20, 0.30, 0.10],
    'Risk Parity': [0.20, 0.20, 0.20, 0.20, 0.20],
    'Lasso': [0.01, 0.33, 0.00, 0.29, 0.37],
    'Random Forest': [0.05, 0.30, 0.15, 0.25, 0.25],
    'XGBoost': [0.10, 0.28, 0.12, 0.30, 0.20],
    'MLP': [0.05, 0.35, 0.10, 0.30, 0.20],
    'LSTM': [0.07, 0.32, 0.10, 0.31, 0.20],
    'GRU': [0.09, 0.30, 0.12, 0.29, 0.20],
}

# Example: Simulated return & volatility data
performance = pd.DataFrame({
    'Strategy': strategies,
    'Return': [0.0586, 0.0521, 0.0003, 0.0412, 0.0465, 0.0321, 0.0333, 0.0308],
    'Volatility': [0.101, 0.093, 0.101, 0.095, 0.096, 0.090, 0.091, 0.092]
})
performance['Sharpe'] = performance['Return'] / performance['Volatility']

# ===========================
# 2. Sidebar selector
# ===========================
st.sidebar.header("Select Strategy")
selected_strategy = st.sidebar.selectbox("Choose a strategy to view weights", strategies)

# ===========================
# 3. Weight pie chart
# ===========================
st.subheader(f"🎯 Portfolio Weights — {selected_strategy}")
weights = weights_dict[selected_strategy]
weight_df = pd.DataFrame({'ETF': tickers, 'Weight': weights})
pie = px.pie(weight_df, names='ETF', values='Weight', hole=0.4)
st.plotly_chart(pie, use_container_width=True)

# ===========================
# 4. Strategy comparison chart (Return vs Volatility)
# ===========================
st.subheader("📉 Strategy Risk vs Return")
fig = px.scatter(
    performance,
    x='Volatility',
    y='Return',
    text='Strategy',
    size=[12]*len(performance),
    color='Sharpe',
    color_continuous_scale='Blues',
    labels={'Volatility': 'Annualised Volatility', 'Return': 'Annualised Return'}
)
fig.update_traces(textposition='top center')
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# ===========================
# 5. Strategy summary table
# ===========================
st.subheader("📊 Strategy Summary Table")
st.dataframe(performance.set_index('Strategy').style.format("{:.2%}"))