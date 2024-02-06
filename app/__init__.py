from flask import Flask

app = Flask(__name__)

# Import views (route handlers) after creating the Flask app object
from app import views
