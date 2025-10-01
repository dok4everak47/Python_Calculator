"""
Calculator UI Components Module
"""

import kivy
kivy.require('2.0.0')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from core.calculator_core import CalculatorCore

class CalculatorWidget(BoxLayout):
    """Calculator Main Interface Module"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        
        # Initialize core calculation module
        self.core = CalculatorCore()
        
        # Create mode display
        self.mode_display = self._create_mode_display()
        self.add_widget(self.mode_display)
        
        # Create history display area
        self.history_display = self._create_history_display()
        self.add_widget(self.history_display)
        
        # Create display screen
        self.solution = self._create_display()
        self.add_widget(self.solution)
        
        # Create button layout
        buttons = self._create_buttons()
        
        # Add buttons
        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for label in row:
                if label == 'DEG/RAD':
                    # Create toggle button for angle mode
                    button = ToggleButton(text=f'DEG', font_size=20)
                    button.bind(on_press=self._toggle_angle_mode)
                    button.state = 'down' if self.core.get_angle_mode() == 'deg' else 'normal'
                else:
                    button = Button(text=label, font_size=30)
                    button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.add_widget(h_layout)
            
    def _create_mode_display(self):
        """Create mode display area"""
        mode_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        
        # Angle mode display
        self.angle_mode_label = Label(
            text=f"Angle: {self.core.get_angle_mode().upper()}",
            font_size=16,
            color=(0.5, 0.5, 0.8, 1)
        )
        
        # Memory display
        self.memory_label = Label(
            text="Memory: 0",
            font_size=16,
            color=(0.8, 0.5, 0.5, 1)
        )
        
        mode_layout.add_widget(self.angle_mode_label)
        mode_layout.add_widget(self.memory_label)
        
        return mode_layout
    
    def _create_display(self):
        """
        Create display screen
        
        Returns:
            TextInput: Display screen component
        """
        return TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
    
    def _create_history_display(self):
        """
        Create history display area
        
        Returns:
            ScrollView: Scroll view containing history records
        """
        # Create history label with clear button
        history_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        
        history_label = Label(
            text="History", 
            font_size=20,
            color=(0.7, 0.7, 0.7, 1)
        )
        
        # Create clear history button
        clear_button = Button(
            text="Clear", 
            size_hint_x=None,
            width=80,
            font_size=14,
            background_color=(0.8, 0.3, 0.3, 1)
        )
        clear_button.bind(on_press=self._clear_history)
        
        history_header.add_widget(history_label)
        history_header.add_widget(clear_button)
        
        # Create history display area
        self.history_text = TextInput(
            multiline=True, 
            readonly=True, 
            font_size=16,
            size_hint_y=None,
            height=100
        )
        self.history_text.text = "No history records"
        
        # Create scroll view
        self.scroll_view = ScrollView(size_hint_y=None, height=130)
        
        # Create vertical layout
        history_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=130)
        history_layout.add_widget(history_header)
        history_layout.add_widget(self.history_text)
        
        self.scroll_view.add_widget(history_layout)
        return self.scroll_view
    
    def _create_buttons(self):
        """
        Create button layout with scientific functions
        
        Returns:
            list: Button layout list
        """
        return [
            ['C', '+/-', '%', '/', 'sin', 'cos'],
            ['7', '8', '9', '*', 'tan', 'cot'],
            ['4', '5', '6', '-', 'asin', 'acos'],
            ['1', '2', '3', '+', 'atan', 'log'],
            ['0', '.', '=', 'π', 'ln', 'e'],
            ['x²', 'x³', 'xⁿ', '√', '³√', '!'],
            ['(', ')', '|x|', 'MR', 'M+', 'M-'],
            ['MC', 'MS', 'DEG/RAD', 'DEL', 'CE', 'ANS']
        ]
            
    def on_button_press(self, instance):
        """
        Handle button click events
        
        Args:
            instance: Button instance
        """
        current = self.solution.text
        button_text = instance.text
        
        if button_text == 'C':
            # Clear screen
            self.solution.text = ""
        elif button_text == 'CE':
            # Clear entry (clear current input)
            self.solution.text = ""
        elif button_text == 'DEL':
            # Backspace
            self.solution.text = current[:-1]
        elif button_text == '=':
            # Calculate result and display
            result = self.core.evaluate_expression(current)
            self.solution.text = result
            
            # Update history display
            self._update_history_display()
        elif button_text == 'ANS':
            # Insert last answer
            if self.core.last_result:
                self.solution.text = current + self.core.last_result
        elif button_text == 'MR':
            # Memory recall
            memory_value = self.core.memory_recall()
            self.solution.text = current + memory_value
        elif button_text == 'MS':
            # Memory store
            if current:
                self.core.memory_store(current)
                self._update_memory_display()
        elif button_text == 'M+':
            # Memory add
            if current:
                self.core.memory_add(current)
                self._update_memory_display()
        elif button_text == 'M-':
            # Memory subtract
            if current:
                self.core.memory_subtract(current)
                self._update_memory_display()
        elif button_text == 'MC':
            # Memory clear
            self.core.memory_clear()
            self._update_memory_display()
        else:
            # Add button text to current expression
            if self.core.validate_input(current, button_text):
                # Handle special cases for functions that need parentheses
                if button_text in ['sin', 'cos', 'tan', 'cot', 'asin', 'acos', 'atan', 'log', 'ln', '√', '³√']:
                    self.solution.text = current + button_text + '('
                elif button_text == '|x|':
                    self.solution.text = current + '|'
                elif button_text == 'xⁿ':
                    self.solution.text = current + '^'
                else:
                    self.solution.text = current + button_text
    
    def _toggle_angle_mode(self, instance):
        """Toggle between degree and radian mode"""
        current_mode = self.core.get_angle_mode()
        new_mode = 'rad' if current_mode == 'deg' else 'deg'
        self.core.set_angle_mode(new_mode)
        instance.text = new_mode.upper()
        self.angle_mode_label.text = f"Angle: {new_mode.upper()}"
    
    def _update_memory_display(self):
        """Update memory display"""
        self.memory_label.text = f"Memory: {self.core.memory}"
    
    def _update_history_display(self):
        """Update history display"""
        history = self.core.get_history()
        if history:
            # Reverse history records, newest on top
            reversed_history = history[::-1]
            history_text = "\n".join(reversed_history)
            self.history_text.text = history_text
            
            # Auto-scroll to the top (newest record)
            self.history_text.cursor = (0, 0)
        else:
            self.history_text.text = "No history records"
    
    def _clear_history(self, instance):
        """Clear history records"""
        self.core.clear_history()
        self.history_text.text = "No history records"