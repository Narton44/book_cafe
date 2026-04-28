from typing import Optional, Any
from dataclasses import dataclass


class Book: # Класс книги
    
    def __init__(self, title: str, author: str, copies: int = 0, price: float = 0):
        self.title = title          # Название книги
        self.author = author        # Автор книги
        self.copies = copies        # Количество экземпляров
        self.price = price          # Цена книги

    def __str__(self):
        return f"Book('{self.title}', '{self.author}', {self.copies})"


class DepartmentCatalog: # Каталог книг отдела на основе кольцевой очереди (массив)

    def __init__(self, max_size: int = 300):
        self.max_size = max_size                    # Максимальный размер очереди
        self._queue = [None] * max_size             # Массив для хранения книг
        self._front = 0                             # Указатель на начало очереди
        self._rear = -1                             # Указатель на конец очереди
        self._size = 0                              # Текущее количество элементов
    
    def is_empty(self) -> bool: # Проверка, пуст ли каталог

        return self._size == 0

    def is_full(self) -> bool: # Проверка, заполнен ли каталог

        return self._size == self.max_size

    def _next_index(self, index: int) -> int: #  Вычисление следующего индекса с учетом кольцевой структуры

        return (index + 1) % self.max_size

    def add_book(self, book: Book) -> bool: #  Добавление книги в каталог. Если книга уже есть - увеличивает количество экземпляров. Возвращает True в случае успеха, False - если каталог переполнен

        if self.is_full():
            return False
        
        # Поиск существующей книги
        idx = self._front
        for _ in range(self._size):
            current_book = self._queue[idx]
            if current_book.title == book.title and current_book.author == book.author:
                # Книга найдена - увеличиваем количество
                current_book.copies += book.copies
                # Обновляем цену, если она изменилась
                if current_book.price != book.price:
                    current_book.price = book.price
                return True
            idx = self._next_index(idx)
        
        # Книга не найдена - добавляем новую
        self._rear = self._next_index(self._rear)
        self._queue[self._rear] = book
        self._size += 1
        return True

    def remove_book(self, title: str, author: str) -> bool: # Удаление книги из каталога. Возвращает True, если книга была удалена

        if self.is_empty():
            return False
        
        # Создаем временный каталог
        temp_catalog = DepartmentCatalog(self.max_size)
        found = False
        
        # Перемещаем все книги, кроме удаляемой, во временный каталог
        idx = self._front
        for _ in range(self._size):
            book = self._queue[idx]
            if book.title == title and book.author == author:
                found = True  # Пропускаем эту книгу
            else:
                temp_catalog.add_book(book)
            idx = self._next_index(idx)
        
        if found:
            # Копируем данные из временного каталога
            self._queue = temp_catalog._queue
            self._front = temp_catalog._front
            self._rear = temp_catalog._rear
            self._size = temp_catalog._size
            return True
        
        return False

    def find_book(self, title: str, author: str) -> Optional[Book]: # Поиск книги по названию и автору. Возвращает книгу или None, если не найдена

        if self.is_empty():
            return None
        
        idx = self._front
        for _ in range(self._size):
            book = self._queue[idx]
            if book.title == title and book.author == author:
                return book
            idx = self._next_index(idx)
        return None

    def update_copies(self, title: str, author: str, delta: int) -> bool: # Обновление количества экземпляров книги (положительное или отрицательное изменение).Возвращает True в случае успеха

        book = self.find_book(title, author)
        if not book:
            return False
        
        new_copies = book.copies + delta
        if new_copies < 0:
            return False
        
        if new_copies == 0:
            return self.remove_book(title, author)
        else:
            book.copies = new_copies
            return True

    def get_all_books(self) -> list: # Получение всех книг из каталога

        if self.is_empty():
            return []
        
        books = []
        idx = self._front
        for _ in range(self._size):
            books.append(self._queue[idx])
            idx = self._next_index(idx)
        return books

    def get_total_titles(self) -> int: # Получение количества уникальных наименований книг

        return self._size

    def get_total_copies(self) -> int: # Получение суммарного количества экземпляров всех книг

        total = 0
        idx = self._front
        for _ in range(self._size):
            total += self._queue[idx].copies
            idx = self._next_index(idx)
        return total


class Department: # Класс, представляющий тематический отдел книжного магазина

    def __init__(self, name: str, max_books: int = 100):
        self.name = name                             # Название отдела (уникальное)
        self.catalog = DepartmentCatalog(max_books)  # Каталог книг отдела
        self.next = None                             # Ссылка на следующий отдел (для списка)

    def purchase_book(self, title: str, author: str, copies: int, price: float = 0) -> bool: #  Закупка книги в отдел. Если книга существует - увеличивает количество, иначе добавляет новую. Возвращает True в случае успеха

        if copies <= 0:
            return False
        
        book = Book(title, author, copies, price)
        return self.catalog.add_book(book)

    def sell_book(self, title: str, author: str, copies: int) -> bool: # Продажа книги из отдела. Возвращает True в случае успеха

        if copies <= 0:
            return False
        
        return self.catalog.update_copies(title, author, -copies)

    def get_total_titles(self) -> int: # Получение суммарного числа наименований книг в отделе

        return self.catalog.get_total_titles()

    def get_total_copies(self) -> int: # Получение суммарного числа экземпляров книг в отделе

        return self.catalog.get_total_copies()

    def get_all_books(self) -> list: # Получение списка всех книг в отделе

        return self.catalog.get_all_books()

    def find_book(self, title: str, author: str) -> Optional[Book]: # Поиск книги в отделе

        return self.catalog.find_book(title, author)


class CircularLinkedList: # Кольцевой однонаправленный список с заголовком для хранения отделов

    def __init__(self):
        self._head = None      # Заголовок списка (первый элемент)
        self._size = 0         # Количество отделов в списке
    
    def is_empty(self) -> bool: # Проверка, пуст ли список

        return self._head is None
    
    def add_department(self, name: str, max_books: int = 100) -> bool: # Добавление нового отдела в список. Название отдела должно быть уникальным. Возвращает True в случае успеха

        # Проверка на уникальность названия
        if self.find_department(name) is not None:
            return False
        
        new_dept = Department(name, max_books)
        
        if self.is_empty():
            # Пустой список - новый элемент замыкается сам на себя
            self._head = new_dept
            new_dept.next = new_dept
        else:
            # Поиск последнего элемента
            last = self._head
            while last.next != self._head:
                last = last.next
            
            # Вставка в конец
            last.next = new_dept
            new_dept.next = self._head
        
        self._size += 1
        return True
    
    def remove_department(self, name: str) -> bool: # Удаление отдела из списка по названию. Возвращает True в случае успеха

        if self.is_empty():
            return False
        
        # Если удаляем единственный элемент
        if self._head.name == name and self._head.next == self._head:
            self._head = None
            self._size = 0
            return True
        
        # Поиск удаляемого элемента и предыдущего
        prev = None
        current = self._head
        
        while True:
            if current.name == name:
                if prev is not None:
                    prev.next = current.next
                    if current == self._head:
                        self._head = current.next
                else:
                    # Удаляем голову
                    last = self._head
                    while last.next != self._head:
                        last = last.next
                    self._head = current.next
                    last.next = self._head
                
                self._size -= 1
                return True
            
            prev = current
            current = current.next
            if current == self._head:
                break
        
        return False
    
    def find_department(self, name: str) -> Optional[Department]: # Поиск отдела по названию. Возвращает отдел или None, если не найден

        if self.is_empty():
            return None
        
        current = self._head
        while True:
            if current.name == name:
                return current
            current = current.next
            if current == self._head:
                break
        return None
    
    def get_all_departments(self) -> list: # Получение списка всех отделов

        if self.is_empty():
            return []
        
        departments = []
        current = self._head
        while True:
            departments.append(current)
            current = current.next
            if current == self._head:
                break
        return departments
    
    def get_total_titles(self) -> int: # Суммарное число наименований книг по всем отделам

        total = 0
        for dept in self.get_all_departments():
            total += dept.get_total_titles()
        return total
    
    def get_total_copies(self) -> int: # Суммарное число экземпляров книг по всем отделам

        total = 0
        for dept in self.get_all_departments():
            total += dept.get_total_copies()
        return total
    
    def get_size(self) -> int: # Количество отделов в списке

        return self._size


class BookStore: # Главный класс книжного магазина
    
    def __init__(self):
        self._departments = CircularLinkedList()
    
    def add_department(self, name: str, max_books: int = 100) -> bool: # Добавление нового тематического отдела в магазин. Название должно быть уникальным. Возвращает True в случае успеха

        return self._departments.add_department(name, max_books)
    
    def remove_department(self, name: str) -> bool: # Удаление отдела из магазина по названию. Возвращает True в случае успеха

        return self._departments.remove_department(name)
    
    def purchase_book(self, dept_name: str, title: str, author: str, copies: int, price: float = 0) -> bool: # Закупка книги в указанный отдел. Возвращает True в случае успеха

        dept = self._departments.find_department(dept_name)
        if dept is None:
            return False
        return dept.purchase_book(title, author, copies, price)
    
    def sell_book(self, dept_name: str, title: str, author: str, copies: int) -> bool: # Продажа книги из указанного отдела. Возвращает True в случае успеха

        dept = self._departments.find_department(dept_name)
        if dept is None:
            return False
        return dept.sell_book(title, author, copies)
    
    def get_department_titles(self, dept_name: str) -> int: # Статистика отдела (число изданий)

        dept = self._departments.find_department(dept_name)
        if dept is None:
            return 0
        return dept.get_total_titles()
    
    def get_department_copies(self, dept_name: str) -> int: # Статистика отдела (число экземпляров)

        dept = self._departments.find_department(dept_name)
        if dept is None:
            return 0
        return dept.get_total_copies()
    
    def get_shop_total_titles(self) -> int: # Статистика магазина (число изданий)

        return self._departments.get_total_titles()
    
    def get_shop_total_copies(self) -> int: # Статистика отдела (число экземпляров)

        return self._departments.get_total_copies()
    
    def get_all_departments(self) -> list: # Получение списка всех отделов магазина

        return self._departments.get_all_departments()
    
    def get_department_books(self, dept_name: str) -> list: # Получение списка всех книг в указанном отделе

        dept = self._departments.find_department(dept_name)
        if dept is None:
            return []
        return dept.get_all_books()
    
    def find_book_in_shop(self, title: str, author: str) -> tuple: # Поиск книги по всему магазину. Возвращает кортеж (отдел, книга) или (None, None), если не найдена

        for dept in self.get_all_departments():
            book = dept.find_book(title, author)
            if book is not None:
                return (dept, book)
        return (None, None)