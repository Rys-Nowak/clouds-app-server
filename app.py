from flask import Flask

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route("/")
def home():
    return "<p>Hi!</p>"