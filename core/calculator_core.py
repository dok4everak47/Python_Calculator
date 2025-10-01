"""
Calculator Core Calculation Logic Module
"""

import datetime
import math

class CalculatorCore:
    """Calculator Core Calculation Logic Class"""
    
    def __init__(self):
        """Initialize calculator core"""
        self.history = []  # History records list with timestamps
        self.history_counter = 1  # Counter for numbering history records
        self.angle_mode = 'deg'  # Default angle mode: 'deg' or 'rad'
        self.memory = 0  # Memory value
        self.last_result = None  # Last calculation result
    
    def set_angle_mode(self, mode):
        """Set angle mode (deg or rad)"""
        if mode in ['deg', 'rad']:
            self.angle_mode = mode
            return True
        return False
    
    def get_angle_mode(self):
        """Get current angle mode"""
        return self.angle_mode
    
    def memory_store(self, value):
        """Store value in memory"""
        try:
            self.memory = float(value)
            return True
        except:
            return False
    
    def memory_recall(self):
        """Recall value from memory"""
        return str(self.memory)
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
    
    def memory_add(self, value):
        """Add value to memory"""
        try:
            self.memory += float(value)
            return True
        except:
            return False
    
    def memory_subtract(self, value):
        """Subtract value from memory"""
        try:
            self.memory -= float(value)
            return True
        except:
            return False
    
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
            
            # Handle scientific functions
            expression = self._preprocess_scientific_functions(expression)
            
            if expression:
                # Use eval to calculate expression (Note: Use safer parser in production)
                result = str(eval(expression))
                self.last_result = result
                
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
    
    def _preprocess_scientific_functions(self, expression):
        """Preprocess scientific functions in expression"""
        import re
        
        # Handle trigonometric functions with angle mode conversion
        trig_functions = ['sin', 'cos', 'tan', 'cot']
        for func in trig_functions:
            pattern = rf'{func}\(([^)]+)\)'
            matches = re.findall(pattern, expression)
            for match in matches:
                if self.angle_mode == 'deg':
                    # Convert degrees to radians
                    replacement = f'math.{func}(math.radians({match}))'
                else:
                    replacement = f'math.{func}({match})'
                expression = expression.replace(f'{func}({match})', replacement)
        
        # Handle inverse trigonometric functions with angle mode conversion
        inv_trig_functions = ['asin', 'acos', 'atan']
        for func in inv_trig_functions:
            pattern = rf'{func}\(([^)]+)\)'
            matches = re.findall(pattern, expression)
            for match in matches:
                if self.angle_mode == 'deg':
                    # Convert radians to degrees
                    replacement = f'math.degrees(math.{func}({match}))'
                else:
                    replacement = f'math.{func}({match})'
                expression = expression.replace(f'{func}({match})', replacement)
        
        # Handle other scientific functions
        expression = expression.replace('log(', 'math.log10(')
        expression = expression.replace('ln(', 'math.log(')
        expression = expression.replace('π', 'math.pi')
        expression = expression.replace('e', 'math.e')
        expression = expression.replace('√(', 'math.sqrt(')
        expression = expression.replace('³√(', 'math.cbrt(') if hasattr(math, 'cbrt') else expression.replace('³√(', '**(1/3)')
        expression = expression.replace('!', 'math.factorial(') + ')' if '!' in expression else expression
        expression = expression.replace('|', 'abs(') + ')' if '|' in expression else expression
        
        # Handle power functions
        expression = expression.replace('x²', '**2')
        expression = expression.replace('x³', '**3')
        expression = expression.replace('x^y', '**')
        
        return expression
    
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
        
        # Validate scientific function inputs
        scientific_functions = ['sin', 'cos', 'tan', 'cot', 'asin', 'acos', 'atan', 'log', 'ln', 'π', 'e', 'x^y']
        for func in scientific_functions:
            if new_char in func:
                # Allow function input if current text ends with operator or is empty
                if not current_text or current_text[-1] in ['+', '-', '*', '/', '(']:
                    return True
                return False
        
        return True