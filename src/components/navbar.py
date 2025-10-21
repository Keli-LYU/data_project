"""
导航栏组件
"""

from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    """
    创建导航栏
    
    Returns:
        dbc.Navbar: 导航栏组件
    """
    navbar = dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.I(className="fas fa-chart-line me-2")),
                    dbc.Col(dbc.NavbarBrand("中国股市数据分析平台", className="ms-2")),
                ], align="center", className="g-0"),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("首页", href="/", active="exact")),
                    dbc.NavItem(dbc.NavLink("指数分析", href="/index-analysis", active="exact")),
                    dbc.NavItem(dbc.NavLink("融资融券", href="/margin-analysis", active="exact")),
                    dbc.NavItem(dbc.NavLink("相关性分析", href="/correlation", active="exact")),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ], fluid=True),
        color="dark",
        dark=True,
        className="mb-4",
    )
    
    return navbar
