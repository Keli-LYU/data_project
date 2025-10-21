"""
项目配置文件
"""

# 应用配置
APP_TITLE = "中国股市数据分析平台"
APP_HOST = "127.0.0.1"
APP_PORT = 8050
DEBUG_MODE = True

# 数据文件路径
RAW_DATA_PATH = "data/raw"
CLEANED_DATA_PATH = "data/cleaned"

# 图表配置
DEFAULT_PLOT_HEIGHT = 600
DEFAULT_PLOT_TEMPLATE = "plotly_white"

# 颜色配置
COLOR_UP = "red"  # 上涨颜色（中国习惯）
COLOR_DOWN = "green"  # 下跌颜色
COLOR_SH = "red"  # 沪市颜色
COLOR_SZ = "green"  # 深市颜色
