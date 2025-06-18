from sqlalchemy import select
from database.models import Books
from database.models import session

def add_book(name, author, rating, publisher, publication_year, isbn):
    book = session.scalar(select(Books).where(
        Books.name==name,
        Books.author==author,
        Books.rating==rating,
        Books.publisher==publisher,
        Books.publication_year==publication_year,
        Books.isbn==isbn
        ))
    if not book:
        book_info = Books(
            name=name,
            author=author,
            rating=rating,
            publisher=publisher,
            publication_year=publication_year,
            isbn=isbn
        )
        session.add(book_info)
        session.commit()