from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

heroku = Heroku(app)
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    author=db.Column(db.String)

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f"Title {self.title}"

@app.route("/")
def home():
    return"<h1>Hi from Flask</h1>"

if __name__ == "__main__":
    app.debug = True
    app.run()