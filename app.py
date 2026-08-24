from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to SaiBank - Version 3!"

@app.route("/login")
def login():
    return "SaiBank Login Page"

@app.route("/balance")
def balance():
    return "Your balance: ₹50,000"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)