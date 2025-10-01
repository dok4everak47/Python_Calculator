"""
Calculator Core Calculation Logic Module
"""

import datetime

class CalculatorCore:
    """Calculator Core Calculation Logic Class"""
    
    def __init__(self):
        """Initialize calculator core"""
        self.history = []  # History records list with timestamps
        self.history_counter = 1  # Counter for numbering history records
    
    def evaluate_expression(self, expression):
        """
        Calculate mathematical expression and record history
        
        Args:
            expression (str): Mathematical expression string
            
        Returns:
            str: Calculation result or error message
        """
        try:
            # Replace × and ÷ with * and /
            expression = expression.replace('×', '*').replace('÷', '/')
            if expression:
                # Use eval to calculate expression (Note: Use safer parser in production)
                result = str(eval(expression))
                
                # Get current time with seconds precision
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Record history with timestamp and numbering
                history_entry = {
                    'number': self.history_counter,
                    'time': current_time,
                    'expression': expression,
                    'result': result
                }
                self.history.append(history_entry)
                self.history_counter += 1
                
                # Limit history records (keep last 10)
                if len(self.history) > 10:
                    self.history = self.history[-10:]
                
                return result
        except Exception as e:
            return "Error"
    
    def get_history(self):
        """
        Get history records
        
        Returns:
            list: History records list with formatted display text
        """
        formatted_history = []
        for entry in self.history:
            # Format: [1] 2024-01-01 12:30:45: 2+2 = 4
            formatted_entry = f"[{entry['number']}] {entry['time']}: {entry['expression']} = {entry['result']}"
            formatted_history.append(formatted_entry)
        return formatted_history
    
    def clear_history(self):
        """Clear history records"""
        self.history = []
        self.history_counter = 1  # Reset counter when clearing history
    
    @staticmethod
    def validate_input(current_text, new_char):
        """
        Validate input character
        
        Args:
            current_text (str): Current display text
            new_char (str): New input character
            
        Returns:
            bool: Whether input is allowed
        """
        if not current_text:
            return True
            
        # Avoid consecutive operators
        if (current_text[-1] in ['+', '-', '*', '/', '.'] and 
            new_char in ['+', '-', '*', '/', '.']):
            return False
        return True