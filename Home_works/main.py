from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home_page() -> str:
    return "HELLO FROM FLASK APP!!!"

@app.route('/user/<name>')
def user(name):
    return f"Hello, {name}! Welcome to Flask app."

if __name__ == '__main__':
    app.run(debug=True)