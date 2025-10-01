"""
工具函数模块
"""

import math

def format_result(result):
    """
    格式化计算结果
    
    Args:
        result (str): 计算结果字符串
        
    Returns:
        str: 格式化后的结果
    """
    try:
        # 尝试将结果转换为浮点数
        num = float(result)
        
        # 如果是整数，显示为整数形式
        if num.is_integer():
            return str(int(num))
        
        # 保留合适的小数位数
        return f"{num:.10g}"
    except:
        return result

def is_valid_number(s):
    """
    检查字符串是否为有效数字
    
    Args:
        s (str): 待检查字符串
        
    Returns:
        bool: 是否为有效数字
    """
    try:
        float(s)
        return True
    except ValueError:
        return False