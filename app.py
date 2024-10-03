from flask import Flask, request, jsonify
import hashlib
import time
import jwt
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import render_template

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ticketing_db",
        user="your_db_user",
        password="your_password"
    )
    return conn

SECRET_KEY = "your_secret_key"

# Simple hash function for password checking
def hash_secret(secret):
    return hashlib.sha256(secret.encode()).hexdigest()

# Generate JWT tokens
def generate_token(username):
    expiration = datetime.utcnow() + timedelta(minutes=15)
    token = jwt.encode({'username': username, 'exp': expiration}, SECRET_KEY, algorithm='HS256')
    return token

# Verify JWT tokens
def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Logging admin actions
def log_admin_action(user, action):
    print(f"User {user} performed action: {action} at {datetime.now()}")

# Fetch user from the PostgreSQL database
def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return user

# Endpoint for homepage
@app.route('/')
def home():
    return 'Welcome to the Ticketing System!'

# Handle favicon.ico request
@app.route('/favicon.ico')
def favicon():
    return '', 204

# API to request admin privileges
@app.route('/api/request-admin', methods=['POST'])
def request_admin():
    data = request.json
    username = data.get('username')
    secret = data.get('secret')

    # Fetch user from the database
    user = get_user(username)
    
    if user is None:
        return jsonify({"error": "Invalid user"}), 401

    # Verify user secret (password hash comparison)
    if user['passwordhash'] != hash_secret(secret):
        return jsonify({"error": "Invalid secret"}), 401

    token = generate_token(username)
    return jsonify({"message": "Admin token generated", "token": token}), 200

# API to grant admin privileges
@app.route('/api/grant-admin', methods=['POST'])
def grant_admin():
    data = request.json
    token = data.get('token')

    username = verify_token(token)

    if not username:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = get_user(username)

    if user is None:
        return jsonify({"error": "Invalid user"}), 401

    # Criteria to grant admin privileges (e.g., time check)
    if time.localtime().tm_hour in range(9, 18):  # Only allow during office hours
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE users SET role = %s, admin_granted_at = %s WHERE username = %s",
            ('admin', datetime.now(), username)
        )
        conn.commit()
        
        cur.close()
        conn.close()

        log_admin_action(username, 'Granted Admin Privileges')
        return jsonify({"message": f"Admin privileges granted to {username}"}), 200
    else:
        return jsonify({"error": "Request outside of allowed time window"}), 403

# API to revoke admin privileges
@app.route('/api/revoke-admin', methods=['POST'])
def revoke_admin():
    data = request.json
    token = data.get('token')

    username = verify_token(token)

    if not username:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = get_user(username)

    if user is None or user['role'] != 'admin':
        return jsonify({"error": "User is not an admin"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET role = %s, admin_granted_at = %s WHERE username = %s",
        ('user', None, username)
    )
    conn.commit()
    
    cur.close()
    conn.close()

    log_admin_action(username, 'Revoked Admin Privileges')
    return jsonify({"message": f"Admin privileges revoked from {username}"}), 200

# API to submit a ticket
@app.route('/api/tickets', methods=['POST'])
def submit_ticket():
    data = request.json
    user_id = data.get('user_id')          # User ID should come from the request
    software_name = data.get('software_name')  # Software name from request
    ticket_status = "Pending"               # Default status for new tickets
    request_time = datetime.now()           # Capture the request time

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Insert a new ticket into the tickets table
    cur.execute(
        "INSERT INTO tickets (user_id, software_name, ticket_status, request_time) VALUES (%s, %s, %s, %s) RETURNING ticket_id",
        (user_id, software_name, ticket_status, request_time)
    )
    ticket_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Ticket submitted successfully", "ticket_id": ticket_id}), 201

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
