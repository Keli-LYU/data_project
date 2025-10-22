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
                    dbc.Col(dbc.NavbarBrand("China Stock Market Analysis", className="ms-2")),
                ], align="center", className="g-0"),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                    dbc.NavItem(dbc.NavLink("Index Analysis", href="/index-analysis", active="exact")),
                    dbc.NavItem(dbc.NavLink("Margin Trading", href="/margin-analysis", active="exact")),
                    dbc.NavItem(dbc.NavLink("Correlation Analysis", href="/correlation", active="exact")),
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
