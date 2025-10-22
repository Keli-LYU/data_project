"""
融资融券分析页面
"""

from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from src.utils.clean_data import load_cleaned_data
from src.components.margin_charts import (
    create_margin_trend_chart,
    create_margin_components_chart,
    create_margin_balance_change_chart,
    create_margin_heatmap
)


def create_margin_analysis_page():
    """
    创建融资融券分析页面布局
    
    Returns:
        html.Div: 页面布局
    """
    layout = dbc.Container([
        html.H2("Margin Trading Analysis", className="text-center mb-4"),
        html.Hr(),
        
        # 沪深两市融资融券余额趋势
        dbc.Row([
            dbc.Col([
                html.H4("Margin Trading Balance Trend in SH & SZ Markets", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-margin-trend",
                    type="default",
                    children=[
                        dcc.Graph(id='margin-trend-chart'),
                    ]
                )
            ], width=12)
        ], className="mb-4"),
        
        # 余额变化率
        dbc.Row([
            dbc.Col([
                html.H4("Rate of Change of Margin Trading Balance", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-margin-change",
                    type="default",
                    children=[
                        dcc.Graph(id='margin-change-chart'),
                    ]
                )
            ], width=12)
        ], className="mb-4"),
        
        # 市场选择器
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Select Market for Detailed Information:"),
                        dcc.Dropdown(
                            id='margin-market-selector',
                            options=[
                                {'label': 'Shanghai Market', 'value': 'sh'},
                                {'label': 'Shenzhen Market', 'value': 'sz'}
                            ],
                            value='sh',
                            className='mb-3'
                        ),
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 融资买入与偿还
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-margin-components",
                    type="default",
                    children=[
                        dcc.Graph(id='margin-components-chart'),
                    ]
                )
            ], width=12, lg=6),
            
            # 月度热力图
            dbc.Col([
                dcc.Loading(
                    id="loading-margin-heatmap",
                    type="default",
                    children=[
                        dcc.Graph(id='margin-heatmap-chart'),
                    ]
                )
            ], width=12, lg=6),
        ], className="mb-4"),
        
        # 统计信息
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Margin Trading Data Statistics"),
                        html.Div(id='margin-statistics')
                    ])
                ])
            ], width=12)
        ])
        
    ], fluid=True, className="py-4")
    
    return layout


def register_margin_callbacks(app):
    """
    注册融资融券分析页面的回调函数
    
    Args:
        app: Dash应用实例
    """
    @app.callback(
        [Output('margin-trend-chart', 'figure'),
         Output('margin-change-chart', 'figure'),
         Output('margin-components-chart', 'figure'),
         Output('margin-heatmap-chart', 'figure'),
         Output('margin-statistics', 'children')],
        [Input('margin-market-selector', 'value')]
    )
    def update_margin_charts(selected_market):
        """更新融资融券图表"""
        # 加载数据
        data = load_cleaned_data()
        sh_margin = data['sh_margin']
        sz_margin = data['sz_margin']
        
        # 创建趋势图（沪深对比）
        trend_fig = create_margin_trend_chart(sh_margin, sz_margin)
        
        # 创建余额变化率图
        change_fig = create_margin_balance_change_chart(sh_margin, sz_margin)
        
        # 根据选择的市场创建详细图表
        if selected_market == 'sh':
            selected_data = sh_margin
            market_name = 'Shanghai Market'
        else:
            selected_data = sz_margin
            market_name = 'Shenzhen Market'
        
        # 创建组成部分图表
        components_fig = create_margin_components_chart(selected_data, market_name)
        
        # 创建热力图
        heatmap_fig = create_margin_heatmap(selected_data, market_name)
        
        # 计算统计信息
        latest = selected_data.iloc[-1]
        earliest = selected_data.iloc[0]
        
        stats = html.Div([
            dbc.Row([
                dbc.Col([
                    html.P(f"Market: {market_name}"),
                    html.P(f"Data Points: {len(selected_data)}"),
                    html.P(f"Date Range: {selected_data['date'].min().strftime('%Y-%m-%d')} to {selected_data['date'].max().strftime('%Y-%m-%d')}"),
                ], width=6),
                dbc.Col([
                    html.P(f"Latest Margin Balance: {latest['margin_balance']/100000000:.2f} billion yuan"),
                    html.P(f"Latest Financing Balance: {latest['financing_balance']/100000000:.2f} billion yuan"),
                    html.P(f"Period Growth: {((latest['margin_balance'] / earliest['margin_balance'] - 1) * 100):.2f}%"),
                ], width=6),
            ])
        ])
        
        return trend_fig, change_fig, components_fig, heatmap_fig, stats
