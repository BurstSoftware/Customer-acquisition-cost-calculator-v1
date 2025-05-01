import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Streamlit app configuration
st.set_page_config(page_title="CAC Calculator", layout="wide")

# Title and description
st.title("Customer Acquisition Cost (CAC) Calculator")
st.markdown("""
Calculate and analyze the cost of acquiring customers to optimize your marketing spend.  
Input marketing expenses and customer data, compare CAC with CLV, and explore trends over time.
""")

# --- Sidebar for Inputs ---
st.sidebar.header("Input Marketing & Customer Data")
with st.sidebar.form(key="input_form"):
    # Marketing expenses by channel
    st.subheader("Marketing Expenses ($)")
    ads_cost = st.number_input("Ads (e.g., Google, Facebook)", min_value=0.0, value=1000.0, step=100.0)
    referrals_cost = st.number_input("Referrals", min_value=0.0, value=500.0, step=100.0)
    email_cost = st.number_input("Email Marketing", min_value=0.0, value=300.0, step=50.0)
    
    # Customers acquired by channel
    st.subheader("Customers Acquired")
    ads_customers = st.number_input("Customers from Ads", min_value=0, value=50, step=1)
    referrals_customers = st.number_input("Customers from Referrals", min_value=0, value=20, step=1)
    email_customers = st.number_input("Customers from Email", min_value=0, value=10, step=1)
    
    # CLV input
    clv = st.number_input("Customer Lifetime Value (CLV) ($)", min_value=0.0, value=2000.0, step=100.0)
    
    # Time period for trend analysis
    periods = st.slider("Select number of months for trend analysis", min_value=1, max_value=12, value=6)
    
    submit_button = st.form_submit_button(label="Calculate CAC")

# --- Main Content ---
if submit_button:
    # Create data for calculations
    channels = ["Ads", "Referrals", "Email Marketing"]
    costs = [ads_cost, referrals_cost, email_cost]
    customers = [ads_customers, referrals_customers, email_customers]
    
    # Calculate CAC per channel
    cac_values = [cost / cust if cust > 0 else 0 for cost, cust in zip(costs, customers)]
    total_cost = sum(costs)
    total_customers = sum(customers)
    overall_cac = total_cost / total_customers if total_customers > 0 else 0
    
    # Create DataFrame for results
    results_df = pd.DataFrame({
        "Channel": channels,
        "Cost ($)": costs,
        "Customers Acquired": customers,
        "CAC ($)": [round(cac, 2) for cac in cac_values]
    })
    
    # Display results
    st.subheader("CAC Results")
    st.dataframe(results_df, use_container_width=True)
    st.write(f"**Overall CAC**: ${round(overall_cac, 2)}")
    st.write(f"**Customer Lifetime Value (CLV)**: ${clv}")
    st.write(f"**CLV to CAC Ratio**: {round(clv / overall_cac, 2) if overall_cac > 0 else 'N/A'}")
    
    # --- CLV vs CAC Comparison ---
    st.subheader("CLV vs CAC Comparison")
    if overall_cac > 0:
        fig_comparison = go.Figure(data=[
            go.Bar(name="CAC", x=["Overall"], y=[overall_cac]),
            go.Bar(name="CLV", x=["Overall"], y=[clv])
        ])
        fig_comparison.update_layout(
            title="CLV vs CAC",
            yaxis_title="Amount ($)",
            barmode="group"
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # --- Trend Analysis ---
    st.subheader("CAC Trends Over Time")
    # Simulate historical CAC data (replace with real data in production)
    trend_data = pd.DataFrame({
        "Month": [f"Month {i+1}" for i in range(periods)],
        "Ads CAC": [cac_values[0] * (1 + 0.1 * (i % 3)) for i in range(periods)],
        "Referrals CAC": [cac_values[1] * (1 - 0.05 * (i % 4)) for i in range(periods)],
        "Email CAC": [cac_values[2] * (1 + 0.08 * (i % 2)) for i in range(periods)]
    })
    
    # Plot trends with Plotly
    fig_trends = px.line(
        trend_data.melt(id_vars="Month", value_vars=["Ads CAC", "Referrals CAC", "Email CAC"]),
        x="Month",
        y="value",
        color="variable",
        title="CAC Trends by Channel",
        labels={"value": "CAC ($)", "variable": "Channel"}
    )
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # --- Recommendations ---
    st.subheader("Recommendations for Cost Reduction")
    recommendations = []
    if overall_cac > clv / 3:
        recommendations.append("Your CAC is high relative to CLV. Consider optimizing high-cost channels.")
    for channel, cac in zip(channels, cac_values):
        if cac > overall_cac * 1.2:
            recommendations.append(f"**{channel}** has a high CAC (${round(cac, 2)}). Explore cost-efficient strategies or reallocate budget.")
        if cac < overall_cac * 0.8 and cac > 0:
            recommendations.append(f"**{channel}** has a low CAC (${round(cac, 2)}). Consider scaling this channel.")
    
    if recommendations:
        for rec in recommendations:
            st.markdown(f"- {rec}")
    else:
        st.write("Your CAC is well-optimized. Continue monitoring trends.")
    
    # --- Link to AI Advertising Writer ---
    st.subheader("Optimize Campaigns")
    st.markdown("""
    Use our [AI Advertising Writer](https://x.ai/ad-writer) to create cost-effective ad campaigns and improve customer acquisition.
    """)

# --- Footer ---
st.markdown("---")
st.write("Built with Streamlit | Enhances marketing efficiency similar to HubSpot analytics.")
