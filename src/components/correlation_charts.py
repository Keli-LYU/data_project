"""
相关性分析图表组件
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def create_correlation_scatter(df1, df2, name1='Index 1', name2='Index 2'):
    """
    创建两个指数的散点图和相关性分析
    
    Args:
        df1 (pd.DataFrame): 第一个指数数据
        df2 (pd.DataFrame): 第二个指数数据
        name1 (str): 第一个指数名称
        name2 (str): 第二个指数名称
        
    Returns:
        plotly.graph_objects.Figure: 散点图
    """
    # 合并数据，确保日期对齐
    merged = pd.merge(
        df1[['date', 'close']],
        df2[['date', 'close']],
        on='date',
        suffixes=('_1', '_2')
    )
    
    # 计算相关系数
    correlation = np.corrcoef(merged['close_1'], merged['close_2'])[0, 1]
    
    fig = go.Figure()
    
    # 添加散点图
    fig.add_trace(
        go.Scatter(
            x=merged['close_1'],
            y=merged['close_2'],
            mode='markers',
            name='Data Points',
            marker=dict(
                size=5,
                color=merged.index,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Time Sequence")
            ),
            text=merged['date'].dt.strftime('%Y-%m-%d'),
            hovertemplate='<b>Date:</b> %{text}<br>' +
                         f'<b>{name1}:</b> %{{x:.2f}}<br>' +
                         f'<b>{name2}:</b> %{{y:.2f}}<extra></extra>'
        )
    )
    
    # 添加趋势线
    z = np.polyfit(merged['close_1'], merged['close_2'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(merged['close_1'].min(), merged['close_1'].max(), 100)
    
    fig.add_trace(
        go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode='lines',
            name='Trend Line',
            line=dict(color='red', width=2, dash='dash')
        )
    )
    
    fig.update_layout(
        title=f'{name1} vs {name2}<br>Correlation: {correlation:.4f}',
        xaxis_title=name1,
        yaxis_title=name2,
        height=600,
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig


def create_rolling_correlation(df1, df2, window=60, name1='Index 1', name2='Index 2'):
    """
    创建滚动相关性图表
    
    Args:
        df1 (pd.DataFrame): 第一个指数数据
        df2 (pd.DataFrame): 第二个指数数据
        window (int): 滚动窗口大小
        name1 (str): 第一个指数名称
        name2 (str): 第二个指数名称
        
    Returns:
        plotly.graph_objects.Figure: 滚动相关性图表
    """
    # 合并数据
    merged = pd.merge(
        df1[['date', 'close']],
        df2[['date', 'close']],
        on='date',
        suffixes=('_1', '_2')
    )
    
    # 计算滚动相关系数
    merged['rolling_corr'] = merged['close_1'].rolling(window=window).corr(merged['close_2'])
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=merged['date'],
            y=merged['rolling_corr'],
            mode='lines',
            name=f'{window}-Day Rolling Correlation',
            line=dict(color='blue', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 100, 200, 0.2)'
        )
    )
    
    # 添加参考线
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_hline(y=0.5, line_dash="dot", line_color="green", opacity=0.3)
    fig.add_hline(y=-0.5, line_dash="dot", line_color="red", opacity=0.3)
    
    fig.update_layout(
        title=f'{window}-Day Rolling Correlation between {name1} and {name2}',
        xaxis_title='Date',
        yaxis_title='Correlation Coefficient',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_dual_axis_chart(df1, df2, name1='Index 1', name2='Index 2'):
    """
    创建双Y轴对比图
    
    Args:
        df1 (pd.DataFrame): 第一个指数数据
        df2 (pd.DataFrame): 第二个指数数据
        name1 (str): 第一个指数名称
        name2 (str): 第二个指数名称
        
    Returns:
        plotly.graph_objects.Figure: 双Y轴图表
    """
    # 确保数据按日期对齐
    merged = pd.merge(
        df1[['date', 'close']],
        df2[['date', 'close']],
        on='date',
        suffixes=('_1', '_2')
    )
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 添加第一个指数
    fig.add_trace(
        go.Scatter(
            x=merged['date'],
            y=merged['close_1'],
            name=name1,
            line=dict(color='red', width=2)
        ),
        secondary_y=False
    )
    
    # 添加第二个指数
    fig.add_trace(
        go.Scatter(
            x=merged['date'],
            y=merged['close_2'],
            name=name2,
            line=dict(color='blue', width=2)
        ),
        secondary_y=True
    )
    
    # 设置坐标轴标题
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text=name1, secondary_y=False)
    fig.update_yaxes(title_text=name2, secondary_y=True)
    
    fig.update_layout(
        title=f'Trend Comparison: {name1} vs {name2}',
        height=500,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_return_comparison(df1, df2, name1='Index 1', name2='Index 2'):
    """
    创建收益率对比图
    
    Args:
        df1 (pd.DataFrame): 第一个指数数据
        df2 (pd.DataFrame): 第二个指数数据
        name1 (str): 第一个指数名称
        name2 (str): 第二个指数名称
        
    Returns:
        plotly.graph_objects.Figure: 收益率对比图
    """
    # 合并数据
    merged = pd.merge(
        df1[['date', 'close', 'change_pct']],
        df2[['date', 'close', 'change_pct']],
        on='date',
        suffixes=('_1', '_2')
    )
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=(f'{name1} Daily Return', f'{name2} Daily Return'),
        vertical_spacing=0.1
    )
    
    # 第一个指数的收益率
    fig.add_trace(
        go.Bar(
            x=merged['date'],
            y=merged['change_pct_1'],
            name=f'{name1} Return',
            marker_color=['red' if x >= 0 else 'green' for x in merged['change_pct_1']]
        ),
        row=1, col=1
    )
    
    # 第二个指数的收益率
    fig.add_trace(
        go.Bar(
            x=merged['date'],
            y=merged['change_pct_2'],
            name=f'{name2} Return',
            marker_color=['red' if x >= 0 else 'green' for x in merged['change_pct_2']]
        ),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Return (%)", row=1, col=1)
    fig.update_yaxes(title_text="Return (%)", row=2, col=1)
    
    fig.update_layout(
        height=700,
        template='plotly_white',
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig


def create_correlation_matrix(data_dict):
    """
    创建相关性矩阵热力图
    
    Args:
        data_dict (dict): 包含多个指数数据的字典
        
    Returns:
        plotly.graph_objects.Figure: 相关性矩阵热力图
    """
    # 准备数据
    df_list = []
    names = []
    
    for name, df in data_dict.items():
        df_temp = df[['date', 'close']].copy()
        df_temp.columns = ['date', name]
        df_list.append(df_temp)
        names.append(name)
    
    # 合并所有数据
    merged = df_list[0]
    for df in df_list[1:]:
        merged = pd.merge(merged, df, on='date', how='inner')
    
    # 计算相关性矩阵
    corr_matrix = merged[names].corr()
    
    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values,
        texttemplate='%{text:.3f}',
        textfont={"size": 12},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Index Correlation Matrix',
        height=500,
        template='plotly_white'
    )
    
    return fig
