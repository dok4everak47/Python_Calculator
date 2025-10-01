"""
SciCalc Pro - 科学计算器
模块化主程序入口
"""

from kivy.app import App
from ui.calculator_ui import CalculatorWidget

class CalculatorApp(App):
    def build(self):
        return CalculatorWidget()

if __name__ == "__main__":
    app = CalculatorApp()
    app.run()