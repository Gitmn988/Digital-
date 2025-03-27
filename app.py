import os
from flask import Flask, render_template

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    """Render the main bibliography generator page"""
    return render_template('index.html')

# Per Vercel - Esporta app come handler WSGI
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
