# Project Refactoring Summary
This document describes the major changes made when refactoring the messy-migration project to a cleaner, more maintainable structure using Blueprints, modular folders, security utils, and an application factory.


# Project Structure
Before:
# Major Issues Identified

Routes, DB logic, and security logic were combined in single files.
Hard to read and maintain.

The app did not use Flask’s recommended factory pattern.
This makes testing & config harder.

All routes were in a single file instead of modularized.

Passwords were stored in plain text or weakly hashed.

Hashing and checks were scattered in routes and models.

Mixed singular/plural route names (/user/<id> vs /users).

Not RESTful in naming.

DB connection code was duplicated across functions.

Database setup was manual.

Routes assumed JSON without validation.

Could return 415/400 if requests were invalid.

After:
# Changes Made & Why

Introduced create_app() App Factory

Allows configuration flexibility.

Makes testing easier.

Added Blueprints

Moved user routes to routes/users.py.

Easier to add more modules later.

Centralized DB Connection

database.py with get_db_connection() using row_factory for dict-like rows.

Centralized Security

security.py handles all password hashing and checking with bcrypt.

No raw password operations in routes.

Consistent RESTful Endpoints

Unified all routes to use /users for collection, /users/<id> for item.

Added /login and /search with proper query param handling.

Added init_db.py

Creates users table if not exists.

Adds default admin if missing.

Can run standalone.

Improved Error Handling

Routes now return 400 for missing fields.

No server crash if bad JSON or missing params.

Uses consistent jsonify responses.

Clean Response

No passwords exposed in /users responses.

Added Content-Type Example

Suggested setting Content-Type: application/json for POST/PUT.

# Benefits
Easier to maintain and scale.
Clean separation of concerns (routes vs models vs utilities).
Secure password handling.
Consistent error messages.
Simpler to test and deploy.


# Assumptions & Trade-offs 

No ORM (like SQLAlchemy)
We used plain SQLite commands instead of a bigger tool like SQLAlchemy.
Easy for a small project.
For bigger apps, an ORM would make things easier to manage.

No Sessions or Tokens
The login just checks the email and password — there’s no session or token to keep the user logged in.
Simple to test and learn.
Not safe enough for real use — should add JWT tokens or sessions.

Hardcoded Database File
The database is always users.db in the code.
Fine for local testing.
In real apps, it’s better to use settings from environment variables.

No Database Migrations
The database table is created with plain SQL if it doesn’t exist.
Works for a small project.
Bigger projects should use a proper tool (like Alembic) to handle database changes over time.


# What I’d Do With More Time (Simple & Relevant)
Add Login Sessions or Tokens
Right now, login just checks email and password. I’d add proper sessions or JWT tokens so users stay logged in safely.

Use SQLAlchemy Instead of Raw SQL
Right now, the app uses plain SQL and SQLite. I’d switch to SQLAlchemy to make the database easier to manage and add real migrations for updating the database.

Check Input Data
I’d add input checks with a tool like marshmallow so bad data (like empty names or wrong emails) can’t break the app.

Write Tests
I’d write tests to make sure all routes (GET, POST, PUT, DELETE, login) work as expected and keep working in the future.

Add Logging
I’d add proper logs so if something breaks, we can see exactly what happened.

Use Config Files and Docker
Right now, the database name is hardcoded. I’d move that to a .env file and run the whole app in Docker so it’s easy to run anywhere.

Add API Docs
I’d add Swagger docs so anyone using the API knows exactly what routes to call and what data to send.


# How to Run
bash
Copy
Edit
# Initialize the DB:
python init_db.py

# Start the server:
python app.py

# If Use Postman with:

POST and PUT: set Body → raw → JSON

GET /search?name=Admin → query param only
in Body->raw->JSON
[
  {
    "id": 1,
    "name": "Admin User",
    "email": "admin@example.com"
  }
]


DELETE /users/<id>


POST /Users
Include Body->raw->JSON 
{
  "name": "Alice",
  "email": "alice@example.com",
  "password": "secret123"
}

PUT /Users/<id>
{
  "name": "Updated Name",
  "email": "newemail@example.com"
}

