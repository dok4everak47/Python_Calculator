import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class CalculatorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        
        # 创建显示屏幕
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        self.add_widget(self.solution)
        
        # 创建按钮布局
        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '=']
        ]
        
        # 添加按钮
        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for label in row:
                button = Button(text=label, font_size=40)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.add_widget(h_layout)
            
        # 特殊处理等于号占据两行
        # 获取最后一个按钮（等于号）
        equal_button = h_layout.children[0]
        equal_button.height = 200  # 调整高度
        
    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        
        if button_text == 'C':
            # 清除屏幕
            self.solution.text = ""
        elif button_text == '=':
            try:
                # 计算结果并显示
                # 将 × 和 ÷ 替换为 * 和 /
                expression = current.replace('×', '*').replace('÷', '/')
                if expression:
                    result = str(eval(expression))
                    self.solution.text = result
            except Exception:
                self.solution.text = "Error"
        else:
            # 添加按钮文本到当前表达式
            if current and (current[-1] in ['+', '-', '*', '/', '.'] and 
                           button_text in ['+', '-', '*', '/', '.']):
                # 避免连续的操作符
                return
            self.solution.text = current + button_text


class CalculatorApp(App):
    def build(self):
        return CalculatorWidget()


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()