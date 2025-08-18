"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from pydantic import BaseModel
import os
import re
import operator
from typing import Dict, List, Callable, Union, Optional
from pathlib import Path

class Calculator:
    """
    An efficient calculator class that evaluates mathematical expressions.
    Supports basic arithmetic operations: +, -, *, /, (, and ).
    """
    def __init__(self):
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
    
    def calculate(self, expression: str) -> float:
        """
        Efficiently calculates the result of a mathematical expression using
        the Shunting Yard algorithm to handle operator precedence.
        
        Args:
            expression: A string containing a mathematical expression
            
        Returns:
            The calculated result as a float
        
        Raises:
            ValueError: If the expression is invalid
        """
        # Remove all spaces
        expression = expression.replace(' ', '')
        
        # Check if expression is empty
        if not expression:
            return 0
            
        # Validate the expression format
        # Check for consecutive operators which are invalid (e.g., "3++4")
        for i in range(len(expression) - 1):
            if (expression[i] in self.operations and 
                expression[i+1] in self.operations):
                raise ValueError(f"Invalid expression: consecutive operators {expression[i]}{expression[i+1]}")
        
        # Define operator precedence
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        
        # Initialize stacks for operators and values
        operators = []
        values = []
        
        i = 0
        try:
            while i < len(expression):
                char = expression[i]
                
                # Handle numbers (including decimals)
                if char.isdigit() or char == '.':
                    num = ''
                    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                        num += expression[i]
                        i += 1
                    try:
                        values.append(float(num))
                    except ValueError:
                        raise ValueError(f"Invalid number format: {num}")
                    continue
                
                # Handle parentheses
                elif char == '(':
                    operators.append(char)
                elif char == ')':
                    while operators and operators[-1] != '(':
                        self._apply_operator(operators, values)
                    if operators and operators[-1] == '(':
                        operators.pop()  # Remove the '('
                    else:
                        raise ValueError("Mismatched parentheses")
                
                # Handle operators
                elif char in self.operations:
                    while (operators and operators[-1] != '(' and 
                        operators[-1] in precedence and 
                        precedence.get(char, 0) <= precedence.get(operators[-1], 0)):
                        self._apply_operator(operators, values)
                    operators.append(char)
                else:
                    raise ValueError(f"Unknown character in expression: {char}")
                
                i += 1
            
            # Apply remaining operators
            while operators:
                op = operators[-1]
                if op == '(' or op == ')':
                    raise ValueError("Mismatched parentheses")
                self._apply_operator(operators, values)
                
            # The result should be the only value left in the values stack
            if len(values) != 1:
                raise ValueError("Invalid expression")
                
            return values[0]
            
        except (IndexError, ZeroDivisionError) as e:
            if isinstance(e, ZeroDivisionError):
                raise
            raise ValueError("Invalid expression format")
    
    def _apply_operator(self, operators: List[str], values: List[float]) -> None:
        """Apply the top operator to the top two values on the values stack"""
        if not operators:
            raise ValueError("Invalid expression: missing operator")
            
        operator = operators.pop()
        if operator in self.operations:
            if len(values) < 2:
                raise ValueError("Invalid expression: not enough values for operation")
                
            right = values.pop()
            left = values.pop()
            
            # Handle division by zero explicitly
            if operator == '/' and right == 0:
                raise ZeroDivisionError("Division by zero")
                
            values.append(self.operations[operator](left, right))


# User model for authentication
class User(BaseModel):
    email: str
    username: str

# Global user storage
users_db = {}

# OAuth configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get current user
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    if token not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return users_db[token]

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    # Intellectual
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Science Club": {
        "description": "Explore science experiments and participate in science fairs",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    # Sports
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": []
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly games",
        "schedule": "Fridays, 5:00 PM - 6:30 PM",
        "max_participants": 20,
        "participants": []
    },
    # Artistic
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Drama Society": {
        "description": "Act in plays and learn about theater production",
        "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 14,
        "participants": []
    },
    "Music Ensemble": {
        "description": "Perform music in a group and learn new instruments",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Prevent duplicate registration
    if email in activity["participants"]:
        return {"error": "Student already registered for this activity."}
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

# Auth token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Login form data model
class LoginData(BaseModel):
    username: str
    password: str

# Token endpoint
@app.post("/token", response_model=Token)
def login_for_access_token(login_data: LoginData):
    """
    OAuth token endpoint for user authentication
    """
    # Note: In a real application, this would validate against a proper database
    # and use secure password hashing
    
    # For demo purposes, we'll accept any login with password "password"
    if login_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate a simple token (in production use JWT or similar)
    token = f"user-{login_data.username}-token"
    
    # Store user in our db
    users_db[token] = User(email=f"{login_data.username}@mergington.edu", username=login_data.username)
    
    return {"access_token": token, "token_type": "bearer"}

# User information endpoint
@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information (requires authentication)
    """
    return current_user

# Calculator endpoint
@app.post("/calculate")
def calculate_expression(expression: str, current_user: User = Depends(get_current_user)):
    """
    Calculate the result of a mathematical expression.
    Requires user to be authenticated.
    """
    calculator = Calculator()
    try:
        result = calculator.calculate(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating expression: {str(e)}")
