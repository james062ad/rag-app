import sys
import os

# Add the parent directory to the Python path so we can import basic_functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_functions import add, subtract, multiply

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(2, 3) == 6
