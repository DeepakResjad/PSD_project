from flask import Flask, render_template, request, jsonify,redirect, url_for, session, render_template_string
from werkzeug.security import generate_password_hash,check_password_hash
import hashlib , uuid
import time
import jwt
from datetime import datetime, timedelta
import os, psycopg2
from psycopg2.extras import RealDictCursor
from transformers import pipeline
import openai
import os
from transformers.file_utils import TRANSFORMERS_CACHE
from automate import login_and_download_cert , reset_password , get_user_credentials, generate_and_send_otp
# from sklearn.cluster import KMeans


print(TRANSFORMERS_CACHE)

app = Flask(__name__)
SECRET_KEY = "your_secret_key"  # Define your secret key

app.secret_key = SECRET_KEY  # Set the secret key for session management

mock_org_users = {"user1": "pass123"}

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ticketing_db",
        user="postgres",
        password="11b09postgres"
    )
    return conn


# def get_db_connection():
#     connection_string = os.getenv('DB_CONNECTION_STRING')  # Retrieve connection string from environment variable
#     if not connection_string:
#         raise ValueError("No database connection string found. Ensure DB_CONNECTION_STRING is set.")
#     conn = psycopg2.connect(connection_string)
#     return conn




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

# @app.route('/protected')
# @token_required  # Decorator to enforce token authentication
# def protected():
#     return jsonify({'message': 'This is a protected route'}), 200


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

        return render_template('login.html')
    
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

@app.route('/login', methods=['GET', 'POST'])
def login_submit():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query user from the PostgreSQL database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, password_hash FROM users WHERE email = %s", (email,))
        user = cur.fetchone()  # Fetch one matching row
        cur.close()
        conn.close()

        if user:
            user_id, stored_password_hash = user  # Fetch user_id and password_hash

            # Check if the password matches
            if check_password_hash(stored_password_hash, password):
                session['user_id'] = user_id  # Store user ID in session
                return redirect(url_for('dashboard'))  # Redirect to dashboard on successful login
            else:
                return render_template('login.html', error="Invalid email or password"), 401
        else:
            return render_template('login.html', error="Invalid email or password"), 401

    # Render the login page for GET requests
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Get the logged-in user from the PostgreSQL database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, email FROM users WHERE user_id = %s", (session['user_id'],))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            username, email = user
            return render_template('dashboard.html', username=username, email=email)
    else:
        return redirect(url_for('login_submit'))  # Redirect to login if user is not logged in


@app.route('/contact')
def contact_page():
    return render_template('contact.html')

# Handle favicon.ico request
@app.route('/favicon.ico')
def favicon():
    return '', 204


# # API to request admin privileges
# @app.route('/api/request-admin', methods=['POST'])
# def request_admin():
#     data = request.json
#     username = data.get('username')
#     secret = data.get('secret')

#     # Fetch user from the database
#     user = get_user(username)
    
#     if user is None:
#         return jsonify({"error": "Invalid user"}), 401

#     # Verify user secret (password hash comparison)
#     if user['password_hash'] != hash_secret(secret):
#         return jsonify({"error": "Invalid secret"}), 401

#     token = generate_token(username)
#     return jsonify({"message": "Admin token generated", "token": token}), 200

@app.route('/logout')
def logout():
    # Clear session data to log the user out
    session.clear()
    # Redirect to login page (assuming you have a login route)
    return redirect(url_for('login_page'))

# API to grant admin privileges
@app.route('/api/grant-admin', methods=['POST'])
def grant_admin():
    data = request.json
    token = data.get('token')

# # API to grant admin privileges
# @app.route('/api/grant-admin', methods=['POST'])
# def grant_admin():
#     data = request.json
#     token = data.get('token')


#     username = verify_token(token)

#     if not username:
#         return jsonify({"error": "Invalid or expired token"}), 401

#     user = get_user(username)

#     if user is None:
#         return jsonify({"error": "Invalid user"}), 401

#     # Criteria to grant admin privileges (e.g., time check)
#     if time.localtime().tm_hour in range(9, 18):  # Only allow during office hours
#         conn = get_db_connection()
#         cur = conn.cursor()
        
#         cur.execute(
#             "UPDATE users SET is_admin = 'admin' WHERE username = %s",
#             (True, username)
#         )
#         conn.commit()
        
#         cur.close()
#         conn.close()

#         log_admin_action(username, 'Granted Admin Privileges')
#         return jsonify({"message": f"Admin privileges granted to {username}"}), 200
#     else:
#         return jsonify({"error": "Request outside of allowed time window"}), 403

# # API to revoke admin privileges
# @app.route('/api/revoke-admin', methods=['POST'])
# def revoke_admin():
#     data = request.json
#     token = data.get('token')

#     username = verify_token(token)

#     if not username:
#         return jsonify({"error": "Invalid or expired token"}), 401

#     user = get_user(username)

#     if user is None or user['role'] != 'admin':
#         return jsonify({"error": "User is not an admin"}), 400

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "UPDATE users SET role = %s, admin_granted_at = %s WHERE username = %s",
#         ('user', None, username)
#     )
#     conn.commit()
    
#     cur.close()
#     conn.close()

#     log_admin_action(username, 'Revoked Admin Privileges')
#     return jsonify({"message": f"Admin privileges revoked from {username}"}), 200

# Load Hugging Face sentiment analysis model
sentiment_analysis = pipeline(task="sentiment-analysis", model="SamLowe/roberta-base-go_emotions")
print("Model loaded successfully:", sentiment_analysis)

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
    request_type = data.get("request_type", "general")  # Default to 'general' if not specified

    # Default values for ticket status and priority
    ticket_status = "Open"  # Status is now either "Open" or "Closed"
    request_time = datetime.now()

    # Sentiment analysis logic
    sentiment_result = sentiment_analysis(ticket_message)
    sentiment_label = sentiment_result[0]['label']  # Sentiment result (e.g., 'POSITIVE', 'NEGATIVE')

    # Set ticket priority based on sentiment analysis
    negative_emotions = ['anger', 'sadness', 'grief', 'disgust', 'disappointment', 'worry', 'annoyance', 'disapproval', 'remorse', 'fear', 'confusion']
    ticket_priority = "Urgent" if sentiment_label.lower() in negative_emotions else "Low"

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the user exists
    cur.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
    user_exists = cur.fetchone()[0]

    if user_exists == 0:
        return jsonify({"error": "User ID does not exist. Please provide a valid user."}), 400

    # Insert the ticket into the database
    insert_query = """
        INSERT INTO tickets (user_id, software_name, ticket_status, ticket_priority, request_time, request_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING ticket_id
    """
    cur.execute(insert_query, (user_id, software_name, ticket_status, ticket_priority, request_time, request_type))
    ticket_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Ticket submitted successfully", "ticket_id": ticket_id}), 201

@app.route('/api/tickets/<int:ticket_id>/status', methods=['PATCH'])
def update_ticket_status(ticket_id):
    data = request.get_json()  # Get the JSON data from the request body
    new_status = data.get('ticket_status')  # Extract the new status (e.g., "Closed")

    if new_status not in ["Open", "Closed"]:
        return jsonify({"error": "Invalid status. Status must be 'Open' or 'Closed'."}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the ticket exists
    cur.execute("SELECT COUNT(*) FROM tickets WHERE ticket_id = %s", (ticket_id,))
    ticket_exists = cur.fetchone()[0]

    if ticket_exists == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "Ticket ID does not exist."}), 404

    # Update the ticket's status
    update_query = "UPDATE tickets SET ticket_status = %s WHERE ticket_id = %s"
    cur.execute(update_query, (new_status, ticket_id))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": f"Ticket status updated to '{new_status}'."}), 200


@app.route('/api/ticket_counts', methods=['GET'])
def get_ticket_counts():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Query to get counts of tickets grouped by status
        cur.execute("SELECT ticket_status, COUNT(*) FROM tickets GROUP BY ticket_status")
        ticket_counts = cur.fetchall()

        # Prepare ticket counts in a structured format
        counts = {
            'open': 0,
            'closed': 0,
            'in_progress': 0,
            'resolved': 0
        }

        for status, count in ticket_counts:
            if status == "Open":
                counts['open'] = count
            elif status == "Closed":
                counts['closed'] = count
            elif status == "In Progress":
                counts['in_progress'] = count
            elif status == "Resolved":
                counts['resolved'] = count

        return jsonify(counts), 200

    except Exception as e:
        print(f"Error fetching ticket counts: {e}")
        return jsonify({"error": "Unable to fetch ticket counts"}), 500

    finally:
        cur.close()
        conn.close()


#SECURE GATEWAY

# @app.route("/mock_org_login", methods=["GET", "POST"])
# def mock_org_login():
#     # Render a simple HTML form for user login
#     if request.method == "GET":
#         return render_template_string("""
#         <form method="POST">
#             <label for="username">Username:</label>
#             <input type="text" name="username" required>
#             <label for="password">Password:</label>
#             <input type="password" name="password" required>
#             <button type="submit">Login</button>
#         </form>
#         """)

#     # Process login form submission
#     username = request.form.get("username")
#     password = request.form.get("password")
#     if username in mock_org_users and mock_org_users[username] == password:
#         # Simulate an authorization code and redirect
#         auth_code = str(uuid.uuid4())  # Generate a mock authorization code
#         session["mock_auth_code"] = auth_code  # Store the code in the session
#         print(f"Stored auth_code in session: {session.get('mock_auth_code')}")
#         return redirect(url_for("callback", code=auth_code))
#     else:
#         return "Invalid credentials. Please try again.", 401
    
# @app.route("/callback")
# def callback():
#     # Check for the authorization code in the URL
#     auth_code = request.args.get("code")
#     if auth_code and auth_code == session.get("mock_auth_code"):
#         # "Exchange" the code for an access token (simply set session data in this case)
#         session["user_authenticated"] = True
#         session["username"] = "user1"  # Mock user info
#         return redirect(url_for("create_ticket"))  # Redirect to the ticket submission page
#     else:
#         return "Invalid authorization code", 400


#GEN AI IMPLEMENTATION

# Automated Response Generation

# # Initialize the model pipeline
# response_generator = pipeline("text-generation", model="gpt-3.5-turbo")

# def generate_response(prompt):
#     response = response_generator(prompt, max_length=100, num_return_sequences=1)
#     return response[0]['generated_text']

# @app.route('/generate_response', methods=['POST'])
# def generate_ticket_response():
#     data = request.json
#     prompt = data.get('content')
#     if prompt:
#         response = generate_response(prompt)
#         return jsonify({"response": response}), 200
#     return jsonify({"error": "Content is required"}), 400



# Dynamic Knowledge Base Creation

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def create_knowledge_base_entry(tickets):
#     clusters = KMeans(n_clusters=5).fit(tickets)  # Example with 5 clusters
#     knowledge_base = {}
#     for idx, cluster in enumerate(clusters):
#         summary = summarizer(" ".join(cluster), max_length=150, min_length=40)
#         knowledge_base[f'Cluster {idx}'] = summary[0]['summary_text']
#     return knowledge_base

# @app.route('/update_knowledge_base', methods=['POST'])
# def update_knowledge_base():
#     # Retrieve tickets from database here
#     # Example: tickets = [ticket['content'] for ticket in get_all_tickets()]
#     knowledge_base = create_knowledge_base_entry(tickets)
#     # Store knowledge_base in your DB or file
#     return jsonify({"message": "Knowledge base updated"}), 200


# Contextual Ticket Summarization

# def summarize_ticket_history(history_text):
#     summary = summarizer(history_text, max_length=100, min_length=30)
#     return summary[0]['summary_text']

# @app.route('/summarize_ticket', methods=['POST'])
# def summarize_ticket():
#     data = request.json
#     history = data.get('history')
#     if history:
#         summary = summarize_ticket_history(history)
#         return jsonify({"summary": summary}), 200
#     return jsonify({"error": "History content required"}), 400

# Predictive Text Suggestions for Agents

# def suggest_text(input_text):
#     suggestion = response_generator(input_text, max_length=50)
#     return suggestion[0]['generated_text']

# @app.route('/text_suggestion', methods=['POST'])
# def text_suggestion():
#     data = request.json
#     input_text = data.get('input')
#     if input_text:
#         suggestion = suggest_text(input_text)
#         return jsonify({"suggestion": suggestion}), 200
#     return jsonify({"error": "Input text required"}), 400

# Ticket Categorization and Priority Setting

# classifier = pipeline("text-classification", model="type-of-classifier-model")

# def categorize_ticket(content):
#     category = classifier(content)[0]['label']
#     priority = 'High' if 'urgent' in content else 'Low'
#     return category, priority

# @app.route('/categorize_ticket', methods=['POST'])
# def categorize_ticket_endpoint():
#     data = request.json
#     content = data.get('content')
#     if content:
#         category, priority = categorize_ticket(content)
#         return jsonify({"category": category, "priority": priority}), 200
#     return jsonify({"error": "Content required"}), 400


# Home route to render the chatbot HTML page

user_data = {}

@app.route('/chat')
def chatbot():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message").lower().strip()

    # Check if session data already exists
    if "fullname" not in session:
        session["fullname"] = message
        return jsonify({"response": "Thank you! Can I have your email address?"})

    if "email" not in session:
        session["email"] = message
        return jsonify({"response": "Thank you! Lastly, may I have your date of birth (YYYY-MM-DD)?"})

    if "dob" not in session:
        try:
            datetime.strptime(message, "%Y-%m-%d")  # Validate DOB format
            session["dob"] = message
            return jsonify({"response": "Thank you for the details! Type 'reset password' or 'download certificate' to proceed."})
        except ValueError:
            return jsonify({"response": "Invalid date format. Please enter in YYYY-MM-DD format."})

    # Process the requests based on the action required
    if "reset password" in message:
        session["action"] = "reset_password"
        
        # Generate OTP and send
        otp_message = generate_and_send_otp(session["email"])
        if otp_message:
            session["otp"] = otp_message
            return jsonify({"response": f"{otp_message}. Please enter the OTP sent to your email."})
        else:
            return jsonify({"response": "Failed to send OTP. Please try again later."})

    elif "download certificate" in message:
        session["action"] = "download_certificate"

        # Fetch user credentials and initiate download
        user = get_user_credentials(session["fullname"], session["dob"], session["email"])
        if user:
            username, password = user
            result = login_and_download_cert(username, password)
            session.clear()  # Clear session data after completion
            return jsonify({"response": result})
        else:
            session.clear()
            return jsonify({"response": "User not found or credentials do not match."})

    # Default responses for greetings or unrecognized inputs
    if "hi" in message or "hello" in message:
        return jsonify({"response": "Hello! How can I assist you today?"})
    elif "thank you" in message or "thanks" in message:
        return jsonify({"response": "You're welcome!"})
    elif "bye" in message or "goodbye" in message:
        return jsonify({"response": "Goodbye! Have a great day!"})

    # Catch-all response if message doesn't fit criteria
    return jsonify({"response": "Please specify your request: 'reset password' or 'download certificate'."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')