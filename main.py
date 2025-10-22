"""
中国股市数据分析平台 - 主程序
使用 Dash 框架构建的交互式数据分析平台

运行方式:
    python main.py
"""

import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from config import APP_TITLE, APP_HOST, APP_PORT, DEBUG_MODE
from src.components.navbar import create_navbar
from src.pages.home import create_home_page
from src.pages.index_analysis import create_index_analysis_page, register_index_callbacks
from src.pages.margin_analysis import create_margin_analysis_page, register_margin_callbacks
from src.pages.correlation import create_correlation_page, register_correlation_callbacks
from src.utils.clean_data import process_and_save_all_data


def create_app():
    """
    创建并配置 Dash 应用
    
    Returns:
        Dash: 配置好的 Dash 应用实例
    """
    # 初始化 Dash 应用，使用 Bootstrap 主题
    app = Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
        ],
        suppress_callback_exceptions=True,
        title=APP_TITLE,
        update_title="Loading..."
    )
    
    # 创建应用布局
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        
        # 导航栏
        create_navbar(),
        
        # 页面内容
        html.Div(id='page-content')
    ])
    
    # 注册页面路由回调
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        """
        根据 URL 路径显示对应页面
        
        Args:
            pathname (str): URL 路径
            
        Returns:
            html.Div: 页面内容
        """
        if pathname == '/index-analysis':
            return create_index_analysis_page()
        elif pathname == '/margin-analysis':
            return create_margin_analysis_page()
        elif pathname == '/correlation':
            return create_correlation_page()
        else:  # 默认首页
            return create_home_page()
    
    # 注册各页面的回调函数
    register_index_callbacks(app)
    register_margin_callbacks(app)
    register_correlation_callbacks(app)
    
    return app

app = create_app()
server = app.server

def main():
    """
    主函数：初始化数据并启动应用
    """
    print("=" * 60)
    print(f"  {APP_TITLE}")
    print("=" * 60)
    
    # 检查并处理数据
    print("\nChecking data files...")
    try:
        # 处理并保存清洗后的数据
        print("Processing data...")
        process_and_save_all_data()
        print("Data processing complete.")
    except Exception as e:
        print(f"Data processing failed: {e}")
        print("\nPlease ensure the following data files exist in the data/raw directory:")
        print("  - sh_index.csv")
        print("  - sz_index.csv")
        print("  - sh_margin_trade.csv")
        print("  - sz_margin_trade.csv")
        sys.exit(1)
    
    # 创建应用
    print("\nStarting application...")
    
    # 运行服务器
    print(f"\nApplication started successfully!")
    print(f"\nAccess at: http://{APP_HOST}:{APP_PORT}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(
        host=APP_HOST,
        port=APP_PORT,
        debug=DEBUG_MODE
    )


if __name__ == '__main__':
    main()
