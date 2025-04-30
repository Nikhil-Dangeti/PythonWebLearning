
from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST')
)
cursor = conn.cursor()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data['name']
    college = data['college']
    email = data['email']
    password = data['password']

    cursor.execute("INSERT INTO users (name, college, email, password) VALUES (%s, %s, %s, %s)",
                   (name, college, email, password))
    conn.commit()
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    cursor.execute("SELECT name, college, email FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        name, college, email = user
        return jsonify({
            'success': True,
            'user': {
                'name': name,
                'college': college,
                'email': email
            }
        })
    else:
        return jsonify({'success': False})

@app.route('/contact', methods=['POST'])
def contact():
    data = request.form
    name = data.get('name')
    college = data.get('college')
    email = data.get('email')
    message = data.get('message')

    # print or store message (already working)
    print(f"New Contact Message:\nName: {name}\nCollege: {college}\nEmail: {email}\nMessage: {message}")

    # Show thank you page
    return send_from_directory('static', 'contact_thankyou.html')

# Serve any other static files (HTML, JS, CSS, PDFs)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
