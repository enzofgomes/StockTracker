import os
import logging
from flask import Flask
from flask_wtf.csrf import CSRFProtect

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Import routes after app creation to avoid circular imports
from routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
