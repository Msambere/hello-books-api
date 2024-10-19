from flask import Blueprint, abort, make_response
from app.models.book import books

books_bp= Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.get("")
def get_all_books():
    response_body=[]
    for book in books:
        response_body.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return response_body

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)
    return{
        "id":book.id,
        "title": book.title,
        "description": book.description
    },200


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"msg": f"Book {book_id} is invalid."}
        abort(make_response(response,400))
    for book in books:
        if book.id == book_id:
            return book
    response = {"msg": f"Book {book_id} not found."}
    abort(make_response(response,404))

    