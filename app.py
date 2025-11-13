from flask import Flask

app = Flask(__name__)


if "__main__" == __name__:
    app.run(debug=True)