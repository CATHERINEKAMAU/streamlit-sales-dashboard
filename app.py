# app.py
"""
Main Sales Dashboard Application
Imports styling from styles.py module for clean separation of concerns
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# Import UI/UX styling module
from styles import (
    get_custom_css,
    get_header_html,
    get_section_header_html,
    get_info_box_html,
    get_footer_html,
    CHART_COLORS,
    get_plotly_theme
)

# --- CONFIGURATION CONSTANTS ---
DATA_FILE = "sales_dashboard.csv" 
DATE_COL = "order_date"
SALES_COL = "total_sales"
REGION_COL = "region"
CATEGORY_COL = "category"
ORDER_ID_COL = "order_id"

# --- DATA FUNCTIONS ---

@st.cache_data
def load_data(file_path):
    """
    Loads, cleans, and transforms the sales data (Cached for performance).
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"❌ Error: File not found at {file_path}. Please ensure the file is in the same directory.")
        return None 
        
    # Data cleaning
    df[DATE_COL] = df[DATE_COL].astype(str).str.strip() 
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], format='%Y-%m-%d', errors='coerce') 
    df[SALES_COL] = df[SALES_COL].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df[SALES_COL] = pd.to_numeric(df[SALES_COL], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df.dropna(subset=[DATE_COL, SALES_COL, CATEGORY_COL, REGION_COL], inplace=True)
    
    return df


def to_excel(df):
    """Converts a Pandas DataFrame to an Excel file stored in memory."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Filtered_Sales_Data', index=False)
    output.seek(0)
    return output.read()


# --- CHART CREATION FUNCTIONS ---

def create_time_series_chart(df_filtered):
    """Creates an enhanced time series chart."""
    sales_over_time = df_filtered.set_index(DATE_COL).resample('M')[SALES_COL].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sales_over_time[DATE_COL],
        y=sales_over_time[SALES_COL],
        mode='lines+markers',
        name='Revenue',
        line=dict(color=CHART_COLORS['primary'][0], width=3),
        marker=dict(size=8, color=CHART_COLORS['primary'][1]),
        fill='tozeroy',
        fillcolor=f'rgba(99, 102, 241, 0.1)'
    ))
    
    fig.update_layout(
        title='Monthly Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue (Ksh)',
        hovermode='x unified',
        **get_plotly_theme(),
        height=400,
        showlegend=False
    )
    
    return fig


def create_regional_chart(df_filtered):
    """Creates an enhanced regional analysis chart."""
    sales_by_region = df_filtered.groupby(REGION_COL)[SALES_COL].sum().reset_index()
    sales_by_region = sales_by_region.sort_values(by=SALES_COL, ascending=False)
    
    fig = px.bar(
        sales_by_region,
        x=REGION_COL,
        y=SALES_COL,
        title='Revenue by Region',
        labels={SALES_COL: 'Revenue (Ksh)', REGION_COL: 'Region'},
        color=SALES_COL,
        color_continuous_scale=[[0, '#164E63'], [0.5, '#0891B2'], [1, '#67E8F9']],
        text=SALES_COL
    )
    
    fig.update_traces(texttemplate='Ksh %{text:,.0f}', textposition='outside')
    fig.update_layout(**get_plotly_theme(), height=400, showlegend=False)
    
    return fig


def create_category_pie_chart(df_filtered):
    """Creates a pie chart for category distribution."""
    sales_by_category = df_filtered.groupby(CATEGORY_COL)[SALES_COL].sum().reset_index()
    
    fig = px.pie(
        sales_by_category,
        values=SALES_COL,
        names=CATEGORY_COL,
        title='Revenue Distribution by Category',
        color_discrete_sequence=['#164E63', '#0E7490', '#0891B2', '#06B6D4', '#22D3EE', '#67E8F9']
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig


def create_category_bar_chart(df_filtered):
    """Creates a horizontal bar chart for categories."""
    sales_by_category = df_filtered.groupby(CATEGORY_COL)[SALES_COL].sum().reset_index()
    sales_by_category = sales_by_category.sort_values(by=SALES_COL, ascending=False)
    
    fig = px.bar(
        sales_by_category,
        x=SALES_COL,
        y=CATEGORY_COL,
        orientation='h',
        title='Revenue by Category',
        labels={SALES_COL: 'Revenue (Ksh)', CATEGORY_COL: 'Category'},
        color=SALES_COL,
        color_continuous_scale=[[0, '#164E63'], [0.5, '#0891B2'], [1, '#67E8F9']],
        text=SALES_COL
    )
    fig.update_traces(texttemplate='Ksh %{text:,.0f}', textposition='outside')
    fig.update_layout(height=400, showlegend=False)
    
    return fig


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- APPLY CUSTOM STYLING ---
st.markdown(get_custom_css(), unsafe_allow_html=True)

# --- CUSTOM HEADER ---
st.markdown(
    get_header_html(
        "📊 Sales Analytics Dashboard",
        "Real-time insights and performance metrics for data-driven decisions"
    ),
    unsafe_allow_html=True
)

# --- DATA LOADING ---
df = load_data(DATA_FILE)

if df is None:
    st.stop()

# =================================================================
# === SIDEBAR FILTERS ===
# =================================================================
with st.sidebar:
    st.markdown("### 🎛️ Filter Controls")
    st.markdown("---")
    
    # Date Range Filter
    st.markdown("#### 📅 Date Range")
    min_date = df[DATE_COL].min().date()
    max_date = df[DATE_COL].max().date()
    
    date_range = st.date_input(
        "Select period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Region Filter
    st.markdown("#### 🌍 Region")
    selected_regions = st.multiselect(
        "Select regions to analyze",
        options=sorted(df[REGION_COL].unique()),
        default=df[REGION_COL].unique(),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Category Filter
    st.markdown("#### 📦 Product Category")
    selected_categories = st.multiselect(
        "Select product categories",
        options=sorted(df[CATEGORY_COL].unique()),
        default=df[CATEGORY_COL].unique(),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("### 📈 Quick Stats")
    total_records = len(df)
    date_range_text = f"{min_date} to {max_date}"
    st.info(f"**Total Records:** {total_records:,}")
    st.info(f"**Date Range:** {date_range_text}")

# --- APPLY FILTERS ---
if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    
    df_filtered = df[
        (df[DATE_COL] >= start_date) & 
        (df[DATE_COL] <= end_date) &
        (df[REGION_COL].isin(selected_regions)) &
        (df[CATEGORY_COL].isin(selected_categories))
    ].copy()
else:
    st.warning("⚠️ Please select a complete date range.")
    st.stop() 

if df_filtered.empty:
    st.error("❌ No data available based on current filters. Try widening your selection.")
    st.stop()

# =================================================================
# === 1. KEY PERFORMANCE INDICATORS ===
# =================================================================
st.markdown(
    get_section_header_html('🎯 Key Performance Indicators'),
    unsafe_allow_html=True
)

# Calculate KPIs
total_sales = df_filtered[SALES_COL].sum()
avg_sales = df_filtered[SALES_COL].mean()
total_orders = df_filtered[ORDER_ID_COL].nunique()
top_product = df_filtered.groupby('product')[SALES_COL].sum().idxmax()

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"Ksh {total_sales:,.0f}",
        delta=f"{(total_sales/1000000):.1f}M"
    )

with col2:
    st.metric(
        label="📊 Average Order",
        value=f"Ksh {avg_sales:,.0f}",
        delta="Per transaction"
    )

with col3:
    st.metric(
        label="🛒 Total Orders",
        value=f"{total_orders:,}",
        delta=f"{len(df_filtered)} items"
    )
    
with col4:
    st.metric(
        label="🏆 Top Product",
        value=top_product[:20] + "..." if len(top_product) > 20 else top_product,
        delta="Best seller"
    )

st.markdown("<br>", unsafe_allow_html=True)

# =================================================================
# === 2. PERFORMANCE TRENDS ===
# =================================================================
st.markdown(
    get_section_header_html('📈 Performance Trends'),
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["📅 Time Series", "🌍 Regional Analysis", "📦 Category Breakdown"])

with tab1:
    fig_time = create_time_series_chart(df_filtered)
    st.plotly_chart(fig_time, use_container_width=True)

with tab2:
    fig_region = create_regional_chart(df_filtered)
    st.plotly_chart(fig_region, use_container_width=True)

with tab3:
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_pie = create_category_pie_chart(df_filtered)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_b:
        fig_cat = create_category_bar_chart(df_filtered)
        st.plotly_chart(fig_cat, use_container_width=True)

# =================================================================
# === 3. DATA INSIGHTS ===
# =================================================================
st.markdown(
    get_section_header_html('💡 Data Insights'),
    unsafe_allow_html=True
)

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown("### 📊 Top 5 Products")
    top_products = df_filtered.groupby('product')[SALES_COL].sum().sort_values(ascending=False).head(5)
    for idx, (product, sales) in enumerate(top_products.items(), 1):
        st.markdown(f"**{idx}.** {product[:30]}... - Ksh {sales:,.0f}")

with insight_col2:
    st.markdown("### 🌟 Top 3 Regions")
    top_regions = df_filtered.groupby(REGION_COL)[SALES_COL].sum().sort_values(ascending=False).head(3)
    for idx, (region, sales) in enumerate(top_regions.items(), 1):
        st.markdown(f"**{idx}.** {region} - Ksh {sales:,.0f}")

with insight_col3:
    st.markdown("### 📈 Growth Metrics")
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    st.markdown(f"**Avg Order Value:** Ksh {avg_order_value:,.0f}")
    st.markdown(f"**Total Categories:** {df_filtered[CATEGORY_COL].nunique()}")
    st.markdown(f"**Active Regions:** {df_filtered[REGION_COL].nunique()}")

# =================================================================
# === 4. DATA EXPORT & PREVIEW ===
# =================================================================
st.markdown(
    get_section_header_html('📥 Data Export & Preview'),
    unsafe_allow_html=True
)

# Download section
col_dl1, col_dl2, col_dl3 = st.columns([2, 1, 1])

with col_dl1:
    excel_data = to_excel(df_filtered)
    st.download_button(
        label="⬇️ Download Filtered Data as Excel",
        data=excel_data,
        file_name=f'Sales_Analytics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_dl2:
    st.metric("Records", f"{len(df_filtered):,}")

with col_dl3:
    st.metric("Columns", len(df_filtered.columns))

# Data preview with search
st.markdown("### 🔍 Filtered Data Preview")

search_term = st.text_input("🔎 Search in data", placeholder="Enter search term...")

if search_term:
    mask = df_filtered.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
    preview_df = df_filtered[mask]
    st.info(f"Found {len(preview_df)} matching records")
else:
    preview_df = df_filtered

st.dataframe(
    preview_df,
    use_container_width=True,
    height=400,
    column_config={
        SALES_COL: st.column_config.NumberColumn(
            "Total Sales",
            format="Ksh %.2f"
        ),
        DATE_COL: st.column_config.DateColumn(
            "Order Date",
            format="DD/MM/YYYY"
        )
    }
)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    get_footer_html(datetime.now().strftime('%B %d, %Y at %H:%M')),
    unsafe_allow_html=True
)
