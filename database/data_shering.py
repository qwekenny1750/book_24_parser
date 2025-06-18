from database.requests import add_book

class DataBase_exchanging:
    def __init__(self, name, author, rating, publisher, publication_year, isbn):
        self.name = name
        self.author = author
        self.rating = rating
        self.publisher = publisher
        self.publication_year = publication_year
        self.isbn = isbn

    def exchanging(self):
        add_book(self.name, self.author, self.rating, self.publisher, self.publication_year, self.isbn)
