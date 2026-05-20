"""Chart creation helpers with consistent styling."""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Color palette
COLORS = {
    'purple': '#667eea', 'dark_purple': '#764ba2',
    'pink': '#f093fb', 'red': '#f5576c',
    'orange': '#ff9a56', 'orange_end': '#f77062',
    'green': '#43e97b', 'teal': '#38f9d7',
    'blue': '#74b9ff', 'yellow': '#ffeaa7',
}

GRADIENT_COLORS = [
    '#667eea', '#764ba2', '#f093fb', '#f5576c',
    '#ff9a56', '#43e97b', '#74b9ff', '#a29bfe',
    '#fd79a8', '#00cec9'
]

def base_layout(title="", height=240, showlegend=True):
    """Return a consistent base layout dict for 1280x585 screen with NO gridlines."""
    return dict(
        title=dict(
            text=title, 
            font=dict(size=11, family='Outfit', color='#1f2937', weight='bold'), 
            x=0, 
            xanchor='left'
        ),
        font=dict(family='Outfit', size=9, color='#4b5563'),
        plot_bgcolor='white', 
        paper_bgcolor='white',
        height=height, 
        margin=dict(l=35, r=10, t=25, b=25),
        showlegend=showlegend,
        legend=dict(
            orientation='h', 
            yanchor='bottom', 
            y=1.02,
            xanchor='left', 
            x=0, 
            font=dict(size=9, family='Outfit'),
            bgcolor='rgba(0,0,0,0)', 
            borderwidth=0
        ),
        xaxis=dict(
            showgrid=False, 
            zeroline=False,
            showline=True, 
            linewidth=1, 
            linecolor='#e5e7eb',
            tickfont=dict(size=8, family='Outfit'), 
            automargin=True,
        ),
        yaxis=dict(
            showgrid=False, 
            zeroline=False,
            showline=False, 
            tickfont=dict(size=8, family='Outfit'), 
            automargin=True,
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white', 
            font_size=10, 
            font_family='Outfit',
            bordercolor='#e5e7eb'
        ),
    )


def line_chart(df, x_col, y_cols, names, colors=None, height=240, title=""):
    """Multi-line chart."""
    fig = go.Figure()
    if colors is None:
        colors = GRADIENT_COLORS
    for i, (col, name) in enumerate(zip(y_cols, names)):
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[col], name=name,
            mode='lines', line=dict(color=colors[i % len(colors)], width=1.8),
            hovertemplate='%{y:,.2f}<extra></extra>'
        ))
    fig.update_layout(**base_layout(title, height, showlegend=len(y_cols) > 1))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def area_chart(df, x_col, y_cols, names, colors=None, height=240, title=""):
    """Multi-area chart."""
    fig = go.Figure()
    if colors is None:
        colors = GRADIENT_COLORS
    for i, (col, name) in enumerate(zip(y_cols, names)):
        c = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[col], name=name,
            mode='lines', fill='tonexty' if i > 0 else 'tozeroy',
            line=dict(color=c, width=1.5),
            fillcolor=c.replace(')', ',0.08)').replace('rgb', 'rgba') if 'rgb' in c else f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.08)",
            hovertemplate='%{y:,.2f}<extra></extra>'
        ))
    fig.update_layout(**base_layout(title, height, showlegend=len(y_cols) > 1))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def dual_axis_chart(df, x_col, y1_col, y2_col, name1, name2, color1, color2, height=240, title=""):
    """Dual y-axis line chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col], y=df[y1_col], name=name1,
        mode='lines', line=dict(color=color1, width=1.8),
        hovertemplate='%{y:,.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df[x_col], y=df[y2_col], name=name2,
        mode='lines', line=dict(color=color2, width=1.8), yaxis='y2',
        hovertemplate='%{y:,.2f}<extra></extra>'
    ))
    layout = base_layout(title, height)
    layout['yaxis']['title'] = dict(text=name1, font=dict(size=9, family='Outfit', color=color1))
    layout['yaxis']['tickfont'] = dict(size=8, family='Outfit', color=color1)
    layout['yaxis2'] = dict(
        title=dict(text=name2, font=dict(size=9, family='Outfit', color=color2)),
        overlaying='y', side='right', showgrid=False, zeroline=False,
        tickfont=dict(size=8, family='Outfit', color=color2), automargin=True,
    )
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def bar_chart(categories, values, colors=None, height=240, title="", horizontal=False):
    """Bar chart."""
    if colors is None:
        colors = GRADIENT_COLORS[:len(categories)]
    orientation = 'h' if horizontal else 'v'
    x_vals, y_vals = (values, categories) if horizontal else (categories, values)
    fig = go.Figure(go.Bar(
        x=x_vals, y=y_vals, marker=dict(color=colors),
        orientation=orientation,
        text=[f'{v:,.1f}' if abs(v) < 100 else f'{v:,.0f}' for v in values], textposition='outside',
        textfont=dict(size=8, family='Outfit'),
        hovertemplate='%{x:,.2f}<extra></extra>' if horizontal else '%{y:,.2f}<extra></extra>'
    ))
    layout = base_layout(title, height, showlegend=False)
    if not horizontal:
        layout['xaxis']['tickangle'] = -30
    layout['margin']['b'] = 30 if not horizontal else 25
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def pct_bar_chart(categories, values, height=240, title=""):
    """Bar chart with percentage values, colored by pos/neg."""
    colors = ['#10b981' if v >= 0 else '#ef4444' for v in values]
    fig = go.Figure(go.Bar(
        x=categories, y=values,
        marker=dict(color=colors),
        text=[f'{v:+.1f}%' for v in values], textposition='outside',
        textfont=dict(size=8, family='Outfit'),
        hovertemplate='%{y:+.2f}%<extra></extra>'
    ))
    layout = base_layout(title, height, showlegend=False)
    layout['xaxis']['tickangle'] = -30
    layout['margin']['b'] = 30
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def heatmap_chart(corr_matrix, labels, height=240, title=""):
    """Correlation heatmap."""
    fig = go.Figure(go.Heatmap(
        z=corr_matrix.values, x=labels, y=labels,
        colorscale=[[0, '#ef4444'], [0.5, '#ffffff'], [1, '#4f46e5']],
        zmin=-1, zmax=1,
        text=np.round(corr_matrix.values, 2), texttemplate='%{text}',
        textfont=dict(size=8, family='Outfit'),
        hovertemplate='%{x} vs %{y}: %{z:.2f}<extra></extra>',
        colorbar=dict(thickness=8, tickfont=dict(size=8, family='Outfit'))
    ))
    layout = base_layout(title, height, showlegend=False)
    layout['xaxis']['tickangle'] = -45
    layout['margin'] = dict(l=40, r=10, t=25, b=40)
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def candlestick_style_line(df, x_col, y_col, color='#667eea', height=240, title=""):
    """Single line with filled area below."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col], y=df[y_col], mode='lines',
        line=dict(color=color, width=1.8),
        fill='tozeroy',
        fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.05)",
        hovertemplate='%{y:,.2f}<extra></extra>'
    ))
    fig.update_layout(**base_layout(title, height, showlegend=False))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def scatter_plot(df, x_col, y_col, name_x, name_y, color='#7c3aed', height=240, title=""):
    """Scatter plot with trendline."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col], y=df[y_col], mode='markers',
        marker=dict(color=color, size=4, opacity=0.7),
        name='Data',
        hovertemplate=f'{name_x}: %{{x:,.2f}}<br>{name_y}: %{{y:,.2f}}<extra></extra>'
    ))
    mask = ~df[x_col].isna() & ~df[y_col].isna()
    if mask.sum() > 1:
        x_clean = df.loc[mask, x_col]
        y_clean = df.loc[mask, y_col]
        poly = np.polyfit(x_clean, y_clean, 1)
        trend_y = np.polyval(poly, x_clean)
        fig.add_trace(go.Scatter(
            x=x_clean, y=trend_y, mode='lines',
            line=dict(color='#f97316', width=1.2, dash='dash'),
            name='Tren',
            hovertemplate='Garis Tren<extra></extra>'
        ))
    layout = base_layout(title, height, showlegend=False)
    layout['xaxis']['title'] = dict(text=name_x, font=dict(size=9, family='Outfit'))
    layout['yaxis']['title'] = dict(text=name_y, font=dict(size=9, family='Outfit'))
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig
