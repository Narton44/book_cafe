class Book:

    def __init__(self, title: str, author: str, quantity: int=0, price: float=0):
        self.title = title
        self.author = author
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Book('{self.title}', '{self.author}', {self.quantity})"

class DepartmentCatalog: # Каталог книг отдела, кольцевая очередь на основе обычного массива

    def __init__(self, max_size: int=300):
        self.max_size = max_size
        self.books = [None] * max_size # Массив для хранения книг
        self.front = 0 # Указатель на начало очереди
        self.rear = -1 # Указатель на конец очереди
        self.size = 0 # Текущее количество книг

    def is_full(self):
        return self.size == self.max_size

    def is_empty(self):
        return self.size == 0
    
    def _next_index(self, index: int) -> int:
        """Вычисляет следующий индекс с учётом кольцевой структуры."""
        return (index + 1) % self.max_size

    def add_book(self, book: Book):
        """Добавляет книгу в каталог. Если книга уже есть — увеличивает количество."""

        if self.is_full():
            raise OverflowError("Каталог переполнен")

        for i in range(self.size):
            current_index = (self.front + i) % self.max_size
            if self.books[current_index].title == book.title and self.books[current_index].author == book.author:
                self.books[current_index].quantity += book.quantity
                return True
            
        self.rear = self._next_index(self.rear) # последний индекс увеличивается на единицу, т.е. список увеличивается на 1 элемент
        self.books[self.rear] = book # в конец списка книг (под только что добавленным индексом) помещается новая книга 
        self.size += 1 # размер списка увеличивается на единицу
    

    def sell_book(self, book:Book):
        pass



class Department: # Отделы, адресный замкнутый (кольцевой) неупорядоченный однонаправленный список с заголовком


    def __init__(self, name: str, max_books: int = 100):
        pass 