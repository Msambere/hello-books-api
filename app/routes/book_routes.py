from flask import Blueprint, abort, make_response, request
from app.models.book import Book
from ..db import db
from sqlalchemy import select

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")


@books_bp.post("")
def create_book():
    new_book = validate_new_book_data()
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201

@books_bp.get("")
def get_all_books():
    query = db.select(Book).order_by(Book.id)
    books = db.session.scalars(query)
    # books = db.session.execute(query).scalars() is another option

    response_body = []
    for book in books:
        response_body.append(book.to_dict())

    return response_body, 200

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)
    return book.to_dict(), 200





def validate_new_book_data():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    if not isinstance(title, str) or not isinstance(description, str):
        response = {"msg": "Invalid book details"}
        abort(make_response(response, 400))

    book_exists = bool(
        db.session.query(Book).filter_by(title=title, description=description).first()
    )

    if book_exists:
        response = {"msg": "Book already exists in database."}
        abort(make_response(response, 400))

    new_book = Book(title=title, description=description)

    return new_book


# from app.models.book import books

# @books_bp.get("")
# def get_all_books():
#     response_body=[]
#     for book in books:
#         response_body.append(book.to_dict()
#         )
#     return response_body

# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)
#     return book.to_dict(), 200


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"msg": f"Book {book_id} is invalid."}
        abort(make_response(response,400))

    # found_book = db.session.query(Book).filter_by(id =book_id).first()
    
    book_exists = bool(
        db.session.query(Book).filter_by(id = book_id).first()
    )

    if not book_exists:
        response = {"msg": f"Book {book_id} not found."}
        abort(make_response(response,404))
    
    found_book = db.select(Book).where(Book.id == book_id)
    book =db.session.scalar(found_book) 
    return book