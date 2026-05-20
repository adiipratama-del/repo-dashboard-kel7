"""Interactive Streamlit Dashboard — Nilai Tukar Rupiah & IHSG."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import textwrap
from data_loader import load_data
from charts import (
    line_chart, area_chart, dual_axis_chart, bar_chart,
    pct_bar_chart, heatmap_chart, candlestick_style_line,
    scatter_plot, GRADIENT_COLORS, COLORS
)

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Nilai Tukar & IHSG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Inject Premium Custom CSS for 1280x585 Viewport ──
st.markdown("""
<style>
    /* Load Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Apply Font Globally */
    * {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Background and Layout */
    html, body, [data-testid="stApp"] {
        background-color: #f8fafc !important;
        overflow-x: hidden !important;
        overflow-y: auto !important; 
    }
    
    /* Push main view container all the way to the top */
    [data-testid="stHeader"], .stAppHeader, header {
        display: none !important;
        height: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    
    /* Minimize Streamlit default container margins & paddings */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 0px !important;
        margin-top: 0px !important;
        padding-bottom: 8px !important;
        padding-left: 15px !important;
        padding-right: 15px !important;
    }
    
    /* Spacing between columns and blocks (natural flow, no zero margins to avoid overlaps) */
    div[data-testid="stVerticalBlock"] {
        gap: 12px !important;
    }
    
    /* Title header container — Ultra Compact & at absolute top */
    .title-container {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        padding: 4px 12px;
        border-radius: 6px;
        box-shadow: 0 2px 10px rgba(30, 27, 75, 0.08);
        margin-top: 0px;
        margin-bottom: 2px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .title-text {
        font-size: 12px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.5px;
        line-height: 1.1;
    }
    .subtitle-text {
        font-size: 8px;
        color: #c7d2fe;
        font-weight: 500;
    }
    
    /* Premium Tab Navigation */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #ffffff !important;
        padding: 3px !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
        border-bottom: none !important;
        gap: 5px !important;
        margin-bottom: 2px !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 4px 12px !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        border-radius: 5px !important;
        color: #4b5563 !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
        height: 24px !important;
        line-height: 24px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #4f46e5 !important;
        background-color: #f3f4f6 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2) !important;
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] div {
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-border-highlight"] {
        display: none !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2px !important;
    }
    
    /* Custom simple tables */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 1px 6px rgba(0, 0, 0, 0.02);
        background-color: #ffffff;
    }
    .custom-table th {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        font-size: 8px;
        text-transform: uppercase;
        font-weight: 700;
        padding: 4px 8px;
        text-align: left;
        letter-spacing: 0.5px;
    }
    .custom-table td {
        font-size: 8px;
        padding: 4px 8px;
        border-bottom: 1px solid #f3f4f6;
        color: #1f2937;
        font-weight: 500;
        line-height: 1.1;
    }
    .custom-table tr:last-child td {
        border-bottom: none;
    }
    .custom-table tr:hover td {
        background-color: #f9fafb;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────
@st.cache_data
def get_cached_data():
    return load_data()

df_fx, df_ihsg, CURR_NAMES, SECTOR_NAMES, CURR_COLS, SECTOR_COLS = get_cached_data()

df_merged = pd.merge(
    df_fx, df_ihsg[['time', 'composite']],
    left_on='Tanggal', right_on='time', how='inner'
).drop(columns=['time'])

# ── Helpers ────────────────────────────────────────────────
def clean_html(html_str):
    """Strip all newlines and indentation to prevent streamlit markdown code-block parsing."""
    return "".join(line.strip() for line in html_str.splitlines())

def make_html_kpi(label, value, subtext=None, theme='purple'):
    gradients = {
        'purple': ('linear-gradient(135deg, #4f46e5, #7c3aed)', 'rgba(79, 70, 229, 0.12)'),
        'green': ('linear-gradient(135deg, #10b981, #059669)', 'rgba(16, 185, 129, 0.12)'),
        'red': ('linear-gradient(135deg, #ef4444, #dc2626)', 'rgba(239, 68, 68, 0.12)'),
        'blue': ('linear-gradient(135deg, #0284c7, #0369a1)', 'rgba(2, 132, 199, 0.12)'),
        'indigo': ('linear-gradient(135deg, #3f51b5, #5c6bc0)', 'rgba(63, 81, 181, 0.12)'),
    }
    grad, shadow = gradients.get(theme, gradients['purple'])
    sub_html = f'<div style="font-size: 8px; color: rgba(255,255,255,0.85); font-weight: 500; margin-top: 1px;">{subtext}</div>' if subtext else ''
    return f"""
    <div style="
        flex: 1;
        background: {grad};
        border-radius: 6px;
        padding: 5px 8px;
        box-shadow: 0 3px 8px {shadow};
        text-align: center;
        line-height: 1.1;
        min-width: 0;
    ">
        <div style="font-size: 8px; text-transform: uppercase; color: rgba(255,255,255,0.85); font-weight: 700; margin-bottom: 1px; letter-spacing: 0.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{label}</div>
        <div style="font-size: 13px; font-weight: 800; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{value}</div>
        {sub_html}
    </div>
    """

def make_kpi_row(cards_html_list):
    cards_html = "".join(cards_html_list)
    return clean_html(f"""
    <div style="display: flex; gap: 5px; width: 100%; margin-bottom: 4px;">
        {cards_html}
    </div>
    """)

SHORT_SECTORS = {
    'Basic Materials': 'Basic Mat',
    'Non-Cyclical': 'Non-Cyc',
    'Healthcare': 'Health',
    'Property': 'Prop',
    'Technology': 'Tech',
    'Transportation': 'Trans',
    'Industrial': 'Indust',
    'Finance': 'Finance',
    'Energy': 'Energy',
    'Infrastructure': 'Infra',
    'Cyclical': 'Cyc'
}

def get_filtered_df_by_period(df, date_col, period):
    max_date = df[date_col].max()
    if period == "YTD":
        start_date = pd.to_datetime(f"{max_date.year}-01-01")
    elif period == "1 Tahun":
        start_date = max_date - pd.DateOffset(years=1)
    elif period == "6 Bulan":
        start_date = max_date - pd.DateOffset(months=6)
    else:  # Semua
        start_date = df[date_col].min()
    
    mask = (df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(max_date))
    return df[mask] if mask.any() else df

# ── Header Title — Ultra Compact ────────────────────────────
st.html(clean_html("""
<div class="title-container">
    <div class="title-text">Dashboard Nilai Tukar & IHSG</div>
    <div class="subtitle-text">Analisis Pasar Keuangan Indonesia</div>
</div>
"""))

# ── Tabs Setup ──────────────────────────────────────────────
tab_overview, tab_rates, tab_ihsg = st.tabs(["Overview", "Exchange Rates", "IHSG Sektoral"])

# Highly compact chart height for 1280x585 viewport to prevent scrollbars
H_CHART = 140

# ── TAB 1: OVERVIEW ──────────────────────────────────────────
with tab_overview:
    latest_year = df_ihsg['time'].max().year
    start_of_year = pd.to_datetime(f"{latest_year}-01-01")
    
    ytd_ihsg = df_ihsg[df_ihsg['time'] >= start_of_year]
    ihsg_start = ytd_ihsg.iloc[0]['composite']
    ihsg_end = ytd_ihsg.iloc[-1]['composite']
    ihsg_ytd_return = ((ihsg_end - ihsg_start) / ihsg_start) * 100
    
    sec_returns = {}
    for col in SECTOR_COLS:
        if col != 'composite':
            s_start = ytd_ihsg.iloc[0][col]
            s_end = ytd_ihsg.iloc[-1][col]
            sec_returns[col] = ((s_end - s_start) / s_start) * 100
            
    best_sec = max(sec_returns, key=sec_returns.get)
    worst_sec = min(sec_returns, key=sec_returns.get)
    
    ytd_fx = df_fx[df_fx['Tanggal'] >= start_of_year]
    usd_max = ytd_fx['USDIDR'].max()
    usd_min = ytd_fx['USDIDR'].min()
    
    # 1. YTD KPI cards (Top)
    kpi_cards = [
        make_html_kpi("IHSG Return (YTD)", f"{ihsg_ytd_return:+.1f}%", "Indeks Gabungan", "purple"),
        make_html_kpi("Sektor Terbaik (YTD)", SHORT_SECTORS.get(SECTOR_NAMES[best_sec], SECTOR_NAMES[best_sec]), f"{sec_returns[best_sec]:+.1f}%", "green"),
        make_html_kpi("Sektor Terburuk (YTD)", SHORT_SECTORS.get(SECTOR_NAMES[worst_sec], SECTOR_NAMES[worst_sec]), f"{sec_returns[worst_sec]:+.1f}%", "red"),
        make_html_kpi("USD/IDR Max (YTD)", f"Rp {usd_max:,.0f}", "Rupiah Terlemah", "indigo"),
        make_html_kpi("USD/IDR Min (YTD)", f"Rp {usd_min:,.0f}", "Rupiah Terkuat", "blue")
    ]
    st.html(make_kpi_row(kpi_cards))
    
    # 2. Filter (Below KPIs)
    ov_period = st.selectbox("Periode Analisis:", ["Semua", "YTD", "1 Tahun", "6 Bulan"], key="ov_p_sel", index=0)
    df_filtered = get_filtered_df_by_period(df_merged, 'Tanggal', ov_period)
    
    # 3. Row 1: Line Chart (65%) + Area Chart of Top 3 Currencies (35%)
    r1_col1, r1_col2 = st.columns([65, 35])
    with r1_col1:
        fig1 = dual_axis_chart(df_filtered, 'Tanggal', 'USDIDR', 'composite',
                               'USD/IDR', 'IHSG Composite',
                               '#4f46e5', '#ec4899', height=H_CHART)
        st.plotly_chart(fig1, use_container_width=True, theme=None, config={'displayModeBar': False})
    with r1_col2:
        fig_area = area_chart(df_filtered, 'Tanggal', ['USDIDR', 'EURIDR', 'GBPIDR'], 
                              ['USD/IDR', 'EUR/IDR', 'GBP/IDR'], height=H_CHART)
        fig_area.update_layout(title=dict(text="Tren 3 Mata Uang Utama", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_area, use_container_width=True, theme=None, config={'displayModeBar': False})
    
    # 4. Row 2: Bar Chart (50%) + Sector Return Table (50%)
    col1, col2 = st.columns([1, 1])
    with col1:
        changes = []
        for col in CURR_COLS:
            c_start = df_filtered[col].iloc[0]
            c_end = df_filtered[col].iloc[-1]
            chg = ((c_end - c_start) / c_start) * 100
            changes.append((CURR_NAMES[col], chg))
        changes = sorted(changes, key=lambda x: x[1])
        cats, vals = zip(*changes)
        
        m_colors = ['#10b981' if v >= 0 else '#ef4444' for v in vals]
        fig2 = bar_chart(list(cats), list(vals), colors=m_colors, height=H_CHART, horizontal=True)
        fig2.update_layout(title=dict(text="Performa Mata Uang terhadap Rupiah (% Perubahan)", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig2, use_container_width=True, theme=None, config={'displayModeBar': False})
        
    with col2:
        table_rows = []
        for col in SECTOR_COLS:
            if col != 'composite':
                s_name = SHORT_SECTORS.get(SECTOR_NAMES[col], SECTOR_NAMES[col])
                val = sec_returns[col]
                color = "#10b981" if val >= 0 else "#ef4444"
                sign = "+" if val >= 0 else ""
                table_rows.append(f"""
                <tr>
                    <td style="font-weight: 600; padding: 4px 8px;">{s_name}</td>
                    <td style="text-align: right; font-weight: 700; color: {color}; padding: 4px 8px;">{sign}{val:.1f}%</td>
                </tr>
                """)
        table_html = f"""
        <table class="custom-table">
            <thead>
                <tr>
                    <th style="padding: 4px 8px;">Sektor</th>
                    <th style="text-align: right; padding: 4px 8px;">Return YTD</th>
                </tr>
            </thead>
            <tbody>
                {"".join(table_rows)}
            </tbody>
        </table>
        """
        st.html(clean_html(table_html))

# ── TAB 2: EXCHANGE RATES ───────────────────────────────────
with tab_rates:
    df_fx_filt_temp = get_filtered_df_by_period(df_fx, 'Tanggal', 'Semua')
    base_c_temp = 'USDIDR'
    latest_fx_val_temp = df_fx_filt_temp[base_c_temp].iloc[-1]
    
    ytd_base_start_temp = ytd_fx[base_c_temp].iloc[0]
    ytd_base_end_temp = ytd_fx[base_c_temp].iloc[-1]
    base_ytd_temp = ((ytd_base_end_temp - ytd_base_start_temp) / ytd_base_start_temp) * 100
    
    base_max_temp = df_fx_filt_temp[base_c_temp].max()
    base_max_dt_temp = df_fx_filt_temp.loc[df_fx_filt_temp[base_c_temp].idxmax(), 'Tanggal'].strftime('%d %b')
    base_min_temp = df_fx_filt_temp[base_c_temp].min()
    base_min_dt_temp = df_fx_filt_temp.loc[df_fx_filt_temp[base_c_temp].idxmin(), 'Tanggal'].strftime('%d %b')
    
    # 1. KPIs on top of Tab 2
    base_theme_temp = "green" if base_ytd_temp >= 0 else "red"
    fx_kpis = [
        make_html_kpi(f"Terakhir (USD/IDR)", f"Rp {latest_fx_val_temp:,.0f}", "Kurs Penutupan Terbaru", "purple"),
        make_html_kpi("Perubahan YTD", f"{base_ytd_temp:+.1f}%", f"Pertumbuhan Kurs {latest_year}", base_theme_temp),
        make_html_kpi("Tertinggi (Periode)", f"Rp {base_max_temp:,.0f}", f"Obs: {base_max_dt_temp}", "indigo"),
        make_html_kpi("Terendah (Periode)", f"Rp {base_min_temp:,.0f}", f"Obs: {base_min_dt_temp}", "blue")
    ]
    st.html(make_kpi_row(fx_kpis))
    
    # 2. Filters below KPIs
    col_rf1, col_rf2 = st.columns([1, 1])
    with col_rf1:
        selected_curr = st.multiselect(
            "Pilih Mata Uang untuk Dibandingkan:",
            options=CURR_COLS,
            format_func=lambda x: CURR_NAMES[x],
            default=['USDIDR', 'EURIDR'],
            key="fx_select"
        )
    with col_rf2:
        fx_period = st.selectbox(
            "Periode Analisis:",
            options=["Semua", "YTD", "1 Tahun", "6 Bulan"],
            key="fx_p_sel",
            index=0
        )
        
    df_fx_filt = get_filtered_df_by_period(df_fx, 'Tanggal', fx_period)
    
    # 3. Row 1: Line Chart (65%) + Single Currency Details Area Chart (35%)
    r2_col1, r2_col2 = st.columns([65, 35])
    with r2_col1:
        curr_to_plot = selected_curr if selected_curr else CURR_COLS[:2]
        fig_fx1 = line_chart(df_fx_filt, 'Tanggal', curr_to_plot, [CURR_NAMES[c] for c in curr_to_plot], height=H_CHART)
        fig_fx1.update_layout(title=dict(text="Pergerakan Historis Kurs Nilai Tukar Rupiah", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_fx1, use_container_width=True, theme=None, config={'displayModeBar': False})
    with r2_col2:
        primary_c = selected_curr[0] if selected_curr else 'USDIDR'
        fig_single_area = candlestick_style_line(df_fx_filt, 'Tanggal', primary_c, color='#7c3aed', height=H_CHART)
        fig_single_area.update_layout(title=dict(text=f"Detail Tren {CURR_NAMES[primary_c]}", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_single_area, use_container_width=True, theme=None, config={'displayModeBar': False})
        
    # 4. Row 2: Table (50%) + Correlation Heatmap (50%)
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        latest_row = df_fx_filt.iloc[-1]
        prev_row = df_fx_filt.iloc[-2] if len(df_fx_filt) > 1 else latest_row
        
        table_rows = []
        for col in curr_to_plot:
            val = latest_row[col]
            pval = prev_row[col]
            chg = ((val - pval) / pval) * 100
            color = "#10b981" if chg >= 0 else "#ef4444"
            sign = "+" if chg >= 0 else ""
            table_rows.append(f"""
            <tr>
                <td style="font-weight: 600; padding: 4px 8px;">{CURR_NAMES[col]}</td>
                <td style="text-align: right; font-weight: 700; padding: 4px 8px;">Rp {val:,.0f}</td>
                <td style="text-align: right; font-weight: 700; color: {color}; padding: 4px 8px;">{sign}{chg:.2f}%</td>
            </tr>
            """)
        table_html = f"""
        <table class="custom-table">
            <thead>
                <tr>
                    <th style="padding: 6px 8px;">Mata Uang</th>
                    <th style="text-align: right; padding: 6px 8px;">Nilai</th>
                    <th style="text-align: right; padding: 6px 8px;">Harian (%)</th>
                </tr>
            </thead>
            <tbody>
                {"".join(table_rows)}
            </tbody>
        </table>
        """
        st.html(clean_html(table_html))
        
    with col_t2:
        corr_matrix = df_fx_filt[curr_to_plot].corr()
        fig_fx_corr = heatmap_chart(corr_matrix, [CURR_NAMES[c] for c in curr_to_plot], height=H_CHART)
        fig_fx_corr.update_layout(title=dict(text="Matriks Korelasi Pergerakan Kurs", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_fx_corr, use_container_width=True, theme=None, config={'displayModeBar': False})

# ── TAB 3: IHSG SEKTORAL ────────────────────────────────────
with tab_ihsg:
    prim_sec_temp = 'composite'
    df_ihsg_filt_temp = get_filtered_df_by_period(df_ihsg, 'time', 'Semua')
    latest_sec_val_temp = df_ihsg_filt_temp[prim_sec_temp].iloc[-1]
    
    ytd_sec_start_temp = ytd_ihsg[prim_sec_temp].iloc[0]
    ytd_sec_end_temp = ytd_ihsg[prim_sec_temp].iloc[-1]
    sec_ytd_temp = ((ytd_sec_end_temp - ytd_sec_start_temp) / ytd_sec_start_temp) * 100
    
    sec_max_temp = df_ihsg_filt_temp[prim_sec_temp].max()
    sec_max_dt_temp = df_ihsg_filt_temp.loc[df_ihsg_filt_temp[prim_sec_temp].idxmax(), 'time'].strftime('%d %b')
    sec_min_temp = df_ihsg_filt_temp[prim_sec_temp].min()
    sec_min_dt_temp = df_ihsg_filt_temp.loc[df_ihsg_filt_temp[prim_sec_temp].idxmin(), 'time'].strftime('%d %b')
    
    # 1. KPIs on top of Tab 3
    sec_theme_temp = "green" if sec_ytd_temp >= 0 else "red"
    sec_kpis = [
        make_html_kpi("Indeks IHSG Composite", f"{latest_sec_val_temp:,.1f}", "Nilai Penutupan Indeks", "purple"),
        make_html_kpi("Return YTD", f"{sec_ytd_temp:+.1f}%", f"Pertumbuhan Indeks {latest_year}", sec_theme_temp),
        make_html_kpi("Tertinggi (Periode)", f"{sec_max_temp:,.1f}", f"Obs: {sec_max_dt_temp}", "indigo"),
        make_html_kpi("Terendah (Periode)", f"{sec_min_temp:,.1f}", f"Obs: {sec_min_dt_temp}", "blue")
    ]
    st.html(make_kpi_row(sec_kpis))
    
    # 2. Filters below KPIs
    col_sf1, col_sf2 = st.columns([1, 1])
    with col_sf1:
        selected_sec = st.multiselect(
            "Pilih Sektor Indeks untuk Dibandingkan:",
            options=SECTOR_COLS,
            format_func=lambda x: SECTOR_NAMES[x],
            default=['composite', 'idxfinance'],
            key="sec_select"
        )
    with col_sf2:
        sec_period = st.selectbox(
            "Periode Analisis:",
            options=["Semua", "YTD", "1 Tahun", "6 Bulan"],
            key="sec_p_sel",
            index=0
        )
        
    df_ihsg_filt = get_filtered_df_by_period(df_ihsg, 'time', sec_period)
    
    # 3. Row 1: Sector Trends Chart (65%) + Sector comparison bar chart (35%)
    r3_col1, r3_col2 = st.columns([65, 35])
    with r3_col1:
        sec_to_plot = selected_sec if selected_sec else SECTOR_COLS[:2]
        fig_sec1 = line_chart(df_ihsg_filt, 'time', sec_to_plot, [SECTOR_NAMES[s] for s in sec_to_plot], height=H_CHART)
        fig_sec1.update_layout(title=dict(text="Pergerakan Historis Indeks Sektor IHSG", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_sec1, use_container_width=True, theme=None, config={'displayModeBar': False})
    with r3_col2:
        sec_chgs = []
        for s_col in sec_to_plot:
            s_start = df_ihsg_filt[s_col].iloc[0]
            s_end = df_ihsg_filt[s_col].iloc[-1]
            s_chg = ((s_end - s_start) / s_start) * 100
            sec_chgs.append((SHORT_SECTORS.get(SECTOR_NAMES[s_col], SECTOR_NAMES[s_col]), s_chg))
        sec_cats, sec_vals = zip(*sec_chgs)
        fig_sec_bar = pct_bar_chart(list(sec_cats), list(sec_vals), height=H_CHART)
        fig_sec_bar.update_layout(title=dict(text="Performa Sektor Pilihan (% Perubahan)", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_sec_bar, use_container_width=True, theme=None, config={'displayModeBar': False})
        
    # 4. Row 2: Volatility Chart (33%) + Correlation Scatter Plot (33%) + Sector Correlation Heatmap (34%)
    col_s1, col_s2, col_s3 = st.columns([33, 33, 34])
    prim_sec = selected_sec[0] if selected_sec else 'composite'
    with col_s1:
        pct_returns = df_ihsg_filt[prim_sec].pct_change() * 100
        vol_30d = pct_returns.rolling(window=30).std()
        df_vol = pd.DataFrame({'time': df_ihsg_filt['time'], 'vol': vol_30d}).dropna()
        
        fig_vol = line_chart(df_vol, 'time', ['vol'], [f'Vol 30d {SHORT_SECTORS.get(SECTOR_NAMES[prim_sec], SECTOR_NAMES[prim_sec])}'], colors=['#ef4444'], height=H_CHART)
        fig_vol.update_layout(title=dict(text=f"Volatilitas {SHORT_SECTORS.get(SECTOR_NAMES[prim_sec], SECTOR_NAMES[prim_sec])} (30 Hari)", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_vol, use_container_width=True, theme=None, config={'displayModeBar': False})
        
    with col_s2:
        df_scat = pd.merge(
            df_ihsg_filt[['time', prim_sec]],
            df_fx[['Tanggal', 'USDIDR']],
            left_on='time', right_on='Tanggal', how='inner'
        )
        fig_scatter = scatter_plot(
            df_scat, 'USDIDR', prim_sec,
            'USD/IDR', SHORT_SECTORS.get(SECTOR_NAMES[prim_sec], SECTOR_NAMES[prim_sec]),
            height=H_CHART
        )
        fig_scatter.update_layout(title=dict(text=f"Korelasi USD/IDR vs {SHORT_SECTORS.get(SECTOR_NAMES[prim_sec], SECTOR_NAMES[prim_sec])}", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_scatter, use_container_width=True, theme=None, config={'displayModeBar': False})
        
    with col_s3:
        corr_matrix_sec = df_ihsg_filt[sec_to_plot].corr()
        fig_sec_corr = heatmap_chart(corr_matrix_sec, [SHORT_SECTORS.get(SECTOR_NAMES[s], SECTOR_NAMES[s]) for s in sec_to_plot], height=H_CHART)
        fig_sec_corr.update_layout(title=dict(text="Matriks Korelasi Sektor", font=dict(size=10, family='Outfit')))
        st.plotly_chart(fig_sec_corr, use_container_width=True, theme=None, config={'displayModeBar': False})
