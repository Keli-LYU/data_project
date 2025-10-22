"""
指数分析图表组件
包含日线、周线、月线的K线图和趋势图
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from src.utils.clean_data import resample_to_weekly, resample_to_monthly


def create_candlestick_chart(df, title="Candlestick Chart", period="Daily"):
    """
    创建K线图
    
    Args:
        df (pd.DataFrame): 包含OHLC数据的DataFrame
        title (str): 图表标题
        period (str): 周期（日线/周线/月线）
        
    Returns:
        plotly.graph_objects.Figure: K线图对象
    """
    # 创建子图：K线图 + 成交量
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{title} - {period}', 'Volume'),
        row_heights=[0.7, 0.3]
    )
    
    # 添加K线图
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Candlestick',
            increasing_line_color='red',
            decreasing_line_color='green'
        ),
        row=1, col=1
    )
    
    # 如果有移动平均线数据，添加MA线
    if 'ma5' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ma5'],
                mode='lines',
                name='MA5',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
    
    if 'ma10' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ma10'],
                mode='lines',
                name='MA10',
                line=dict(color='orange', width=1)
            ),
            row=1, col=1
        )
    
    if 'ma20' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ma20'],
                mode='lines',
                name='MA20',
                line=dict(color='purple', width=1)
            ),
            row=1, col=1
        )
    
    # 添加成交量柱状图
    colors = ['red' if close >= open else 'green' 
              for close, open in zip(df['close'], df['open'])]
    
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['vol'],
            name='Volume',
            marker_color=colors,
            showlegend=False
        ),
        row=2, col=1
    )
    
    # 更新布局
    fig.update_layout(
        title=f'{title} - {period}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=700,
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig


def create_line_chart(df, title="Trend Chart"):
    """
    创建收盘价趋势线图
    
    Args:
        df (pd.DataFrame): 包含价格数据的DataFrame
        title (str): 图表标题
        
    Returns:
        plotly.graph_objects.Figure: 趋势线图对象
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='blue', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 100, 200, 0.2)'
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Close Price',
        height=400,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def create_comparison_chart(df_sh, df_sz, title="SH & SZ Index Comparison"):
    """
    创建沪深指数对比图
    
    Args:
        df_sh (pd.DataFrame): 沪市指数数据
        df_sz (pd.DataFrame): 深市指数数据
        title (str): 图表标题
        
    Returns:
        plotly.graph_objects.Figure: 对比图对象
    """
    # 标准化处理：以第一天的收盘价为基准
    sh_normalized = (df_sh['close'] / df_sh['close'].iloc[0]) * 100
    sz_normalized = (df_sz['close'] / df_sz['close'].iloc[0]) * 100
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=df_sh['date'],
            y=sh_normalized,
            mode='lines',
            name='Shanghai Comp.',
            line=dict(color='red', width=2)
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_sz['date'],
            y=sz_normalized,
            mode='lines',
            name='Shenzhen Comp.',
            line=dict(color='green', width=2)
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Normalized Index (Base=100)',
        height=500,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig
