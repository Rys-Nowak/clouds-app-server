from flask import Flask
from flask_cors import CORS

from routes.api import api
from CloudClassifier import CloudClassifier


app = Flask(__name__)
app.config['CLIENT_URL'] = 'http://localhost:4200'
cors = CORS(app, resources={r"/api/*": {"origins": app.config['CLIENT_URL']}})
app.register_blueprint(api, url_prefix='/api')
app.config['cls'] = CloudClassifier()
app.config['cls'].load_model()

@app.route("/")
def home():
    return "<p>Hi!</p>"
