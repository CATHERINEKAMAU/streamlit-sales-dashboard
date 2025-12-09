# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# --- CONFIGURATION CONSTANTS ---
DATA_FILE = "sales_dashboard.csv" 
DATE_COL = "order_date"
SALES_COL = "total_sales"
REGION_COL = "region"
CATEGORY_COL = "category" # Used for the new chart
ORDER_ID_COL = "order_id"

# --- HELPER FUNCTIONS ---

@st.cache_data
def load_data(file_path):
    """
    Loads, cleans, and transforms the sales data (Cached for performance).
    """
    try:
        # 1. Load data using the relative path
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: File not found at {file_path}. Please ensure the file is in the same directory.")
        return None 
        
    # --- DATA CLEANING AND TYPE CONVERSION ---
    
    # 1. Date Correction Fix: Strip whitespace and specify format
    df[DATE_COL] = df[DATE_COL].astype(str).str.strip() 
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], format='%Y-%m-%d', errors='coerce') 
    
    # 2. FINAL SALES CLEANING FIX
    df[SALES_COL] = df[SALES_COL].astype(str).str.replace(r'[^\d.]', '', regex=True)

    # 3. Convert to numeric
    df[SALES_COL] = pd.to_numeric(df[SALES_COL], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    # Drop any rows with NaN values in critical columns
    df.dropna(subset=[DATE_COL, SALES_COL, CATEGORY_COL, REGION_COL], inplace=True)
    
    return df

def to_excel(df):
    """Converts a Pandas DataFrame to an Excel file stored in memory."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Filtered_Sales_Data', index=False)
    output.seek(0)
    return output.read()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Regional Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Regional Sales Dashboard")
st.markdown("Metrics and trends based on aggregated sales data.")

# --- DATA LOADING ---
df = load_data(DATA_FILE)

# Stop the script if data loading failed (df is None)
if df is None:
    st.stop()


# =================================================================
# === SIDEBAR FILTERS ===
# =================================================================
st.sidebar.header("Filter Options")

# Date Range Filter
min_date = df[DATE_COL].min().date()
max_date = df[DATE_COL].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Filter
selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=df[REGION_COL].unique(),
    default=df[REGION_COL].unique()
)

# Category Filter
selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=df[CATEGORY_COL].unique(),
    default=df[CATEGORY_COL].unique()
)

# --- APPLY FILTERS ---
if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    
    # Filter the data based on all selections
    df_filtered = df[
        (df[DATE_COL] >= start_date) & 
        (df[DATE_COL] <= end_date) &
        (df[REGION_COL].isin(selected_regions)) &
        (df[CATEGORY_COL].isin(selected_categories))
    ].copy()
else:
    st.warning("Please select a complete date range.")
    st.stop() 

if df_filtered.empty:
    st.error("No data available based on current filters. Try widening your selection.")
    st.stop()


# =================================================================
# === 1. KEY PERFORMANCE INDICATORS (KPIs) ===
# =================================================================
st.header("1. Key Performance Indicators (KPIs)")

# Calculate KPIs on the filtered data
total_sales = df_filtered[SALES_COL].sum()
avg_sales = df_filtered[SALES_COL].mean()
total_orders = df_filtered[ORDER_ID_COL].nunique()
top_product = df_filtered.groupby('product')[SALES_COL].sum().idxmax() 

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"Ksh {total_sales:,.2f}")

with col2:
    st.metric("Avg. Sale Amount", f"Ksh {avg_sales:,.2f}")

with col3:
    st.metric("Total Orders", f"{total_orders:,.0f}")
    
with col4:
    st.metric("Top Selling Product", top_product)


# =================================================================
# === 2. INTERACTIVE CHARTS (TIME & REGION) ===
# =================================================================
st.header("2. Revenue Trends and Regional Performance")

chart_col1, chart_col2 = st.columns(2)

# --- Chart A: Sales Trend Over Time (Line Chart) ---
with chart_col1:
    st.subheader("Monthly Revenue Trend")
    
    # Resample to Month ('M') for smoother trend line
    sales_over_time = df_filtered.set_index(DATE_COL).resample('M')[SALES_COL].sum().reset_index()

    fig_time = px.line(
        sales_over_time, 
        x=DATE_COL, 
        y=SALES_COL, 
        title='Monthly Revenue Trend',
        template='plotly_white'
    )
    st.plotly_chart(fig_time, use_container_width=True)


# --- Chart B: Sales by Region (Bar Chart) ---
with chart_col2:
    st.subheader("Total Sales by Region")

    # Group by region and sort to show top performers
    sales_by_region = df_filtered.groupby(REGION_COL)[SALES_COL].sum().reset_index()

    fig_region = px.bar(
        sales_by_region.sort_values(by=SALES_COL, ascending=False),
        x=REGION_COL,
        y=SALES_COL,
        title='Total Revenue by Region',
        labels={
            SALES_COL: 'Total Revenue', 
            REGION_COL: 'Region'
        }, 
        template='plotly_white',
        color=SALES_COL 
    )
    st.plotly_chart(fig_region, use_container_width=True)


# =================================================================
# === 3. SALES BY CATEGORY (NEW SECTION) ===
# =================================================================
st.header("3. Sales by Product Category")

# --- Chart C: Sales by Product Category (Bar Chart) ---
sales_by_category = df_filtered.groupby(CATEGORY_COL)[SALES_COL].sum().reset_index()

fig_category = px.bar(
    sales_by_category.sort_values(by=SALES_COL, ascending=False),
    x=CATEGORY_COL,
    y=SALES_COL,
    title='Total Revenue by Product Category',
    labels={
        SALES_COL: 'Total Revenue', 
        CATEGORY_COL: 'Product Category'
    },
    template='plotly_white',
    color=SALES_COL 
)
st.plotly_chart(fig_category, use_container_width=True)


# =================================================================
# === 4. DOWNLOAD & DATA PREVIEW ===
# =================================================================
st.markdown("---")
st.header("4. Filtered Data")

# Download Button
excel_data = to_excel(df_filtered) 
st.download_button(
    label="Download Filtered Data as Excel (.xlsx)",
    data=excel_data,
    file_name=f'Sales_Dashboard_Export_{pd.Timestamp.now().strftime("%Y%m%d")}.xlsx',
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Raw Data Preview
st.subheader("Filtered Data Preview")
st.dataframe(df_filtered, use_container_width=True)