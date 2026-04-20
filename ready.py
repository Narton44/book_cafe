
from dataclasses import dataclass
from typing import Optional, Any


class Book:

    def __init__(self, title: str, author: str, quantity: int=0, price: float=0):
        self.title = title
        self.author = author
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Book('{self.title}', '{self.author}', {self.quantity})"

class DepartmentCatalog: # Каталог книг отдела, кольцевая очередь (Queue) на основе обычного массива

    def __init__(self, max_size: int=300):
        self.max_size = max_size
        self.books = [None] * max_size # Массив для хранения книг
        self.front = 0 # Указатель (индекс) на начало очереди
        self.rear = -1 # Указатель (индекс) на конец очереди
        self.size = 0 # Текущее количество книг

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size == self.max_size

    def _next_index(self, index) -> int: # """Вычисляет следующий индекс для данного index с учётом кольцевой структуры."""
        return (index  + 1) % self.max_size

    def add_book(self, book: Book):# """Добавляет книгу в каталог. Если книга уже есть — увеличивает количество."""
        
        if self.is_full():
            raise IndexError("Каталог переполнен")

        for i in range(self.size):
            current_index = (self.front + i) % self.max_size
            if self.books[current_index].title == book.title and self.books[current_index].author == book.author:
                self.books[current_index].quantity += book.quantity
                if self.books[current_index].price != book.price:
                    self.books[current_index].price = book.price
                return True
            
        self.rear = self._next_index(self.rear) # последний индекс увеличивается на единицу, т.е. список увеличивается на 1 элемент
        self.books[self.rear] = book # в конец списка книг (под только что добавленным индексом) помещается новая книга 
        self.size += 1 # размер списка увеличивается на единицу

    def sell_book(self) -> Optional[Book]: # """Удаление книги из очереди"""
        if self.is_empty():
            raise IndexError("Каталог итак пуст")
        book = self.books[self.front]
        self.books[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return book

    def peek(self) -> Optional[Book]:
        """Просмотр первого элемента без удаления"""
        if self.is_empty():
            return None
        return self.queue[self.front]

    def find_book(self, title: str, author: str) -> Optional[Book]:
        """Поиск книги по названию и автору"""
        if self.is_empty():
            return None

        idx = self.front
        for _ in range(self.size):
            book = self.queue[idx]
            if book.title == title and book.author == author:
                return book
            idx = (idx + 1) % self.capacity
        return None

    def get_all_books(self) -> list:
        """Получение всех книг в очереди"""
        books = []
        if self.is_empty():
            return books

        idx = self.front
        for _ in range(self.size):
            books.append(self.queue[idx])
            idx = (idx + 1) % self.capacity
        return books

    def get_total_titles(self) -> int:
        """Количество уникальных наименований книг"""
        return self.size

    def get_total_copies(self) -> int:
        """Суммарное количество экземпляров"""
        total = 0
        idx = self.front
        for _ in range(self.size):
            total += self.queue[idx].copies
            idx = (idx + 1) % self.capacity
        return total

    def update_copies(self, title: str, author: str, delta: int) -> bool:
        """Обновление количества экземпляров книги"""
        book = self.find_book(title, author)
        if book:
            new_copies = book.copies + delta
            if new_copies < 0:
                return False
            if new_copies == 0:
                self.remove_book(title, author)
            else:
                book.copies = new_copies
            return True
        return False

    def remove_book(self, title: str, author: str) -> bool:
        """Удаление книги из очереди"""
        if self.is_empty():
            return False
        
        temp_queue = CircularQueue(self.capacity)
        found = False

        idx = self.front
        for _ in range(self.size):
            book = self.queue[idx]
            if book.title == title and book.author == author:
                found = True
                idx = (idx + 1) % self.capacity
                continue
            temp_queue.enqueue(book)
            idx = (idx + 1) % self.capacity

        if found:
            self.queue = temp_queue.queue
            self.front = temp_queue.front
            self.rear = temp_queue.rear
            self.size = temp_queue.size
            return True
        return False


# ======================== Класс отдела ========================
class Department:
    """Класс, представляющий отдел книжного магазина"""
    
    def __init__(self, name: str, max_books: int = 100):
        self.name = name
        self.catalog = CircularQueue(max_books)
        self.next = None  # Для связного списка
    
    def purchase_book(self, title: str, author: str, copies: int) -> bool:
        """Закупка книги (увеличение количества или добавление новой)"""
        if copies <= 0:
            return False
        
        book = self.catalog.find_book(title, author)
        if book:
            book.copies += copies
        else:
            new_book = Book(title, author, copies)
            if not self.catalog.enqueue(new_book):
                return False
        return True
    
    def sell_book(self, title: str, author: str, copies: int) -> bool:
        """Продажа книги (уменьшение количества)"""
        if copies <= 0:
            return False
        
        book = self.catalog.find_book(title, author)
        if not book or book.copies < copies:
            return False
        
        if book.copies == copies:
            return self.catalog.remove_book(title, author)
        else:
            book.copies -= copies
            return True
    
    def get_total_titles(self) -> int:
        """Суммарное число наименований книг в отделе"""
        return self.catalog.get_total_titles()
    
    def get_total_copies(self) -> int:
        """Суммарное число экземпляров в отделе"""
        return self.catalog.get_total_copies()
    
    def get_all_books(self) -> list:
        """Получение всех книг отдела"""
        return self.catalog.get_all_books()


# ======================== Кольцевой однонаправленный список отделов ========================
class CircularLinkedList:
    """Кольцевой однонаправленный список с заголовком для хранения отделов"""
    
    def __init__(self):
        self.head = None
        self.current = None
        self.size = 0
    
    def add_department(self, name: str, max_books: int = 100) -> bool:
        """Добавление нового отдела"""
        # Проверка на уникальность названия
        if self.find_department(name):
            return False
        
        new_dept = Department(name, max_books)
        
        if not self.head:
            self.head = new_dept
            new_dept.next = new_dept  # Замыкаем на себя
        else:
            last = self.head
            while last.next != self.head:
                last = last.next
            last.next = new_dept
            new_dept.next = self.head
        
        self.size += 1
        return True
    
    def find_department(self, name: str) -> Optional[Department]:
        """Поиск отдела по названию"""
        if not self.head:
            return None
        
        current = self.head
        while True:
            if current.name == name:
                return current
            current = current.next
            if current == self.head:
                break
        return None
    
    def remove_department(self, name: str) -> bool:
        """Удаление отдела"""
        if not self.head:
            return False
        
        if self.head.name == name and self.head.next == self.head:
            self.head = None
            self.size = 0
            return True
        
        prev = None
        current = self.head
        
        while True:
            if current.name == name:
                if prev:
                    prev.next = current.next
                    if current == self.head:
                        self.head = current.next
                else:
                    # Удаляем голову
                    last = self.head
                    while last.next != self.head:
                        last = last.next
                    self.head = current.next
                    last.next = self.head
                self.size -= 1
                return True
            
            prev = current
            current = current.next
            if current == self.head:
                break
        return False
    
    def get_all_departments(self) -> list:
        """Получение всех отделов"""
        departments = []
        if not self.head:
            return departments
        
        current = self.head
        while True:
            departments.append(current)
            current = current.next
            if current == self.head:
                break
        return departments
    
    def get_shop_total_titles(self) -> int:
        """Суммарное число наименований книг по всему магазину"""
        total = 0
        for dept in self.get_all_departments():
            total += dept.get_total_titles()
        return total
    
    def get_shop_total_copies(self) -> int:
        """Суммарное число экземпляров по всему магазину"""
        total = 0
        for dept in self.get_all_departments():
            total += dept.get_total_copies()
        return total


# ======================== Класс магазина ========================
class BookStore:
    """Главный класс книжного магазина"""
    
    def __init__(self):
        self.departments = CircularLinkedList()
    
    def add_department(self, name: str, max_books: int = 100) -> bool:
        """Добавление нового отдела"""
        return self.departments.add_department(name, max_books)
    
    def remove_department(self, name: str) -> bool:
        """Удаление отдела"""
        return self.departments.remove_department(name)
    
    def purchase_book(self, dept_name: str, title: str, author: str, copies: int) -> bool:
        """Закупка книги в отдел"""
        dept = self.departments.find_department(dept_name)
        if not dept:
            return False
        return dept.purchase_book(title, author, copies)
    
    def sell_book(self, dept_name: str, title: str, author: str, copies: int) -> bool:
        """Продажа книги из отдела"""
        dept = self.departments.find_department(dept_name)
        if not dept:
            return False
        return dept.sell_book(title, author, copies)
    
    def get_department_stats(self, dept_name: str) -> tuple:
        """Статистика по отделу"""
        dept = self.departments.find_department(dept_name)
        if dept:
            return (dept.get_total_titles(), dept.get_total_copies())
        return (0, 0)
    
    def get_shop_stats(self) -> tuple:
        """Статистика по магазину в целом"""
        return (self.departments.get_shop_total_titles(), 
                self.departments.get_shop_total_copies())
    
    def get_all_departments(self) -> list:
        """Список всех отделов"""
        return self.departments.get_all_departments()
    
    def get_department_books(self, dept_name: str) -> list:
        """Список книг в отделе"""
        dept = self.departments.find_department(dept_name)
        if dept:
            return dept.get_all_books()
        return []
