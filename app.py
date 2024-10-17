from flask import Flask, render_template, request, jsonify,redirect, url_for
from werkzeug.security import generate_password_hash
import hashlib
import time
import jwt
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
from transformers import pipeline

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ticketing_db",
        user="postgres",
        password="11b09postgres"
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
def index():
    return render_template('index.html')

# Define the register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        # Insert into PostgreSQL
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        conn.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/MyTickets')
def my_tickets_page():
    return render_template('MyTickets.html')

@app.route('/CreateTicket', methods=['POST','GET'])
def create_ticket_page():
    return render_template('CreateTicket.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

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

# Load Hugging Face sentiment analysis model
sentiment_analysis = pipeline(task="sentiment-analysis", model="SamLowe/roberta-base-go_emotions")

# API to retrieve new tickets 
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT ticket_id, user_id, software_name, ticket_status FROM tickets")
    tickets = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Create a list of dictionaries to return as JSON
    ticket_list = []
    for ticket in tickets:
        ticket_dict = {
            'ticket_id': ticket[0],
            'user_id': ticket[1],
            'software_name': ticket[2],
            'ticket_status': ticket[3],
            'priority': 'Closed' if ticket[3] in ['Closed', 'Resolved'] else 'Open'  # Priority logic
        }
        ticket_list.append(ticket_dict)

    return jsonify(ticket_list), 200

# API to submit a ticket
@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()  # Get JSON data from the request body

    user_id = data.get('user_id')  # Extract user_id from the JSON data
    software_name = data.get('software_name')  # Extract software_name from the JSON data
    ticket_message = data.get('message')  # The description or message
    
    ticket_status = "Pending"
    request_time = datetime.now()

    # Sentiment analysis logic
    sentiment_result = sentiment_analysis(ticket_message)
    sentiment_label = sentiment_result[0]['label']  # Sentiment result (e.g., 'POSITIVE', 'NEGATIVE')

    negative_emotions = ['anger', 'sadness', 'grief', 'disgust', 'disappointment', 'worry', 'annoyance', 'disapproval', 'remorse', 'fear', 'confusion']
    ticket_status = "Urgent" if sentiment_label.lower() in negative_emotions else "Low"

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the user exists
    cur.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
    user_exists = cur.fetchone()[0]

    if user_exists == 0:
        return jsonify({"error": "User ID does not exist. Please provide a valid user."}), 400

    # Insert the ticket into the database
    cur.execute(
        "INSERT INTO tickets (user_id, software_name, ticket_status, request_time) VALUES (%s, %s, %s, %s) RETURNING ticket_id",
        (user_id, software_name, ticket_status, request_time)
    )
    ticket_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Ticket submitted successfully", "ticket_id": ticket_id}), 201



if __name__ == '__main__':
    app.run(debug=True)
