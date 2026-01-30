# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
A Flask-based health tracking dashboard for CS 584 (Software Engineering). Students follow `lab_guide.md` to progressively build form handling, POST requests, and dynamic feedback features.

## Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install flask
```

### Run the app
```bash
flask run
# or
python app.py
```
App runs at `http://localhost:5000` with debug mode enabled.

## Architecture

### Structure
- `app.py` - Flask application with routes (`/` GET, `/submit` POST)
- `templates/index.html` - Jinja2 template with conditional rendering
- `static/style.css` - Styling
- `lab_guide.md` - Step-by-step lab instructions for students

### Key Patterns
- **In-memory storage**: User data stored in a Python dict (`user_data`), resets on app restart
- **PRG pattern**: POST to `/submit` redirects back to `/` to prevent duplicate submissions
- **Jinja2 conditionals**: `{% if user_data.name %}` for dynamic UI sections

### Current State
The starter code has the basic `/` route working. Students are expected to:
1. Add the health form to `index.html`
2. Implement the `/submit` POST route in `app.py`
3. Add feedback display with Jinja2 conditionals
