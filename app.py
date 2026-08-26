from flask import Flask
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "Development")

@app.route("/")
def home():
    return f"Welcome to SaiBank - {APP_VERSION}!"

@app.route("/login")
def login():
    return "SaiBank Login Page"

@app.route("/balance")
def balance():
    return "Your balance: ₹50,000"

@app.route("/secret-status")
def secret_status():
    return "Secret configured ✅" if os.getenv("APP_SECRET") else "Secret missing ❌"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)