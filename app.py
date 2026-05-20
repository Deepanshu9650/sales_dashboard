from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Data Dashboard")

df = pd.read_csv('sales_data.csv')
df['city'] = df['city'].fillna('Unknown')
df['quantity'] = df['quantity'].fillna(df['quantity'].mean())
df['revenue'] = df['quantity'] * df['price']

# ── Sidebar filters ──────────────────────────────────────────
st.sidebar.header("Filters")

cities = ['All'] + sorted(df['city'].unique().tolist())
selected_city = st.sidebar.selectbox("City", cities)

months = ['All'] + sorted(df['month'].unique().tolist())
selected_month = st.sidebar.selectbox("Month", months)

products = ['All'] + sorted(df['product'].unique().tolist())
selected_product = st.sidebar.selectbox("Product", products)

# ── Apply filters ─────────────────────────────────────────────
filtered = df.copy()
if selected_city    != 'All': filtered = filtered[filtered['city']    == selected_city]
if selected_month   != 'All': filtered = filtered[filtered['month']   == selected_month]
if selected_product != 'All': filtered = filtered[filtered['product'] == selected_product]

# ── KPI cards ─────────────────────────────────────────────────
st.subheader("Key metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total orders",   len(filtered))
col2.metric("Total revenue",  f"₹{filtered['revenue'].sum():,.0f}")
col3.metric("Avg order value",f"₹{filtered['revenue'].mean():,.0f}")
col4.metric("Units sold",     f"{filtered['quantity'].sum():,.0f}")

st.divider()

# ── Charts ────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by product")
    product_rev = filtered.groupby('product')['revenue'].sum().sort_values(ascending=False)
    st.bar_chart(product_rev)

with col_right:
    st.subheader("Revenue by month")
    month_order = ['Jan','Feb','Mar','Apr','May','Jun']
    month_rev = filtered.groupby('month')['revenue'].sum()
    month_rev = month_rev.reindex([m for m in month_order if m in month_rev.index])
    st.bar_chart(month_rev)

st.subheader("Orders by city")
city_orders = filtered.groupby('city')['order_id'].count().sort_values(ascending=False)
st.bar_chart(city_orders)

st.divider()

# ── Raw data ──────────────────────────────────────────────────
st.subheader(f"Filtered data — {len(filtered)} orders")
st.dataframe(filtered[['order_id','product','category',
                        'quantity','price','revenue','city','month']],
             use_container_width=True)

st.download_button(
    label="Download filtered data as CSV",
    data=filtered.to_csv(index=False),
    file_name='filtered_sales.csv',
    mime='text/csv'
)

st.divider()
st.subheader("Ask AI about your sales data")

# ── Setup Groq AI ─────────────────────────────────────────────
GGROQ_API_KEY = st.secrets["GROQ_API_KEY"]  # paste your gsk_... key here

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

# ── Build data summary for AI context ─────────────────────────
data_summary = f"""
You are a sales data analyst. Answer questions based on this data summary:

Total orders: {len(df)}
Total revenue: ₹{df['revenue'].sum():,.0f}

Revenue by product:
{df.groupby('product')['revenue'].sum().sort_values(ascending=False).to_string()}

Revenue by city:
{df.groupby('city')['revenue'].sum().sort_values(ascending=False).to_string()}

Revenue by month:
{df.groupby('month')['revenue'].sum().sort_values(ascending=False).to_string()}

Revenue by category:
{df.groupby('category')['revenue'].sum().sort_values(ascending=False).to_string()}

Top 5 highest orders:
{df.nlargest(5, 'revenue')[['product','city','month','revenue']].to_string()}

Answer clearly and concisely. Use ₹ for currency.
"""

# ── Chat history ──────────────────────────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ── Display chat history ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

# ── Chat input ────────────────────────────────────────────────
question = st.chat_input("Ask anything about your sales data...")

if question:
    st.session_state.messages.append({'role': 'user', 'content': question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke([
                SystemMessage(content=data_summary),
                HumanMessage(content=question)
            ])
            answer = response.content
            st.write(answer)

    st.session_state.messages.append({'role': 'assistant', 'content': answer})