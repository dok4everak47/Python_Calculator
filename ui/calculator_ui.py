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
                button = Button(text=label, font_size=40)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.add_widget(h_layout)
            
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
        Create button layout
        
        Returns:
            list: Button layout list
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
        Handle button click events
        
        Args:
            instance: Button instance
        """
        current = self.solution.text
        button_text = instance.text
        
        if button_text == 'C':
            # Clear screen
            self.solution.text = ""
        elif button_text == '=':
            # Calculate result and display
            result = self.core.evaluate_expression(current)
            self.solution.text = result
            
            # Update history display
            self._update_history_display()
        else:
            # Add button text to current expression
            if self.core.validate_input(current, button_text):
                self.solution.text = current + button_text
    
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