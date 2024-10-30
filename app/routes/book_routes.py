from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db
from sqlalchemy import select

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")


@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title, description = validate_new_book_data(request_body)

    new_book = Book(title=title, description=description)
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
    title_param = request.args.get("title")
    if title_param:
        query = db.select(Book).where(Book.title.ilike(f"%{title_param}%")).order_by(Book.id)
    else:
        query = db.select(Book).order_by(Book.id)
    books = db.session.scalars(query)
    # books = db.session.execute(query).scalars() is another option

    response_body = []
    for book in books:
        response_body.append(book.to_dict())

    if title_param and not response_body:
        response = {"msg": f"No book titles containing '{title_param}' found."}
        abort(make_response(response,404))

    return response_body, 200

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book_id(book_id)
    return book.to_dict(), 200

@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book_id(book_id)
    request_body = request.get_json()
    
    book.title = request_body['title']
    book.description = request_body['description']
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book_id(book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")



# Helper Functions

def validate_new_book_data(request_body):
    try:
        title = request_body['title']
    except:
        response = {"msg":"Please provide a book title"}
        abort(make_response(response, 400))
    try:
        description = request_body['description']
    except:
        response = {"msg":"Please provide a book description"}
        abort(make_response(response, 400))
    if not isinstance(title, str) or not isinstance(description, str):
        response = {"msg": "Invalid book details"}
        abort(make_response(response, 400))

    book_exists = bool(
        db.session.query(Book).filter_by(title=title, description=description).first()
    )

    if book_exists:
        response = {"msg": "Book already exists in database."}
        abort(make_response(response, 400))

    return title, description


def validate_book_id(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"msg": f"Book id {book_id} is invalid."}
        abort(make_response(response,400))
    
    query = db.select(Book).where(Book.id == book_id)
    found_book =db.session.scalar(query)


    if not found_book:
        response = {"msg": f"Book {book_id} not found."}
        abort(make_response(response,404))
    
    return found_book