# Mergington High School API - Development Guide

## Project Overview

This is a FastAPI-based backend service for Mergington High School that provides:
1. An activities management system where students can view and sign up for extracurricular activities
2. A simple calculator service for authenticated users
3. Basic user authentication

## Architecture

- **Backend**: FastAPI application (`src/app.py`) serving both API endpoints and static content
- **Frontend**: Simple HTML/CSS/JS application (`src/static/`) that interacts with the API
- **Data Storage**: All data is stored in-memory (no database)

## Key Components

### 1. Activity Management
- Activities are stored in an in-memory dictionary
- Each activity has: description, schedule, max_participants, and current participants
- See pattern in `src/app.py` activities dictionary for structure

### 2. Calculator Implementation
- Uses Shunting Yard algorithm for expression parsing and evaluation
- Supports basic arithmetic operations (+, -, *, /), parentheses, and decimal numbers
- Complete with error handling for invalid expressions and division by zero

### 3. Authentication
- Simple token-based authentication with OAuth2PasswordBearer
- All user data is in-memory and lost on server restart
- Default password is "password" for all users

## Developer Workflows

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python src/app.py

# Access UI at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculator.py
pytest tests/test_auth.py
```

### Project Conventions

1. **Routes Structure**:
   - Root (`/`) redirects to static content
   - API endpoints use REST conventions
   - Protected endpoints require Bearer token authentication

2. **Error Handling**:
   - Use FastAPI HTTPException with appropriate status codes
   - Always return consistent error format in responses

3. **Testing**:
   - Tests are in the `tests/` directory
   - Test files are named `test_*.py`
   - Use pytest fixtures for test setup

## Key Integration Points

1. **Frontend-Backend Communication**:
   - Frontend uses fetch API to communicate with backend
   - Authentication token is stored in localStorage
   - See examples in `src/static/app.js`

2. **Authentication Flow**:
   - Login at `/token` endpoint to receive token
   - Send token in Authorization header for protected endpoints
   - Example protected endpoint: `/calculate` and `/users/me`
