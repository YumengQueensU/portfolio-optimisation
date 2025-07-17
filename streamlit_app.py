import streamlit as st
import pandas as pd
import plotly.express as px

# 加载性能数据
df = pd.read_csv("results/metrics_summary.csv")

st.title("📊 Portfolio Strategy Comparison Dashboard")

# 策略选择器
strategy = st.selectbox("Select a Strategy", df['Strategy'])

# 权重饼图（从单独的文件中读取）
weights_file = f"results/weights_{strategy.lower().replace(' ', '_')}.csv"
try:
    weights_df = pd.read_csv(weights_file)
    st.subheader(f"📈 Allocation Weights — {strategy}")
    fig_pie = px.pie(weights_df, names='Asset', values='Weight', title='Weight Distribution')
    st.plotly_chart(fig_pie)
except FileNotFoundError:
    st.warning("⚠️ Weight file not found. Please make sure it exists.")

# 风险-收益图
st.subheader("🎯 Risk vs Return")
fig_risk_return = px.scatter(
    df,
    x='Volatility',
    y='Return',
    color='Strategy',
    size='Return',
    hover_data=['Strategy'],
    title="Risk-Return Scatter Plot"
)
st.plotly_chart(fig_risk_return)

# 对比表格
st.subheader("📋 Strategy Metrics Table")
st.dataframe(df.set_index("Strategy").style.format({
    "Return (%)": "{:.2f}",
    "Volatility (%)": "{:.2f}"
}))
