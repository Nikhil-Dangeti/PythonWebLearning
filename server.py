"""import http.server
import socketserver
import json
import psycopg2
from urllib.parse import parse_qs

PORT = 8000

# Database connection
conn = psycopg2.connect(
    dbname="python_learning",
    user="postgres",
    password="9072",
    host="localhost"
)
cursor = conn.cursor()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        if self.path == '/signup':
            name, college, email, password = data['name'], data['college'], data['email'], data['password']
            cursor.execute("INSERT INTO users (name, college, email, password) VALUES (%s, %s, %s, %s)",
                           (name, college, email, password))
            conn.commit()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())

        elif self.path == '/login':
            email, password = data['email'], data['password']
            cursor.execute("SELECT name, college, email FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            if user:
                name, college, email = user
                self.wfile.write(json.dumps({
                    'success': True,
                    'user': {
                        'name': name,
                        'college': college,
                        'email': email
                    }
                }).encode())
            else:
                self.wfile.write(json.dumps({'success': False}).encode())


    def do_GET(self):
        # Serve static files
        super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()"""


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
