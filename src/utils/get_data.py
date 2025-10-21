"""
数据获取模块
从data/raw目录加载原始数据

数据来源：阿里云天池公开数据集
数据集链接：https://tianchi.aliyun.com/
"""

import pandas as pd
import os


def get_raw_data_path():
    """
    获取原始数据目录路径
    
    Returns:
        str: 原始数据目录的绝对路径
    """
    # 获取项目根目录（main.py所在目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    return os.path.join(project_root, 'data', 'raw')


def load_sh_index():
    """
    加载沪市指数数据
    
    Returns:
        pd.DataFrame: 沪市指数数据
    """
    raw_data_path = get_raw_data_path()
    file_path = os.path.join(raw_data_path, 'sh_index.csv')
    
    # 读取CSV文件
    df = pd.read_csv(file_path, encoding='gb2312')
    return df


def load_sz_index():
    """
    加载深证成指数据
    
    Returns:
        pd.DataFrame: 深证成指数据
    """
    raw_data_path = get_raw_data_path()
    file_path = os.path.join(raw_data_path, 'sz_index.csv')
    
    # 读取CSV文件
    df = pd.read_csv(file_path, encoding='gb2312')
    return df


def load_sh_margin_trade():
    """
    加载沪市两融数据
    
    Returns:
        pd.DataFrame: 沪市两融数据
    """
    raw_data_path = get_raw_data_path()
    file_path = os.path.join(raw_data_path, 'sh_margin_trade.csv')
    
    # 读取CSV文件
    df = pd.read_csv(file_path, encoding='utf-8')
    return df


def load_sz_margin_trade():
    """
    加载深市两融数据
    
    Returns:
        pd.DataFrame: 深市两融数据
    """
    raw_data_path = get_raw_data_path()
    file_path = os.path.join(raw_data_path, 'sz_margin_trade.csv')
    
    # 读取CSV文件
    df = pd.read_csv(file_path, encoding='utf-8')
    return df


def load_all_data():
    """
    加载所有数据
    
    Returns:
        dict: 包含所有数据的字典
    """
    return {
        'sh_index': load_sh_index(),
        'sz_index': load_sz_index(),
        'sh_margin': load_sh_margin_trade(),
        'sz_margin': load_sz_margin_trade()
    }
