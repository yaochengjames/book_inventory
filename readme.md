# Book Inventory Management System

A simple web-based application to manage an inventory of books. This system allows users to:

- **Add new books** to the inventory.
- **Filter existing books** based on criteria such as title, author, genre, and publication date.
- **Export book data** in CSV or JSON formats.

---

## Features

- **Add Books**: Input book details including title, author, genre, publication date, and ISBN.
- **Filter Books**: Search and filter books by title, author, genre, or publication date.
- **Export Data**: Export the entire inventory in CSV or JSON format.
- **Simple UI**: User-friendly interface built with basic HTML and CSS.

---

## Prerequisites

- **Python 3.x** installed on your machine.
- **pip** package manager.

---

## Installation

1. **Clone the Repository**

2. **Install Required Packages** : pip install flask

3. **Initialize the Database** : python init_db.py

4. **Running the Application** : python app.py

## Design Decisions

Simplicity: Chose Python Flask and SQLite to keep the project straightforward and easy to set up.
Minimal Frontend: Used basic HTML and CSS to focus on functionality without the complexity of frontend frameworks.
Dynamic Query Building: Implemented dynamic SQL queries with parameterized inputs to handle filtering while preventing SQL injection attacks.
Template Inheritance: Utilized Jinja2 template inheritance for code reusability and a consistent layout.

## Challenges Faced

Input Validation: Ensured required fields are validated and provided meaningful error messages to the user.
Unique Constraints: Handled the uniqueness of ISBN numbers and provided feedback if a duplicate ISBN is entered.
Data Export: Managed in-memory file creation for exporting data in CSV and JSON formats without writing to disk.
