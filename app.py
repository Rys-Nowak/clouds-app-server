from flask import Flask
from routes.api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
# app.config['SECRET_KEY'] = 'your_secret_key_here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route("/")
def home():
    return "<p>Hi!</p>"