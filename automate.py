import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ticketing_db",
        user="postgres",
        password="11b09postgres"
    )
    return conn

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

# Selenium login function
def login_and_download_cert(username, password):
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("http://dummywebsite.com/login")  

        # Find and fill fields
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        time.sleep(2)  # Wait 

        
        driver.find_element(By.ID, "download_certificate").click()  

        print("Certificate download initiated.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fullname = input("Enter Full Name: ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    email = input("Enter Email ID: ")

    user = get_user_credentials(fullname, dob, email)

    if user:
        username, password = user
        login_and_download_cert(username, password)
    else:
        print("User not found or credentials do not match.")
