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
                html.H1("China Stock Market Analysis Platform", className="text-center mb-4"),
                html.Hr(),
            ], width=12)
        ]),
        
        # 简介部分
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("Project Introduction", className="card-title"),
                        html.P([
                            "This platform provides a comprehensive analysis and visualization of major indices (Shanghai Composite, Shenzhen Component) and margin trading data of the Chinese stock market.",
                            "Through multi-dimensional data analysis, it helps users better understand market trends and correlations."
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
                        html.H4("📈 Index Analysis", className="card-title text-center"),
                        html.P([
                            "• Daily, weekly, and monthly analysis of Shanghai and Shenzhen indices",
                            html.Br(),
                            "• Candlestick charts to show market volatility",
                            html.Br(),
                            "• Moving average trend analysis",
                            html.Br(),
                            "• Comparison of Shanghai and Shenzhen indices"
                        ], className="card-text"),
                        dbc.Button("Go to Analysis", 
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
                        html.H4("💰 Margin Trading Analysis", className="card-title text-center"),
                        html.P([
                            "• Trend of margin trading balance in Shanghai and Shenzhen markets",
                            html.Br(),
                            "• Analysis of financing purchases and repayments",
                            html.Br(),
                            "• Monitoring of balance change rate",
                            html.Br(),
                            "• Monthly data heatmap"
                        ], className="card-text"),
                        dbc.Button("Go to Analysis", 
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
                        html.H4("🔗 Correlation Analysis", className="card-title text-center"),
                        html.P([
                            "• Correlation analysis of Shanghai and Shenzhen indices",
                            html.Br(),
                            "• Rolling correlation coefficient calculation",
                            html.Br(),
                            "• Comparative analysis of returns",
                            html.Br(),
                            "• Scatter plot with trend line"
                        ], className="card-text"),
                        dbc.Button("Go to Analysis", 
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
                        html.H3("Data Description", className="card-title"),
                        html.Ul([
                            html.Li("sh_index.csv - Historical data of Shanghai Composite Index"),
                            html.Li("sz_index.csv - Historical data of Shenzhen Component Index"),
                            html.Li("sh_margin_trade.csv - Margin trading data for Shanghai market"),
                            html.Li("sz_margin_trade.csv - Margin trading data for Shenzhen market"),
                        ]),
                        html.P([
                            "Data Source: ",
                            html.A("Alibaba Cloud Tianchi Open Datasets", 
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
