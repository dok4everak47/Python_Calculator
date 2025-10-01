"""
计算器核心计算逻辑模块
"""

class CalculatorCore:
    """计算器核心计算逻辑类"""
    
    @staticmethod
    def evaluate_expression(expression):
        """
        计算数学表达式
        
        Args:
            expression (str): 数学表达式字符串
            
        Returns:
            str: 计算结果或错误信息
        """
        try:
            # 将 × 和 ÷ 替换为 * 和 /
            expression = expression.replace('×', '*').replace('÷', '/')
            if expression:
                # 使用 eval 计算表达式（注意：在生产环境中应使用更安全的解析器）
                result = str(eval(expression))
                return result
        except Exception as e:
            return "Error"
    
    @staticmethod
    def validate_input(current_text, new_char):
        """
        验证输入字符
        
        Args:
            current_text (str): 当前显示文本
            new_char (str): 新输入字符
            
        Returns:
            bool: 是否允许输入
        """
        if not current_text:
            return True
            
        # 避免连续的操作符
        if (current_text[-1] in ['+', '-', '*', '/', '.'] and 
            new_char in ['+', '-', '*', '/', '.']):
            return False
        return True