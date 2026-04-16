class Book:

    def __init__(self, title: str, author: str, quantity: int, price: float):
        self.title = title
        self.author = author
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Book('{self.title}', '{self.author}', {self.copies})"

class DepartmentCatalog: # Каталог книг отдела, кольцевая очередь на основе обычного массива

    def __init__(self, max_size=100):
        self.max_size = max_size
        self.books = [None] * max_size
        self.front = 0
        self.rear = -1
        self.size = 0

    def is_full(self):
        return self.size == self.max_size

    def is_empty(self):
        return self.size == 0

    def add_book(self, book):

        if self.is_full():
            raise OverflowError("Каталог переполнен")

        for i in range(self.size):
            idx = (self.front + i) % self.max_size
            if self.books[idx].title == book.title and self.books[idx].author == book.author:
                self.books[idx].quantity += book.quantity
                return
            
        self.rear = (self.rear + 1) % self.max_size
        self.books[self.rear] = book
        self.size += 1
    
    def sell_book(self, book):












class Department: # Отделы, адресный замкнутый (кольцевой) неупорядоченный однонаправленный список с заголовком


    def __init__(self, name: str, max_books: int = 100):
        pass 