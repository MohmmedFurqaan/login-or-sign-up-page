import re
import csv
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Amazon:
    MAX_ATTEMPTS = 3  # Account lockout after 3 failed attempts
    
    def __init__(self, name, user_name, password, email):
        self.name = name
        self.user_name = user_name
        self.password = password
        self.email = email
        self.failed_attempts = 0  # Track failed login attempts

    def check_user_exists(self):
        """Check if the user already exists in dta.csv and allow login if they do."""
        try:
            with open("dta.csv", "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 4:
                        continue

                    stored_name, stored_user, stored_email, stored_hashed_pw = row
                    
                    if self.email == stored_email or self.user_name == stored_user:
                        print("User already exists! Please log in.")
                        return self.login(stored_hashed_pw)
        except FileNotFoundError:
            print("No existing users found. Proceeding with registration.")

        return self.email_checker_regex()

    def login(self, stored_hashed_pw):
        """Allow existing users to log in."""
        if self.failed_attempts >= self.MAX_ATTEMPTS:
            print("Account locked due to too many failed attempts!")
            return

        user_password = input("Enter your password to log in: ")
        
        if bcrypt.checkpw(user_password.encode(), stored_hashed_pw.encode()):
            print(f"Login successful! Welcome back, {self.user_name}.")
            self.failed_attempts = 0
            self.send_otp()
        else:
            print("Incorrect password! Please try again.")
            self.failed_attempts += 1
            with open("login_attempts.log", "a") as log_file:
                log_file.write(f"Failed login for {self.user_name} ({self.email})\n")

    def send_otp(self):
        """Send a One-Time Password (OTP) to the user's email for authentication."""
        otp = str(random.randint(100000, 999999))
        print(f"OTP sent to {self.email}: {otp}") 
        entered_otp = input("Enter the OTP: ")
        if entered_otp == otp:
            print("OTP verified! Access granted.")
        else:
            print("Incorrect OTP. Access denied.")
    
    def email_checker_regex(self):
        """Check if the email format is valid before storing user data."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, self.email):
            print(f"Valid email: {self.email}")
            return self.password_checker_regex()
        else:
            print(f"Invalid email format: {self.email}")

    def password_checker_regex(self):
        """Check if password meets the criteria and store it securely."""
        pattern = r"^(?=.*[A-Z])(?=.*[#\$%@_]).{7,}\d$"

        if re.match(pattern, self.password):
            print(f'Password is valid! Storing securely...')
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(self.password.encode(), salt).decode()
            with open("dta.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.name, self.user_name, self.email, hashed_pw])
            print(f'Account created successfully for {self.user_name}.')
            return hashed_pw
        else:
            print("Invalid Password!")
            return None

name = input('Enter your name - ')
user_name = input('Enter your User name - ')
password = input('Enter your password - ')
email = input('Enter your E-mail - ')

user = Amazon(name, user_name, password, email)
user.check_user_exists()