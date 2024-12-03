import psycopg2
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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

# Selenium login function
def login_and_download_cert(username, password):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("http://dummywebsite.com/login")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        time.sleep(2)
        
        driver.find_element(By.ID, "download_certificate").click()

        print("Certificate download initiated.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Main function
def main():
    reset_password("reddydeepak771@gmail.com","new_password")