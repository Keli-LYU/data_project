"""
指数分析页面
"""

from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from src.utils.clean_data import load_cleaned_data, resample_to_weekly, resample_to_monthly
from src.components.index_charts import (
    create_candlestick_chart, 
    create_line_chart, 
    create_comparison_chart
)


def create_index_analysis_page():
    """
    创建指数分析页面布局
    
    Returns:
        html.Div: 页面布局
    """
    layout = dbc.Container([
        html.H2("指数分析", className="text-center mb-4"),
        html.Hr(),
        
        # 控制面板
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("选择分析参数"),
                        
                        # 市场选择
                        html.Label("选择市场:"),
                        dcc.Dropdown(
                            id='market-selector',
                            options=[
                                {'label': '上证指数', 'value': 'sh'},
                                {'label': '深证成指', 'value': 'sz'},
                                {'label': '沪深对比', 'value': 'both'}
                            ],
                            value='sh',
                            className='mb-3'
                        ),
                        
                        # 周期选择
                        html.Label("选择时间周期:"),
                        dcc.Dropdown(
                            id='period-selector',
                            options=[
                                {'label': '日线', 'value': 'daily'},
                                {'label': '周线', 'value': 'weekly'},
                                {'label': '月线', 'value': 'monthly'}
                            ],
                            value='daily',
                            className='mb-3'
                        ),
                        
                        # 日期范围选择
                        html.Label("选择日期范围:"),
                        dcc.DatePickerRange(
                            id='date-range',
                            display_format='YYYY-MM-DD',
                            className='mb-3'
                        ),
                    ])
                ])
            ], width=12, lg=3),
            
            # 图表显示区域
            dbc.Col([
                dcc.Loading(
                    id="loading-index",
                    type="default",
                    children=[
                        dcc.Graph(id='index-main-chart'),
                    ]
                )
            ], width=12, lg=9),
        ], className="mb-4"),
        
        # 对比图表
        dbc.Row([
            dbc.Col([
                html.H4("沪深指数对比", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-comparison",
                    type="default",
                    children=[
                        dcc.Graph(id='index-comparison-chart'),
                    ]
                )
            ], width=12)
        ], className="mb-4"),
        
        # 统计信息
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("统计信息"),
                        html.Div(id='index-statistics')
                    ])
                ])
            ], width=12)
        ])
        
    ], fluid=True, className="py-4")
    
    return layout


def register_index_callbacks(app):
    """
    注册指数分析页面的回调函数
    
    Args:
        app: Dash应用实例
    """
    @app.callback(
        [Output('index-main-chart', 'figure'),
         Output('index-comparison-chart', 'figure'),
         Output('index-statistics', 'children'),
         Output('date-range', 'start_date'),
         Output('date-range', 'end_date'),
         Output('date-range', 'min_date_allowed'),
         Output('date-range', 'max_date_allowed')],
        [Input('market-selector', 'value'),
         Input('period-selector', 'value'),
         Input('date-range', 'start_date'),
         Input('date-range', 'end_date')]
    )
    def update_index_charts(market, period, start_date, end_date):
        """更新指数图表"""
        # 加载数据
        data = load_cleaned_data()
        sh_data = data['sh_index']
        sz_data = data['sz_index']
        
        # 根据周期重采样
        if period == 'weekly':
            sh_data = resample_to_weekly(sh_data)
            sz_data = resample_to_weekly(sz_data)
        elif period == 'monthly':
            sh_data = resample_to_monthly(sh_data)
            sz_data = resample_to_monthly(sz_data)
        
        # 设置日期范围
        min_date = min(sh_data['date'].min(), sz_data['date'].min())
        max_date = max(sh_data['date'].max(), sz_data['date'].max())
        
        if start_date is None:
            start_date = max_date - pd.Timedelta(days=365)
        if end_date is None:
            end_date = max_date
        
        # 过滤日期范围
        sh_filtered = sh_data[(sh_data['date'] >= start_date) & (sh_data['date'] <= end_date)]
        sz_filtered = sz_data[(sz_data['date'] >= start_date) & (sz_data['date'] <= end_date)]
        
        # 创建主图表
        period_name = {'daily': '日线', 'weekly': '周线', 'monthly': '月线'}[period]
        
        if market == 'sh':
            main_fig = create_candlestick_chart(sh_filtered, "上证指数", period_name)
            selected_data = sh_filtered
            market_name = "上证指数"
        elif market == 'sz':
            main_fig = create_candlestick_chart(sz_filtered, "深证成指", period_name)
            selected_data = sz_filtered
            market_name = "深证成指"
        else:  # both
            main_fig = create_line_chart(sh_filtered, f"上证指数 - {period_name}")
            selected_data = sh_filtered
            market_name = "沪深指数"
        
        # 创建对比图表
        comparison_fig = create_comparison_chart(sh_filtered, sz_filtered)
        
        # 计算统计信息
        if len(selected_data) > 0:
            stats = html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P(f"市场: {market_name}"),
                        html.P(f"数据点数: {len(selected_data)}"),
                    ], width=6),
                    dbc.Col([
                        html.P(f"最新收盘: {selected_data['close'].iloc[-1]:.2f}"),
                        html.P(f"期间涨跌幅: {((selected_data['close'].iloc[-1] / selected_data['close'].iloc[0] - 1) * 100):.2f}%"),
                    ], width=6),
                ])
            ])
        else:
            stats = html.P("无数据")
        
        return main_fig, comparison_fig, stats, start_date, end_date, min_date, max_date
