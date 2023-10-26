from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/bike")
def h():
    return "H"
