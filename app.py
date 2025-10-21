from flask import Flask

from health import health_bp

app = Flask(__name__)

app.register_blueprint(health_bp)


@app.route('/')
def hello_world():
    return 'Hello, World!'



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)