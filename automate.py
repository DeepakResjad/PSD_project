import psycopg2
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ticketing_db",
        user="postgres",
        password="11b09postgres"
    )
    return conn

# Function to get user credentials from database
def get_user_credentials(fullname, dob, email):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username, password FROM users WHERE fullname = %s AND dob = %s AND email = %s", (fullname, dob, email))
        user = cur.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        user = None
    finally:
        cur.close()
        conn.close()

    return user

# Function to generate and send OTP
def generate_and_send_otp(email):
    otp = random.randint(100000, 998769)
    try:
        sender_email = "ticketingslu@gmail.com"
        sender_password = "gytx sspd yqkz cfye"
        subject = "Your OTP for Password Reset"
        message_body = f"Your OTP for password reset is: {otp}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        
        print("OTP sent to your email.")
        return otp
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return None

# Password reset function
def reset_password(email,new_password):
    new_password = new_password
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
        conn.commit()
        print("Password has been reset successfully.")
    except Exception as e:
        print(f"Failed to reset password: {e}")
    finally:

        cur.close()
        conn.close()

def retrieve_certificate(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Verify user credentials
        cur.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

        if user:
            user_id = user[0]
            # Fetch certificate for the user
            cur.execute("SELECT certificate_path FROM certificates WHERE user_id = %s", (user_id,))
            cert = cur.fetchone()
            
            if cert:
                certificate_path = cert[0]
                print("Certificate retrieved successfully.")
                return certificate_path
            else:
                print("No certificate found for this user.")
                return None
        else:
            print("Invalid username or password.")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving the certificate: {e}")
        return None
    finally:
        cur.close()
        conn.close()

# Example usage of the function
def login_and_download_cert(username, password):
    certificate_path = retrieve_certificate(username, password)
    if certificate_path:
        return f"Certificate path: {certificate_path}"
    else:
        return "Failed to retrieve certificate."