"""
Unit tests for the Calculator class.
"""

import sys
import os
import pytest
from pathlib import Path

# Add the src directory to the path so we can import the app module
sys.path.append(str(Path(__file__).parent.parent))
from src.app import Calculator

class TestCalculator:
    """Test class for Calculator"""
    
    def setup_method(self):
        """Set up a calculator instance before each test"""
        self.calculator = Calculator()
    
    def test_simple_addition(self):
        """Test simple addition calculation"""
        result = self.calculator.calculate("2+3")
        assert result == 5
    
    def test_simple_subtraction(self):
        """Test simple subtraction calculation"""
        result = self.calculator.calculate("5-3")
        assert result == 2
    
    def test_simple_multiplication(self):
        """Test simple multiplication calculation"""
        result = self.calculator.calculate("4*5")
        assert result == 20
    
    def test_simple_division(self):
        """Test simple division calculation"""
        result = self.calculator.calculate("10/2")
        assert result == 5
    
    def test_complex_expression(self):
        """Test complex expression with operator precedence"""
        result = self.calculator.calculate("3+4*2-(1+1)")
        assert result == 9
    
    def test_parentheses(self):
        """Test expressions with parentheses"""
        result = self.calculator.calculate("(3+4)*(2-1)")
        assert result == 7
    
    def test_nested_parentheses(self):
        """Test expressions with nested parentheses"""
        result = self.calculator.calculate("((3+4)*(2-1))/7")
        assert result == 1
    
    def test_decimal_numbers(self):
        """Test calculations with decimal numbers"""
        result = self.calculator.calculate("3.5+2.5")
        assert result == 6.0
    
    def test_spaces(self):
        """Test that spaces are properly handled"""
        result = self.calculator.calculate("3 + 4 * 2")
        assert result == 11
    
    def test_empty_expression(self):
        """Test empty expression returns 0"""
        result = self.calculator.calculate("")
        assert result == 0
    
    def test_division_by_zero(self):
        """Test division by zero raises an error"""
        with pytest.raises(ZeroDivisionError):
            self.calculator.calculate("5/0")
    
    def test_invalid_expression(self):
        """Test invalid expression raises ValueError"""
        with pytest.raises(ValueError):
            self.calculator.calculate("3++4")
