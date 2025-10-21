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
        html.H2("融资融券分析", className="text-center mb-4"),
        html.Hr(),
        
        # 沪深两市融资融券余额趋势
        dbc.Row([
            dbc.Col([
                html.H4("沪深两市融资融券余额趋势", className="text-center mb-3"),
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
                html.H4("融资融券余额变化率", className="text-center mb-3"),
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
                        html.Label("选择市场查看详细信息:"),
                        dcc.Dropdown(
                            id='margin-market-selector',
                            options=[
                                {'label': '沪市', 'value': 'sh'},
                                {'label': '深市', 'value': 'sz'}
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
                        html.H5("融资融券数据统计"),
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
            market_name = '沪市'
        else:
            selected_data = sz_margin
            market_name = '深市'
        
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
                    html.P(f"市场: {market_name}"),
                    html.P(f"数据点数: {len(selected_data)}"),
                    html.P(f"数据时间范围: {selected_data['date'].min().strftime('%Y-%m-%d')} 至 {selected_data['date'].max().strftime('%Y-%m-%d')}"),
                ], width=6),
                dbc.Col([
                    html.P(f"最新融资融券余额: {latest['margin_balance']/100000000:.2f} 亿元"),
                    html.P(f"最新融资余额: {latest['financing_balance']/100000000:.2f} 亿元"),
                    html.P(f"期间增长: {((latest['margin_balance'] / earliest['margin_balance'] - 1) * 100):.2f}%"),
                ], width=6),
            ])
        ])
        
        return trend_fig, change_fig, components_fig, heatmap_fig, stats
