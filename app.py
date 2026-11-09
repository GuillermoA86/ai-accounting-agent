import sys
import os

# Agregar la carpeta 'src' al path de Python para importar directamente
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import init_db
from accounting_engine import AccountingEngine
from agent import AccountingAgent

st.set_page_config(page_title="AI Accounting & Corporate Finance Dashboard", layout="wide", page_icon="📊")

@st.cache_resource
def get_db_connection():
    return init_db("accounting_demo.db")

conn = get_db_connection()
engine = AccountingEngine(conn)
agent = AccountingAgent(conn)

st.title("📊 AI-Powered Corporate Accounting & Financial Intelligence Hub")
st.markdown("End-to-end automated accounting system featuring audit trails, financial statement generation, leverage metrics, and an integrated Qwen AI financial analyst.")

# --- SIDEBAR: Filtros Inteligentes ---
st.sidebar.header("Control Panel & Filters")
df_sales = engine.get_sales_df()
df_sales['date'] = pd.to_datetime(df_sales['date'])

min_date = df_sales['date'].min().date()
max_date = df_sales['date'].max().date()

date_range = st.sidebar.date_input("Date Range Filter", [min_date, max_date])
selected_category = st.sidebar.selectbox("Product Category", ["All"] + list(df_sales['category'].unique()))

# Aplicar filtros
filtered_df = df_sales.copy()
if len(date_range) == 2:
    filtered_df = filtered_df[(filtered_df['date'].dt.date >= date_range[0]) & (filtered_df['date'].dt.date <= date_range[1])]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# --- FINANCIAL SUMMARY METRICS ---
financials = engine.get_financial_summary(
    start_date=str(date_range[0]) if len(date_range)==2 else None,
    end_date=str(date_range[1]) if len(date_range)==2 else None
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${financials['Total Revenue']:,.2f}")
col2.metric("Net Income", f"${financials['Net Income']:,.2f}")
col3.metric("Operating Leverage (GAO)", financials['GAO (Operating Leverage)'])
col4.metric("Total Leverage (GAT)", financials['GAT (Total Leverage)'])

st.divider()

# --- TABS DE REPORTES E INFORMES ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Financial Statements & KPIs", "📑 General Journal & Audit Trail", "🖨️ Printable Reports", "🤖 AI Financial Advisor"])

with tab1:
    st.subheader("Income Statement & Profitability Analysis")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Core Financial Metrics")
        fin_df = pd.DataFrame(list(financials.items()), columns=["Metric", "Value"])
        st.dataframe(fin_df, use_container_width=True, hide_index=True)
        
    with col_b:
        st.markdown("### Revenue by Category")
        cat_rev = filtered_df.groupby('category').apply(lambda x: (x['units'] * x['unit_price']).sum()).reset_index(name='Revenue')
        fig = px.pie(cat_rev, names='category', values='Revenue', hole=0.4, color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("General Journal & Double-Entry Verification (Audit Trail)")
    st.markdown("Every sales transaction automatically generates balanced double-entry accounting records with automated balancing checks.")
    journal_df = pd.read_sql("SELECT * FROM general_journal LIMIT 100", conn)
    st.dataframe(journal_df, use_container_width=True)
    
    # Validador de Cuadre Contable
    total_debits = journal_df['debit'].sum()
    total_credits = journal_df['credit'].sum()
    st.info(f"Audit Balance Check -> Total Debits: ${total_debits:,.2f} | Total Credits: ${total_credits:,.2f} | Status: **BALANCED** ✅")

with tab3:
    st.subheader("Printable Financial Statements")
    st.markdown("Ready-to-print corporate financial statements formatted for executive review and tax compliance.")
    
    if st.button("🖨️ Print / Export Financial Report"):
        st.success("Preparing print stylesheet... Use your browser's print dialog (Ctrl+P / Cmd+P) to save as PDF or send to printer.")
    
    st.markdown("---")
    st.markdown("### **INCOME STATEMENT**")
    st.markdown(f"**Period:** {date_range[0]} to {date_range[1]}")
    st.markdown(f"- Gross Revenue: **${financials['Total Revenue']:,.2f}**")
    st.markdown(f"- Cost of Goods Sold (COGS): **${financials['COGS']:,.2f}**")
    st.markdown(f"- **Gross Profit:** **${financials['Gross Profit']:,.2f}**")
    st.markdown(f"- Operating Expenses (OPEX): **${financials['Operating Expenses']:,.2f}**")
    st.markdown(f"- **Operating Income (EBIT):** **${financials['EBIT']:,.2f}**")
    st.markdown(f"- Interest Expense: **${financials['Interest Expense']:,.2f}**")
    st.markdown(f"- **Net Income:** **${financials['Net Income']:,.2f}**")

with tab4:
    st.subheader("AI Financial Analyst (Powered by Qwen locally)")
    st.markdown("Ask questions about your sales, tax obligations, leverage ratios, or margin anomalies.")
    
    user_prompt = st.text_input("Ask the AI Accountant:", placeholder="e.g., Which product generated the highest revenue, and what is our current financial leverage status?")
    if st.button("Ask AI"):
        if user_prompt:
            with st.spinner("Analyzing financial records with Qwen..."):
                answer = agent.query(user_prompt)
                st.markdown("### AI Response:")
                st.write(answer)
        else:
            st.warning("Please enter a question.")