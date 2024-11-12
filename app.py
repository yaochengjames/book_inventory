from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import csv
import json
from io import StringIO, BytesIO  # Added BytesIO

app = Flask(__name__)

DATABASE = 'books.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Home Page: Display and Filter Books
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Get filter criteria from the form
        title = request.form.get('title', '')
        author = request.form.get('author', '')
        genre = request.form.get('genre', '')
        publication_date = request.form.get('publication_date', '')

        # Build the query dynamically based on inputs
        query = "SELECT * FROM Inventory WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f'%{title}%')
        if author:
            query += " AND author LIKE ?"
            params.append(f'%{author}%')
        if genre:
            query += " AND genre LIKE ?"
            params.append(f'%{genre}%')
        if publication_date:
            query += " AND publication_date = ?"
            params.append(publication_date)

        cursor.execute(query, params)
    else:
        cursor.execute("SELECT * FROM Inventory")

    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Add New Book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        author = request.form['author']
        genre = request.form.get('genre', '')
        publication_date = request.form.get('publication_date', '')
        isbn = request.form['isbn']

        # Validate inputs
        errors = []
        if not title.strip():
            errors.append("Title is required.")
        if not author.strip():
            errors.append("Author is required.")
        if not isbn.strip():
            errors.append("ISBN is required.")

        if errors:
            return render_template('add_book.html', errors=errors)

        # Insert into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Inventory (title, author, genre, publication_date, isbn)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author, genre, publication_date, isbn))
            conn.commit()
        except sqlite3.IntegrityError:
            errors.append("ISBN must be unique.")
            return render_template('add_book.html', errors=errors)
        finally:
            conn.close()

        return redirect('/')
    else:
        return render_template('add_book.html')

# Export Data
@app.route('/export', methods=['GET'])
def export_data():
    export_format = request.args.get('format', 'csv')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Inventory")
    books = cursor.fetchall()
    conn.close()

    if export_format == 'csv':
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['Entry ID', 'Title', 'Author', 'Genre', 'Publication Date', 'ISBN'])
        for book in books:
            cw.writerow([book['entry_id'], book['title'], book['author'], book['genre'],
                         book['publication_date'], book['isbn']])
        output = si.getvalue().encode('utf-8')  # Encode to bytes
        return send_file(
            BytesIO(output),  # Use BytesIO
            mimetype='text/csv',
            as_attachment=True,
            download_name='books.csv'  # Updated parameter name
        )
    elif export_format == 'json':
        books_list = [dict(book) for book in books]
        output = json.dumps(books_list).encode('utf-8')  # Encode to bytes
        return send_file(
            BytesIO(output),  # Use BytesIO
            mimetype='application/json',
            as_attachment=True,
            download_name='books.json'  # Updated parameter name
        )
    else:
        return "Unsupported format", 400

if __name__ == '__main__':
    app.run(debug=True)
