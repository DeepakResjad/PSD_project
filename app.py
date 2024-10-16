from flask import Flask, render_template

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
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/my-tickets')
def my_tickets():
    return render_template('my-tickets.html')

# Endpoint for the Submit Ticket page
@app.route('/SubmitTicket')
def submit_ticket_page():
    return render_template('SubmitTicket.html')

# Endpoint for the Ticket List page
@app.route('/TicketList')
def ticket_list_page():
    return render_template('TicketList.html')

@app.route('/create-ticket')
def create_ticket():
    return render_template('create-ticket.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
