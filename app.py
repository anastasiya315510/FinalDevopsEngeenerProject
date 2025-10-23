"""
Main Flask application module.
Registers health check Blueprint and defines the root endpoint.
"""

from flask import Flask
from health import health_bp

app = Flask(__name__)

# Register the health check Blueprint
app.register_blueprint(health_bp)

@app.route('/')
def hello_world():
    """
    Root endpoint returning a simple greeting.

    Returns:
        str: 'Hello, World!'
    """
    return 'Hello, World!'


if __name__ == "__main__":
    """
    Entry point for running the Flask application.
    Listens on all interfaces (0.0.0.0) and port 8000 with debug mode enabled.
    """
    app.run(host="0.0.0.0", port=8000, debug=True)
