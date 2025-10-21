"""
相关性分析页面
"""

from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from src.utils.clean_data import load_cleaned_data
from src.components.correlation_charts import (
    create_correlation_scatter,
    create_rolling_correlation,
    create_dual_axis_chart,
    create_return_comparison,
    create_correlation_matrix
)


def create_correlation_page():
    """
    创建相关性分析页面布局
    
    Returns:
        html.Div: 页面布局
    """
    layout = dbc.Container([
        html.H2("相关性分析", className="text-center mb-4"),
        html.Hr(),
        
        # 说明文字
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H5("分析说明", className="alert-heading"),
                    html.P("本页面分析上证指数与深证成指之间的相关性，包括价格相关性、收益率相关性以及时间序列上的动态相关性。"),
                ], color="info")
            ], width=12)
        ], className="mb-4"),
        
        # 相关性矩阵
        dbc.Row([
            dbc.Col([
                html.H4("指数相关性矩阵", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-corr-matrix",
                    type="default",
                    children=[
                        dcc.Graph(id='correlation-matrix-chart'),
                    ]
                )
            ], width=12)
        ], className="mb-4"),
        
        # 散点图与双轴对比
        dbc.Row([
            dbc.Col([
                html.H4("价格散点图与趋势线", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-scatter",
                    type="default",
                    children=[
                        dcc.Graph(id='correlation-scatter-chart'),
                    ]
                )
            ], width=12, lg=6),
            
            dbc.Col([
                html.H4("双轴价格走势对比", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-dual-axis",
                    type="default",
                    children=[
                        dcc.Graph(id='dual-axis-chart'),
                    ]
                )
            ], width=12, lg=6),
        ], className="mb-4"),
        
        # 滚动相关性控制
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("滚动相关性窗口大小（交易日）:"),
                        dcc.Slider(
                            id='rolling-window-slider',
                            min=20,
                            max=250,
                            step=10,
                            value=60,
                            marks={20: '20天', 60: '60天', 120: '120天', 250: '250天'},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # 滚动相关性图
        dbc.Row([
            dbc.Col([
                html.H4("滚动相关系数", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-rolling-corr",
                    type="default",
                    children=[
                        dcc.Graph(id='rolling-correlation-chart'),
                    ]
                )
            ], width=12)
        ], className="mb-4"),
        
        # 收益率对比
        dbc.Row([
            dbc.Col([
                html.H4("日收益率对比", className="text-center mb-3"),
                dcc.Loading(
                    id="loading-return-comp",
                    type="default",
                    children=[
                        dcc.Graph(id='return-comparison-chart'),
                    ]
                )
            ], width=12)
        ], className="mb-4"),
        
        # 统计信息
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("相关性统计"),
                        html.Div(id='correlation-statistics')
                    ])
                ])
            ], width=12)
        ])
        
    ], fluid=True, className="py-4")
    
    return layout


def register_correlation_callbacks(app):
    """
    注册相关性分析页面的回调函数
    
    Args:
        app: Dash应用实例
    """
    @app.callback(
        [Output('correlation-matrix-chart', 'figure'),
         Output('correlation-scatter-chart', 'figure'),
         Output('dual-axis-chart', 'figure'),
         Output('rolling-correlation-chart', 'figure'),
         Output('return-comparison-chart', 'figure'),
         Output('correlation-statistics', 'children')],
        [Input('rolling-window-slider', 'value')]
    )
    def update_correlation_charts(window_size):
        """更新相关性图表"""
        # 加载数据
        data = load_cleaned_data()
        sh_index = data['sh_index']
        sz_index = data['sz_index']
        
        # 创建相关性矩阵
        data_dict = {
            '上证指数': sh_index,
            '深证成指': sz_index
        }
        matrix_fig = create_correlation_matrix(data_dict)
        
        # 创建散点图
        scatter_fig = create_correlation_scatter(sh_index, sz_index, '上证指数', '深证成指')
        
        # 创建双轴图
        dual_axis_fig = create_dual_axis_chart(sh_index, sz_index, '上证指数', '深证成指')
        
        # 创建滚动相关性图
        rolling_corr_fig = create_rolling_correlation(
            sh_index, sz_index, window_size, '上证指数', '深证成指'
        )
        
        # 创建收益率对比图（只显示最近1年的数据以提高可读性）
        recent_sh = sh_index.tail(250)
        recent_sz = sz_index.tail(250)
        return_comp_fig = create_return_comparison(recent_sh, recent_sz, '上证指数', '深证成指')
        
        # 计算统计信息
        # 合并数据以计算相关系数
        merged = pd.merge(
            sh_index[['date', 'close']],
            sz_index[['date', 'close']],
            on='date',
            suffixes=('_sh', '_sz')
        )
        
        # 计算皮尔逊相关系数
        import numpy as np
        price_corr = np.corrcoef(merged['close_sh'], merged['close_sz'])[0, 1]
        
        # 计算收益率相关系数
        merged_returns = pd.merge(
            sh_index[['date', 'change_pct']],
            sz_index[['date', 'change_pct']],
            on='date',
            suffixes=('_sh', '_sz')
        )
        merged_returns = merged_returns.dropna()
        return_corr = np.corrcoef(merged_returns['change_pct_sh'], merged_returns['change_pct_sz'])[0, 1]
        
        stats = html.Div([
            dbc.Row([
                dbc.Col([
                    html.P(f"数据点数: {len(merged)}"),
                    html.P(f"时间范围: {merged['date'].min().strftime('%Y-%m-%d')} 至 {merged['date'].max().strftime('%Y-%m-%d')}"),
                ], width=6),
                dbc.Col([
                    html.P(f"价格相关系数: {price_corr:.4f}"),
                    html.P(f"收益率相关系数: {return_corr:.4f}"),
                    html.P([
                        "相关性解读: ",
                        html.Span(
                            "强正相关" if price_corr > 0.7 else "正相关" if price_corr > 0.3 else "弱相关",
                            style={'color': 'green' if price_corr > 0.5 else 'orange'}
                        )
                    ]),
                ], width=6),
            ])
        ])
        
        return matrix_fig, scatter_fig, dual_axis_fig, rolling_corr_fig, return_comp_fig, stats
