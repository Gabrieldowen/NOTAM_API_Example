from flask import Flask, render_template
from app import app

@app.route('/')
def index():
    path = render_template('index.html')
    print(f"\n{path}")
    return path