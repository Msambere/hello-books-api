from flask import Blueprint
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