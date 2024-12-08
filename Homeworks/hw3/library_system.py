class InvalidISBNException(Exception):
    """Exception raised for errors in the input ISBN."""

class Book:
    def init (self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

def add_book(library, book):
    if not isinstance(book.isbn, str) or len(book.isbn) != 13 or not book.isbn.isdigit():
        raise InvalidISBNException(f"Invalid ISBN: {book.isbn}")
    library[book.isbn] = book
