from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nfguungcfacwou:56c7978349cfd5cf75b8ef020f57484a0afe5f8dbec4e50f58c0e6567de55f01@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d803vl9ihrme0c'

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

@app.route('/book/input', methods=['POST'])
def books_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        reg = Book(title, author)
        db.session.add(reg)
        db.session.commit()
        return jsonify('Data Posted')
    return jsonify('Something went terribly wrong')

@app.route('/books', methods=["GET"])
def return_books():
    all_books = db.session.query(Book.id, Book.title, Book.author).all()
    return jsonify(all_books)

@app.route('/book/<id>', methods=['GET'])
def return_single_book(id):
    one_book=db.session.query(Book.id, Book.title, Book.author).filter(Book.id == id).first()
    return jsonify(one_book)

@app.route('/delete/<id>', methods=["DELETE"])
def book_delete(id):
    record = db.session.query(Book).get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify('Deleted')

@app.route('/update_book/<id>', methods=['PUT'])
def book_update(id):
    if request.content_type == 'application/json':
        put_data = request.get_json()
        title = put_data.get('title')
        author = put_data.get('author')
        record = db.session.query(Book).get(id)
        record.title = title
        record.author = author
        db.session.commit()
        return jsonify('update completed')
    return jsonify("something went horribly wrong")

if __name__ == "__main__":
    app.debug = True
    app.run()