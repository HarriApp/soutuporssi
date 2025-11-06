from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Tähän tulee Soutupörssi"

if __name__ == '__main__':
    app.run(debug=False)