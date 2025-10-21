"""
数据清洗和处理模块
对原始数据进行清洗、转换和特征工程
"""

import pandas as pd
import numpy as np
import os
from .get_data import load_all_data


def clean_index_data(df, market_name='沪市'):
    """
    清洗指数数据
    
    Args:
        df (pd.DataFrame): 原始指数数据
        market_name (str): 市场名称
        
    Returns:
        pd.DataFrame: 清洗后的数据
    """
    # 复制数据避免修改原始数据
    df_clean = df.copy()
    
    # 将日期列转换为日期类型
    df_clean['date'] = pd.to_datetime(df_clean['date'], format='%Y%m%d')
    
    # 按日期排序
    df_clean = df_clean.sort_values('date', ascending=True)
    
    # 重置索引
    df_clean = df_clean.reset_index(drop=True)
    
    # 添加市场标识
    df_clean['market'] = market_name
    
    # 计算涨跌幅
    df_clean['change_pct'] = df_clean['close'].pct_change() * 100
    
    # 计算移动平均线
    df_clean['ma5'] = df_clean['close'].rolling(window=5).mean()
    df_clean['ma10'] = df_clean['close'].rolling(window=10).mean()
    df_clean['ma20'] = df_clean['close'].rolling(window=20).mean()
    df_clean['ma60'] = df_clean['close'].rolling(window=60).mean()
    
    return df_clean


def resample_to_weekly(df):
    """
    将日线数据重采样为周线数据
    
    Args:
        df (pd.DataFrame): 日线数据
        
    Returns:
        pd.DataFrame: 周线数据
    """
    df_weekly = df.copy()
    df_weekly = df_weekly.set_index('date')
    
    # 重采样规则：开盘价取第一个，收盘价取最后一个，最高价取最大值，最低价取最小值，成交量求和
    df_weekly = df_weekly.resample('W').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'vol': 'sum',
        'amount': 'sum'
    })
    
    df_weekly = df_weekly.reset_index()
    df_weekly = df_weekly.dropna()
    
    # 计算周涨跌幅
    df_weekly['change_pct'] = df_weekly['close'].pct_change() * 100
    
    return df_weekly


def resample_to_monthly(df):
    """
    将日线数据重采样为月线数据
    
    Args:
        df (pd.DataFrame): 日线数据
        
    Returns:
        pd.DataFrame: 月线数据
    """
    df_monthly = df.copy()
    df_monthly = df_monthly.set_index('date')
    
    # 重采样规则：开盘价取第一个，收盘价取最后一个，最高价取最大值，最低价取最小值，成交量求和
    df_monthly = df_monthly.resample('M').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'vol': 'sum',
        'amount': 'sum'
    })
    
    df_monthly = df_monthly.reset_index()
    df_monthly = df_monthly.dropna()
    
    # 计算月涨跌幅
    df_monthly['change_pct'] = df_monthly['close'].pct_change() * 100
    
    return df_monthly


def clean_margin_data(df, market_name='沪市'):
    """
    清洗融资融券数据
    
    Args:
        df (pd.DataFrame): 原始融资融券数据
        market_name (str): 市场名称
        
    Returns:
        pd.DataFrame: 清洗后的数据
    """
    # 复制数据避免修改原始数据
    df_clean = df.copy()
    
    # 将日期列转换为日期类型
    df_clean['date'] = pd.to_datetime(df_clean['date'], format='%Y%m%d')
    
    # 按日期排序
    df_clean = df_clean.sort_values('date', ascending=True)
    
    # 重置索引
    df_clean = df_clean.reset_index(drop=True)
    
    # 添加市场标识
    df_clean['market'] = market_name
    
    # 填充缺失值
    df_clean = df_clean.fillna(0)
    
    # 计算融资融券余额的变化率
    df_clean['margin_balance_change'] = df_clean['margin_balance'].pct_change() * 100
    
    return df_clean


def process_and_save_all_data():
    """
    处理所有数据并保存到cleaned目录
    
    Returns:
        dict: 包含所有清洗后数据的字典
    """
    # 加载所有原始数据
    raw_data = load_all_data()
    
    # 清洗指数数据
    sh_index_clean = clean_index_data(raw_data['sh_index'], '沪市')
    sz_index_clean = clean_index_data(raw_data['sz_index'], '深市')
    
    # 清洗融资融券数据
    sh_margin_clean = clean_margin_data(raw_data['sh_margin'], '沪市')
    sz_margin_clean = clean_margin_data(raw_data['sz_margin'], '深市')
    
    # 获取cleaned数据目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    cleaned_path = os.path.join(project_root, 'data', 'cleaned')
    
    # 确保目录存在
    os.makedirs(cleaned_path, exist_ok=True)
    
    # 保存清洗后的数据
    sh_index_clean.to_csv(os.path.join(cleaned_path, 'sh_index_clean.csv'), 
                          index=False, encoding='utf-8')
    sz_index_clean.to_csv(os.path.join(cleaned_path, 'sz_index_clean.csv'), 
                          index=False, encoding='utf-8')
    sh_margin_clean.to_csv(os.path.join(cleaned_path, 'sh_margin_clean.csv'), 
                           index=False, encoding='utf-8')
    sz_margin_clean.to_csv(os.path.join(cleaned_path, 'sz_margin_clean.csv'), 
                           index=False, encoding='utf-8')
    
    return {
        'sh_index': sh_index_clean,
        'sz_index': sz_index_clean,
        'sh_margin': sh_margin_clean,
        'sz_margin': sz_margin_clean
    }


def load_cleaned_data():
    """
    从cleaned目录加载已清洗的数据
    
    Returns:
        dict: 包含所有清洗后数据的字典
    """
    # 获取cleaned数据目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    cleaned_path = os.path.join(project_root, 'data', 'cleaned')
    
    # 检查文件是否存在，如果不存在则处理并保存
    if not os.path.exists(os.path.join(cleaned_path, 'sh_index_clean.csv')):
        return process_and_save_all_data()
    
    # 加载清洗后的数据
    sh_index = pd.read_csv(os.path.join(cleaned_path, 'sh_index_clean.csv'))
    sz_index = pd.read_csv(os.path.join(cleaned_path, 'sz_index_clean.csv'))
    sh_margin = pd.read_csv(os.path.join(cleaned_path, 'sh_margin_clean.csv'))
    sz_margin = pd.read_csv(os.path.join(cleaned_path, 'sz_margin_clean.csv'))
    
    # 转换日期列
    sh_index['date'] = pd.to_datetime(sh_index['date'])
    sz_index['date'] = pd.to_datetime(sz_index['date'])
    sh_margin['date'] = pd.to_datetime(sh_margin['date'])
    sz_margin['date'] = pd.to_datetime(sz_margin['date'])
    
    return {
        'sh_index': sh_index,
        'sz_index': sz_index,
        'sh_margin': sh_margin,
        'sz_margin': sz_margin
    }
