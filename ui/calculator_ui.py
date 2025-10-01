"""
计算器UI组件模块
"""

import kivy
kivy.require('2.0.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from core.calculator_core import CalculatorCore

class CalculatorWidget(BoxLayout):
    """计算器主界面模块"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        
        # 初始化核心计算模块
        self.core = CalculatorCore()
        
        # 创建显示屏幕
        self.solution = self._create_display()
        self.add_widget(self.solution)
        
        # 创建按钮布局
        buttons = self._create_buttons()
        
        # 添加按钮
        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for label in row:
                button = Button(text=label, font_size=40)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.add_widget(h_layout)
            
    def _create_display(self):
        """
        创建显示屏幕
        
        Returns:
            TextInput: 显示屏组件
        """
        return TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
    
    def _create_buttons(self):
        """
        创建按钮布局
        
        Returns:
            list: 按钮布局列表
        """
        return [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '=']
        ]
            
    def on_button_press(self, instance):
        """
        处理按钮点击事件
        
        Args:
            instance: 按钮实例
        """
        current = self.solution.text
        button_text = instance.text
        
        if button_text == 'C':
            # 清除屏幕
            self.solution.text = ""
        elif button_text == '=':
            # 计算结果并显示
            result = self.core.evaluate_expression(current)
            self.solution.text = result
        else:
            # 添加按钮文本到当前表达式
            if self.core.validate_input(current, button_text):
                self.solution.text = current + button_text