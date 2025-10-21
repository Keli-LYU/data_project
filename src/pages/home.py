"""
首页
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_home_page():
    """
    创建首页布局
    
    Returns:
        html.Div: 首页布局
    """
    layout = dbc.Container([
        # 标题部分
        dbc.Row([
            dbc.Col([
                html.H1("中国股市数据分析平台", className="text-center mb-4"),
                html.Hr(),
            ], width=12)
        ]),
        
        # 简介部分
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("项目简介", className="card-title"),
                        html.P([
                            "本平台对中国股市的主要指数（上证指数、深证成指）以及融资融券数据进行全面分析和可视化展示。",
                            "通过多维度的数据分析，帮助用户更好地理解市场趋势和相关性。"
                        ], className="card-text"),
                    ])
                ], className="mb-4")
            ], width=12)
        ]),
        
        # 功能模块卡片
        dbc.Row([
            # 指数分析
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src="/assets/index_icon.png", top=True, 
                               style={"height": "200px", "object-fit": "cover"},
                               className="d-none"),  # 如果没有图片就隐藏
                    dbc.CardBody([
                        html.H4("📈 指数分析", className="card-title text-center"),
                        html.P([
                            "• 上证指数与深证成指的日线、周线、月线分析",
                            html.Br(),
                            "• K线图展示市场波动",
                            html.Br(),
                            "• 移动平均线趋势分析",
                            html.Br(),
                            "• 沪深指数对比"
                        ], className="card-text"),
                        dbc.Button("进入分析", 
                                  href="/index-analysis", 
                                  color="primary", 
                                  className="w-100 mt-2")
                    ])
                ], className="h-100 shadow-sm hover-shadow")
            ], width=12, lg=4, className="mb-4"),
            
            # 融资融券分析
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("💰 融资融券分析", className="card-title text-center"),
                        html.P([
                            "• 沪深两市融资融券余额趋势",
                            html.Br(),
                            "• 融资买入与偿还分析",
                            html.Br(),
                            "• 余额变化率监控",
                            html.Br(),
                            "• 月度数据热力图"
                        ], className="card-text"),
                        dbc.Button("进入分析", 
                                  href="/margin-analysis", 
                                  color="success", 
                                  className="w-100 mt-2")
                    ])
                ], className="h-100 shadow-sm hover-shadow")
            ], width=12, lg=4, className="mb-4"),
            
            # 相关性分析
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🔗 相关性分析", className="card-title text-center"),
                        html.P([
                            "• 沪深指数相关性分析",
                            html.Br(),
                            "• 滚动相关系数计算",
                            html.Br(),
                            "• 收益率对比分析",
                            html.Br(),
                            "• 散点图与趋势线"
                        ], className="card-text"),
                        dbc.Button("进入分析", 
                                  href="/correlation", 
                                  color="info", 
                                  className="w-100 mt-2")
                    ])
                ], className="h-100 shadow-sm hover-shadow")
            ], width=12, lg=4, className="mb-4"),
        ], className="mb-4"),
        
        # 数据说明部分
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("数据说明", className="card-title"),
                        html.Ul([
                            html.Li("sh_index.csv - 沪市指数（上证指数）历史数据"),
                            html.Li("sz_index.csv - 深证成指历史数据"),
                            html.Li("sh_margin_trade.csv - 沪市融资融券数据"),
                            html.Li("sz_margin_trade.csv - 深市融资融券数据"),
                        ]),
                        html.P([
                            "数据来源：",
                            html.A("阿里云天池公开数据集", 
                                  href="https://tianchi.aliyun.com/", 
                                  target="_blank",
                                  style={"color": "#1890ff"})
                        ], className="text-muted mt-2"),
                    ])
                ])
            ], width=12)
        ]),
        
    ], fluid=True, className="py-4")
    
    return layout
