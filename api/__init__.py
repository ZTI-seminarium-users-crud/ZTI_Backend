from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# mouse.db.elephantsql.com
# port 5432
# database: dodutbgz
# username: dodutbgz
# password: ZDFBL-EZpK9ADi6ZlO3dp_4uOHMUDpQs

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dodutbgz:ZDFBL-EZpK9ADi6ZlO3dp_4uOHMUDpQs@mouse.db.elephantsql.com:5432/dodutbgz"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'My First API SDasdasda!!'