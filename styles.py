# styles.py
"""
UI/UX Styling Module for Sales Dashboard
Contains all CSS styles and UI helper functions
"""

def get_custom_css():
    """
    Returns custom CSS styling for the dashboard.
    This centralizes all UI/UX design in one place.
    """
    return """
    <style>
    /* ============================================
       THEME VARIABLES
       ============================================ */
    :root {
        --primary-color: #0E7490;
        --secondary-color: #06B6D4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --teal-dark: #164E63;
        --teal-medium: #0891B2;
        --teal-light: #67E8F9;
        --gradient-primary: linear-gradient(135deg, #0E7490 0%, #06B6D4 100%);
        --gradient-dark: linear-gradient(180deg, #164E63 0%, #0E7490 100%);
    }
    
    /* ============================================
       GLOBAL SETTINGS
       ============================================ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ============================================
       METRIC CARDS
       ============================================ */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #1e293b;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="metric-container"] {
        background: var(--gradient-primary);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.2);
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"],
    div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    /* ============================================
       SIDEBAR
       ============================================ */
    [data-testid="stSidebar"] {
        background: var(--gradient-dark);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: white;
    }
    
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* ============================================
       HEADER SECTION
       ============================================ */
    .main-header {
        background: var(--gradient-primary);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        animation: fadeInDown 0.6s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* ============================================
       SECTION HEADERS
       ============================================ */
    .section-header {
        background: linear-gradient(90deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--primary-color);
        margin: 2rem 0 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .section-header h2 {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* ============================================
       CHART CONTAINERS
       ============================================ */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        transition: box-shadow 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
    }
    
    /* ============================================
       BUTTONS
       ============================================ */
    .stDownloadButton button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.2);
    }
    
    /* ============================================
       DATAFRAME
       ============================================ */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* ============================================
       INFO BOXES
       ============================================ */
    .info-box {
        background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left-color: var(--success-color);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left-color: var(--warning-color);
    }
    
    /* ============================================
       TABS
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary);
        color: white;
    }
    
    /* ============================================
       ANIMATIONS
       ============================================ */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* ============================================
       CUSTOM COMPONENTS
       ============================================ */
    .metric-card-custom {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary-color);
        transition: transform 0.3s ease;
    }
    
    .metric-card-custom:hover {
        transform: translateX(5px);
    }
    
    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-top: 3px solid var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .insight-card h3 {
        color: var(--primary-color);
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.75rem;
        }
        
        .main-header p {
            font-size: 0.95rem;
        }
    }
    </style>
    """


def get_header_html(title, subtitle):
    """
    Returns HTML for the main dashboard header.
    
    Args:
        title (str): Main title text
        subtitle (str): Subtitle/description text
    """
    return f"""
    <div class="main-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """


def get_section_header_html(title):
    """
    Returns HTML for section headers.
    
    Args:
        title (str): Section title text
    """
    return f'<div class="section-header"><h2>{title}</h2></div>'


def get_info_box_html(content, box_type="info"):
    """
    Returns HTML for styled info boxes.
    
    Args:
        content (str): Content to display
        box_type (str): Type of box - 'info', 'success', 'warning'
    """
    box_class = f"{box_type}-box" if box_type != "info" else "info-box"
    return f'<div class="{box_class}">{content}</div>'


def get_metric_card_html(icon, label, value, description=""):
    """
    Returns HTML for custom metric cards.
    
    Args:
        icon (str): Emoji or icon
        label (str): Metric label
        value (str): Metric value
        description (str): Optional description text
    """
    desc_html = f'<div style="color: #64748b; font-size: 0.875rem; margin-top: 0.5rem;">{description}</div>' if description else ''
    
    return f"""
    <div class="metric-card-custom">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: #64748b; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">
            {label}
        </div>
        <div style="color: #1e293b; font-size: 1.75rem; font-weight: 700;">
            {value}
        </div>
        {desc_html}
    </div>
    """


def get_insight_card_html(title, items):
    """
    Returns HTML for insight cards with lists.
    
    Args:
        title (str): Card title
        items (list): List of tuples (item_name, item_value)
    """
    items_html = ""
    for idx, (name, value) in enumerate(items, 1):
        items_html += f'<div style="padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;"><strong>{idx}.</strong> {name} - {value}</div>'
    
    return f"""
    <div class="insight-card">
        <h3>{title}</h3>
        {items_html}
    </div>
    """


def get_footer_html(update_time):
    """
    Returns HTML for dashboard footer.
    
    Args:
        update_time (str): Formatted timestamp
    """
    return f"""
    <div style='text-align: center; color: #64748b; padding: 1rem; margin-top: 2rem; border-top: 1px solid #e2e8f0;'>
        📊 Sales Analytics Dashboard | Made with Streamlit | Last updated: {update_time}
    </div>
    """


# Color schemes for different chart types
CHART_COLORS = {
    'primary': ['#0E7490', '#06B6D4', '#22D3EE', '#67E8F9', '#A5F3FC'],
    'teal_gradient': ['#164E63', '#0E7490', '#0891B2', '#06B6D4', '#22D3EE'],
    'success': ['#065f46', '#047857', '#059669', '#10b981', '#34d399'],
    'mixed': ['#0E7490', '#10b981', '#f59e0b', '#ef4444', '#06B6D4']
}


def get_plotly_theme():
    """
    Returns custom Plotly theme configuration.
    """
    return {
        'template': 'plotly_white',
        'colorway': CHART_COLORS['primary'],
        'font': {
            'family': 'Inter, sans-serif',
            'size': 12,
            'color': '#164E63'
        }
    }
