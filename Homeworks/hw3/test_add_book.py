import unittest
from library_system import Book, add_book, InvalidISBNException

class SyntaxErrorException(Exception):
    """Exception raised for Syntax errors in the input ISBN."""

class TestAddBook(unittest.TestCase):
    def setUp(self) -> None:
        self.library = {}
        super().setUp()
    
    def test_invalid_length_1(self):
        """Test case 1 for ISBN with invalid length, i.e. length != 13."""
        book = Book()
        book.init("TestBook", "San Zhang", "97873021")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
    
    def test_invalid_length_2(self):
        """Test case 2 for ISBN with invalid length, i.e. length != 13."""
        book = Book()
        book.init("TestBook", "San Zhang", "9787302122609123")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)

    def test_non_digit_1(self):
        """Test case 1 for ISBN with non-digit characters."""
        book = Book()
        book.init("TestBook", "San Zhang", "9787302A22609")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
    
    def test_non_digit_2(self):
        """Test case 2 for ISBN with non-digit characters."""
        book = Book()
        book.init("TestBook", "San Zhang", "9787302 22609")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)

    def test_non_string_type_1(self):
        """Test case 1 for ISBN with non-string type."""
        book = Book()
        book.init("TestBook", "San Zhang", 9787302122609)
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
    
    def test_non_string_type_2(self):
        """Test case 2 for ISBN with non-string type."""
        book = Book()
        book.init("TestBook", "San Zhang", int("6457372123610"))
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
    
    def test_invalid_length_non_digit_1(self):
        """Test case 1 for ISBN with invalid length and non-digit characters."""
        book = Book()
        book.init("TestBook", "San Zhang", "9787302B22603c4")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
    
    def test_invalid_length_non_digit_2(self):
        """Test case 2 for ISBN with invalid length and non-digit characters."""
        book = Book()
        book.init("TestBook", "San Zhang", "9-87302 22")
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)

    def test_invalid_length_non_string_type_1(self):
        """Test case 1 for ISBN with invalid length and non-string type."""
        book = Book()
        book.init("TestBook", "San Zhang", 9787302122)
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
    
    def test_invalid_length_non_string_type_2(self):
        """Test case 2 for ISBN with invalid length and non-string type."""
        book = Book()
        book.init("TestBook", "San Zhang", int("978730212260907"))
        with self.assertRaises(InvalidISBNException):
            add_book(self.library, book)
    
    def test_non_string_type_non_digit_1(self):
        """Test case 1 for ISBN with non-string type and non-digit characters."""
        """Here I consider 9787212261123 as the ISBN code."""
        book = Book()
        try:
            book.init("TestBook", "San Zhang", 978721226+"1"+123)
        except:
            try:
                add_book(self.library, book)
            except:
                self.assertRaises(InvalidISBNException)
    
    def test_non_string_type_non_digit_2(self):
        """Test case 2 for ISBN with non-string type and non-digit characters."""
        """Here I consider 9787212241123 as the ISBN code."""
        book = Book()
        try:
            book.init("TestBook", "San Zhang", int("97872122")+"41"+123)
        except:
            try:
                add_book(self.library, book)
            except:
                self.assertRaises(InvalidISBNException)

    
    def test_all_invalid_1(self):
        """Test case 1 for ISBN with invalid length, non-string type and non-digit characters."""
        """Here I consider 978730212a31276 as the ISBN code."""
        book = Book()
        try:
            book.init("TestBook", "San Zhang", 978730212 + 'a' + 31276)
        except:
            try:
                add_book(self.library, book)
            except:
                self.assertRaises(InvalidISBNException)
    
    def test_all_invalid_2(self):
        """Test case for ISBN with invalid length, non-string type and non-digit characters."""
        """Here I consider 97812 33 as the ISBN code."""
        book = Book()
        try:
            book.init("TestBook", "San Zhang", int("978") + '12 3' + 3)
        except:
            try:
                add_book(self.library, book)
            except:
                self.assertRaises(InvalidISBNException)
                
    def test_valid_isbn(self):  
        """Test case for valid ISBN. The function should not consider a valid ISBN as invalid."""
        book = Book()
        book.init("TestBook", "San Zhang", "9787302122609")
        add_book(self.library, book)
        self.assertIn(book.isbn, self.library)


if __name__ == '__main__':
    unittest.main()
