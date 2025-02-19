# Amazon User Authentication System

## Overview
This project implements a **User Authentication System** in Python using `bcrypt` for password hashing, `regex` for validation, and `CSV` for data storage. It includes features such as:

- **User Registration with Secure Password Storage**
- **Login System with Account Lockout on Multiple Failed Attempts**
- **Email & Password Validation Using Regex**
- **Multi-Factor Authentication via OTP**
- **Logging Failed Login Attempts**

## Features

### 1. User Registration
- Checks if the user already exists (based on email/username).
- Ensures a valid email format using `regex`.
- Enforces a strong password policy:
  - At least 7 characters long
  - At least one uppercase letter
  - At least one special character (`# $ % @ _`)
  - Must end with a digit
- Hashes passwords securely with `bcrypt` before storing.
- Stores user details in a CSV file (`dta.csv`).

### 2. User Login
- Allows existing users to log in by verifying their credentials.
- Implements account lockout after 3 failed login attempts.
- Logs unsuccessful login attempts in `login_attempts.log`.

### 3. Multi-Factor Authentication (MFA)
- Generates a **One-Time Password (OTP)**.
- Grants access only after successful OTP verification.

## Technologies Used
- **Python**: Core programming language
- **bcrypt**: Password hashing
- **re (Regex)**: Email and password validation
- **csv**: Storing user details
- **smtplib & email**: Sending OTP via email

## Usage
Run the script:
```sh
python script.py
```
Follow the on-screen prompts to register or log in.

## License
This project is licensed under the **MIT License**.

