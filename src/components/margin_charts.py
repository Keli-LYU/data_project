"""
融资融券分析图表组件
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_margin_trend_chart(df_sh, df_sz):
    """
    创建融资融券余额趋势图
    
    Args:
        df_sh (pd.DataFrame): 沪市融资融券数据
        df_sz (pd.DataFrame): 深市融资融券数据
        
    Returns:
        plotly.graph_objects.Figure: 融资融券余额趋势图
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=('融资融券余额趋势', '融资余额对比'),
        vertical_spacing=0.1,
        row_heights=[0.5, 0.5]
    )
    
    # 第一个子图：融资融券总余额
    fig.add_trace(
        go.Scatter(
            x=df_sh['date'],
            y=df_sh['margin_balance'] / 100000000,  # 转换为亿元
            mode='lines',
            name='沪市融资融券余额',
            line=dict(color='red', width=2)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_sz['date'],
            y=df_sz['margin_balance'] / 100000000,  # 转换为亿元
            mode='lines',
            name='深市融资融券余额',
            line=dict(color='green', width=2)
        ),
        row=1, col=1
    )
    
    # 第二个子图：融资余额对比
    fig.add_trace(
        go.Scatter(
            x=df_sh['date'],
            y=df_sh['financing_balance'] / 100000000,  # 转换为亿元
            mode='lines',
            name='沪市融资余额',
            line=dict(color='orange', width=2)
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_sz['date'],
            y=df_sz['financing_balance'] / 100000000,  # 转换为亿元
            mode='lines',
            name='深市融资余额',
            line=dict(color='blue', width=2)
        ),
        row=2, col=1
    )
    
    # 更新布局
    fig.update_xaxes(title_text="日期", row=2, col=1)
    fig.update_yaxes(title_text="余额 (亿元)", row=1, col=1)
    fig.update_yaxes(title_text="余额 (亿元)", row=2, col=1)
    
    fig.update_layout(
        height=800,
        hovermode='x unified',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig


def create_margin_components_chart(df, market_name='沪市'):
    """
    创建融资融券各组成部分的堆叠面积图
    
    Args:
        df (pd.DataFrame): 融资融券数据
        market_name (str): 市场名称
        
    Returns:
        plotly.graph_objects.Figure: 堆叠面积图
    """
    fig = go.Figure()
    
    # 融资买入额
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['financing_purchase'] / 100000000,
        mode='lines',
        name='融资买入',
        stackgroup='one',
        line=dict(width=0.5, color='rgb(255, 127, 80)')
    ))
    
    # 融资偿还额
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['financing_redeem'] / 100000000,
        mode='lines',
        name='融资偿还',
        stackgroup='one',
        line=dict(width=0.5, color='rgb(100, 149, 237)')
    ))
    
    fig.update_layout(
        title=f'{market_name}融资买入与偿还趋势',
        xaxis_title='日期',
        yaxis_title='金额 (亿元)',
        height=500,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def create_margin_balance_change_chart(df_sh, df_sz):
    """
    创建融资融券余额变化率图表
    
    Args:
        df_sh (pd.DataFrame): 沪市融资融券数据
        df_sz (pd.DataFrame): 深市融资融券数据
        
    Returns:
        plotly.graph_objects.Figure: 余额变化率图表
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=df_sh['date'],
            y=df_sh['margin_balance_change'],
            mode='lines',
            name='沪市余额变化率',
            line=dict(color='red', width=1.5)
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_sz['date'],
            y=df_sz['margin_balance_change'],
            mode='lines',
            name='深市余额变化率',
            line=dict(color='green', width=1.5)
        )
    )
    
    # 添加0轴参考线
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title='融资融券余额变化率',
        xaxis_title='日期',
        yaxis_title='变化率 (%)',
        height=400,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def create_margin_heatmap(df, market_name='沪市'):
    """
    创建融资融券月度热力图
    
    Args:
        df (pd.DataFrame): 融资融券数据
        market_name (str): 市场名称
        
    Returns:
        plotly.graph_objects.Figure: 热力图
    """
    # 按月份聚合数据
    df_monthly = df.copy()
    df_monthly['year'] = df_monthly['date'].dt.year
    df_monthly['month'] = df_monthly['date'].dt.month
    
    # 计算每月平均余额
    pivot_data = df_monthly.groupby(['year', 'month'])['margin_balance'].mean().reset_index()
    pivot_data['margin_balance'] = pivot_data['margin_balance'] / 100000000  # 转为亿元
    
    # 创建透视表
    heatmap_data = pivot_data.pivot(index='month', columns='year', values='margin_balance')
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='RdYlGn',
        text=heatmap_data.values,
        texttemplate='%{text:.0f}',
        textfont={"size": 10},
        colorbar=dict(title="余额(亿元)")
    ))
    
    fig.update_layout(
        title=f'{market_name}融资融券月度平均余额热力图',
        xaxis_title='年份',
        yaxis_title='月份',
        height=500,
        template='plotly_white'
    )
    
    return fig
