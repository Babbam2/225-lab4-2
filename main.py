from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        if name and phone:
            db = get_db()
            db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            db.commit()
            message = 'Contact added successfully.'
        else:
            message = 'Missing name or phone number.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact Information</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            margin-top: 20px;
            color: #333;
        }
        table {
            margin: 0 auto;
            border-collapse: collapse;
            width: 80%;
            background-color: #fff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            color: #333;
            text-transform: uppercase;
        }
        td {
            background-color: #fff;
            color: #666;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f2f2f2;
        }
        form {
            text-align: center;
            margin-top: 20px;
        }
        input[type="text"], input[type="submit"] {
            padding: 8px;
            margin: 5px;
        }
    </style>
</head>
<body>
    <h1>Contact Information</h1>
    <form action="/" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name">
        <label for="phone">Phone Number:</label>
        <input type="text" id="phone" name="phone">
        <input type="submit" value="Add Contact">
    </form>
    <table>
        <tr>
            <th>Name</th>
            <th>Phone Number</th>
        </tr>
        {% for contact in contacts %}
        <tr>
            <td>{{ contact['name'] }}</td>
            <td>{{ contact['phone'] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% if message %}
    <p>{{ message }}</p>
    {% endif %}
</body>
</html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
