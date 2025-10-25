from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from App Service (Flask)'


if __name__ == '__main__':
    # For local testing only
    app.run(debug=True, host='0.0.0.0', port=8000)
