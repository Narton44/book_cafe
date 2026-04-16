class Book:

    def __init__(self, title: str, author: str, copies: int, price: float):
        self.title = title
        self.author = author
        self.copies = copies
        self.price = price

    def __str__(self):
        return f"Book('{self.title}', '{self.author}', {self.copies})"

class DepartmentCatalog:
    
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
    

class Department:

    def __init__(self, name: str, max_books: int = 100):
        pass 