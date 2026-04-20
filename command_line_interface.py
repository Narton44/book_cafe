# ======================== Консольное приложение ========================
from ready import BookStore

class ConsoleApp:
    def __init__(self):
        self.store = BookStore()
    
    def run(self):
        print("\n" + "="*60)
        print("КНИЖНЫЙ МАГАЗИН - Консольное приложение")
        print("="*60)
        
        # Добавляем тестовые данные
        self._init_test_data()
        
        while True:
            print("\nМЕНЮ:")
            print("1. Добавить отдел")
            print("2. Удалить отдел")
            print("3. Закупка книги")
            print("4. Продажа книги")
            print("5. Статистика отдела")
            print("6. Статистика магазина")
            print("7. Список всех отделов")
            print("8. Список книг в отделе")
            print("0. Выход")
            
            choice = input("\nВыберите действие: ")
            
            if choice == '0':
                print("До свидания!")
                break
            elif choice == '1':
                self._add_department()
            elif choice == '2':
                self._remove_department()
            elif choice == '3':
                self._purchase_book()
            elif choice == '4':
                self._sell_book()
            elif choice == '5':
                self._show_dept_stats()
            elif choice == '6':
                self._show_shop_stats()
            elif choice == '7':
                self._list_departments()
            elif choice == '8':
                self._list_books_in_dept()
            else:
                print("Неверный выбор!")
    
    def _init_test_data(self):
        """Инициализация тестовых данных"""
        self.store.add_department("Художественная литература")
        self.store.add_department("Научно-популярная")
        self.store.add_department("Детская литература")
        
        self.store.purchase_book("Художественная литература", "Война и мир", "Л. Толстой", 10)
        self.store.purchase_book("Художественная литература", "Преступление и наказание", "Ф. Достоевский", 8)
        self.store.purchase_book("Научно-популярная", "Краткая история времени", "С. Хокинг", 5)
        self.store.purchase_book("Детская литература", "Маленький принц", "А. де Сент-Экзюпери", 7)
        
        print("\nТестовые данные добавлены!")
    
    def _add_department(self):
        name = input("Название отдела: ")
        if self.store.add_department(name):
            print(f"Отдел '{name}' успешно добавлен!")
        else:
            print("Отдел с таким названием уже существует!")
    
    def _remove_department(self):
        name = input("Название отдела для удаления: ")
        if self.store.remove_department(name):
            print(f"Отдел '{name}' успешно удален!")
        else:
            print("Отдел не найден!")
    
    def _purchase_book(self):
        dept = input("Название отдела: ")
        title = input("Название книги: ")
        author = input("Автор: ")
        copies = int(input("Количество экземпляров: "))
        
        if self.store.purchase_book(dept, title, author, copies):
            print("Книга успешно закуплена!")
        else:
            print("Ошибка закупки! Возможно, отдел не найден или превышена емкость каталога.")
    
    def _sell_book(self):
        dept = input("Название отдела: ")
        title = input("Название книги: ")
        author = input("Автор: ")
        copies = int(input("Количество экземпляров: "))
        
        if self.store.sell_book(dept, title, author, copies):
            print("Книга успешно продана!")
        else:
            print("Ошибка продажи! Возможно, книги нет в наличии или недостаточно экземпляров.")
    
    def _show_dept_stats(self):
        dept = input("Название отдела: ")
        titles, copies = self.store.get_department_stats(dept)
        print(f"\nСтатистика отдела '{dept}':")
        print(f"  - Число наименований: {titles}")
        print(f"  - Число экземпляров: {copies}")
    
    def _show_shop_stats(self):
        titles, copies = self.store.get_shop_stats()
        print(f"\nСтатистика магазина в целом:")
        print(f"  - Число наименований: {titles}")
        print(f"  - Число экземпляров: {copies}")
    
    def _list_departments(self):
        depts = self.store.get_all_departments()
        if not depts:
            print("Нет отделов!")
        else:
            print("\nСписок отделов:")
            for i, dept in enumerate(depts, 1):
                print(f"  {i}. {dept.name}")
    
    def _list_books_in_dept(self):
        dept = input("Название отдела: ")
        books = self.store.get_department_books(dept)
        if not books:
            print(f"В отделе '{dept}' нет книг или отдел не найден!")
        else:
            print(f"\nКниги в отделе '{dept}':")
            for i, book in enumerate(books, 1):
                print(f"  {i}. {book}")