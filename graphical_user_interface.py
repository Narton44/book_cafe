import tkinter as tk
from tkinter import ttk, messagebox
from models import BookStore


class WindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Книжный магазин - Система управления")
        self.root.geometry("900x700")
        
        self.store = BookStore()
        self._init_test_data()
        
        self._create_widgets()
        self._refresh_departments_list()
        self._refresh_stats()
    
    def _init_test_data(self):
        """Инициализация тестовых данных"""
        self.store.add_department("Художественная литература")
        self.store.add_department("Научно-популярная")
        self.store.add_department("Детская литература")
        
        self.store.purchase_book("Художественная литература", "Война и мир", "Л. Толстой", 10)
        self.store.purchase_book("Художественная литература", "Преступление и наказание", "Ф. Достоевский", 8)
        self.store.purchase_book("Научно-популярная", "Краткая история времени", "С. Хокинг", 5)
        self.store.purchase_book("Детская литература", "Маленький принц", "А. де Сент-Экзюпери", 7)
    
    def _create_widgets(self):
        # Создание вкладок
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка управления отделами
        dept_frame = ttk.Frame(notebook)
        notebook.add(dept_frame, text="Управление отделами")
        self._create_dept_management(dept_frame)
        
        # Вкладка операций с книгами
        book_frame = ttk.Frame(notebook)
        notebook.add(book_frame, text="Операции с книгами")
        self._create_book_operations(book_frame)
        
        # Вкладка статистики
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Статистика")
        self._create_stats_view(stats_frame)
    
    def _create_dept_management(self, parent):
        # Добавление отдела
        add_frame = ttk.LabelFrame(parent, text="Добавить отдел", padding=10)
        add_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(add_frame, text="Название отдела:").pack(side='left', padx=5)
        self.dept_name_entry = ttk.Entry(add_frame, width=30)
        self.dept_name_entry.pack(side='left', padx=5)
        ttk.Button(add_frame, text="Добавить", command=self._add_department).pack(side='left', padx=5)
        
        # Удаление отдела
        remove_frame = ttk.LabelFrame(parent, text="Удалить отдел", padding=10)
        remove_frame.pack(fill='x', padx=10, pady=5)
        
        self.dept_remove_combo = ttk.Combobox(remove_frame, width=30)
        self.dept_remove_combo.pack(side='left', padx=5)
        ttk.Button(remove_frame, text="Удалить", command=self._remove_department).pack(side='left', padx=5)
        
        # Список отделов
        list_frame = ttk.LabelFrame(parent, text="Список отделов", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.depts_listbox = tk.Listbox(list_frame, height=10)
        self.depts_listbox.pack(fill='both', expand=True)
        
        # Кнопка обновления
        ttk.Button(parent, text="Обновить список", command=self._refresh_departments_list).pack(pady=10)
    
    def _create_book_operations(self, parent):
        # Выбор отдела
        dept_frame = ttk.LabelFrame(parent, text="Выберите отдел", padding=10)
        dept_frame.pack(fill='x', padx=10, pady=5)
        
        self.book_dept_combo = ttk.Combobox(dept_frame, width=30)
        self.book_dept_combo.pack(side='left', padx=5)
        ttk.Button(dept_frame, text="Обновить", command=self._refresh_book_dept_combo).pack(side='left', padx=5)
        
        # Закупка книги
        purchase_frame = ttk.LabelFrame(parent, text="Закупка книги", padding=10)
        purchase_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(purchase_frame, text="Название:").grid(row=0, column=0, padx=5, pady=2)
        self.purchase_title = ttk.Entry(purchase_frame, width=25)
        self.purchase_title.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(purchase_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=2)
        self.purchase_author = ttk.Entry(purchase_frame, width=25)
        self.purchase_author.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(purchase_frame, text="Кол-во:").grid(row=2, column=0, padx=5, pady=2)
        self.purchase_copies = ttk.Entry(purchase_frame, width=10)
        self.purchase_copies.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Button(purchase_frame, text="Закупить", command=self._purchase_book).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Продажа книги
        sell_frame = ttk.LabelFrame(parent, text="Продажа книги", padding=10)
        sell_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(sell_frame, text="Название:").grid(row=0, column=0, padx=5, pady=2)
        self.sell_title = ttk.Entry(sell_frame, width=25)
        self.sell_title.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(sell_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=2)
        self.sell_author = ttk.Entry(sell_frame, width=25)
        self.sell_author.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(sell_frame, text="Кол-во:").grid(row=2, column=0, padx=5, pady=2)
        self.sell_copies = ttk.Entry(sell_frame, width=10)
        self.sell_copies.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Button(sell_frame, text="Продать", command=self._sell_book).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Просмотр книг отдела
        view_frame = ttk.LabelFrame(parent, text="Книги в отделе", padding=10)
        view_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.books_text = tk.Text(view_frame, height=10, width=80)
        self.books_text.pack(fill='both', expand=True)
        
        ttk.Button(view_frame, text="Показать книги", command=self._show_books).pack(pady=5)
    
    def _create_stats_view(self, parent):
        # Статистика по отделам
        dept_stats_frame = ttk.LabelFrame(parent, text="Статистика по отделам", padding=10)
        dept_stats_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.dept_stats_combo = ttk.Combobox(dept_stats_frame, width=30)
        self.dept_stats_combo.pack(pady=5)
        ttk.Button(dept_stats_frame, text="Показать статистику отдела", command=self._show_dept_stats).pack(pady=5)
        
        self.dept_stats_label = ttk.Label(dept_stats_frame, text="", font=("Arial", 10))
        self.dept_stats_label.pack(pady=10)
        
        # Статистика по магазину
        shop_stats_frame = ttk.LabelFrame(parent, text="Статистика магазина в целом", padding=10)
        shop_stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.shop_stats_label = ttk.Label(shop_stats_frame, text="", font=("Arial", 12, "bold"))
        self.shop_stats_label.pack(pady=10)
        
        ttk.Button(parent, text="Обновить всю статистику", command=self._refresh_stats).pack(pady=10)
    
    def _refresh_departments_list(self):
        self.depts_listbox.delete(0, tk.END)
        depts = self.store.get_all_departments()
        for dept in depts:
            self.depts_listbox.insert(tk.END, f"{dept.name} (наименований: {dept.get_total_titles()}, экз.: {dept.get_total_copies()})")
        
        # Обновляем комбобоксы
        dept_names = [dept.name for dept in depts]
        self.dept_remove_combo['values'] = dept_names
        self.book_dept_combo['values'] = dept_names
        self.dept_stats_combo['values'] = dept_names
    
    def _refresh_book_dept_combo(self):
        depts = self.store.get_all_departments()
        dept_names = [dept.name for dept in depts]
        self.book_dept_combo['values'] = dept_names
    
    def _refresh_stats(self):
        titles = self.store.get_shop_total_titles()
        copies = self.store.get_shop_total_copies()
        self.shop_stats_label.config(text=f"Всего наименований: {titles} | Всего экземпляров: {copies}")
        
        self._refresh_departments_list()
    
    def _add_department(self):
        name = self.dept_name_entry.get().strip()
        if name:
            if self.store.add_department(name):
                messagebox.showinfo("Успех", f"Отдел '{name}' добавлен!")
                self.dept_name_entry.delete(0, tk.END)
                self._refresh_departments_list()
                self._refresh_stats()
            else:
                messagebox.showerror("Ошибка", "Отдел с таким названием уже существует!")
        else:
            messagebox.showwarning("Предупреждение", "Введите название отдела!")
    
    def _remove_department(self):
        name = self.dept_remove_combo.get()
        if name:
            if self.store.remove_department(name):
                messagebox.showinfo("Успех", f"Отдел '{name}' удален!")
                self._refresh_departments_list()
                self._refresh_stats()
            else:
                messagebox.showerror("Ошибка", "Отдел не найден!")
    
    def _purchase_book(self):
        dept = self.book_dept_combo.get()
        title = self.purchase_title.get().strip()
        author = self.purchase_author.get().strip()
        
        try:
            copies = int(self.purchase_copies.get())
            if copies <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Предупреждение", "Введите корректное количество экземпляров!")
            return
        
        if dept and title and author:
            if self.store.purchase_book(dept, title, author, copies):
                messagebox.showinfo("Успех", "Книга успешно закуплена!")
                self.purchase_title.delete(0, tk.END)
                self.purchase_author.delete(0, tk.END)
                self.purchase_copies.delete(0, tk.END)
                self._refresh_departments_list()
                self._refresh_stats()
                self._show_books()
            else:
                messagebox.showerror("Ошибка", "Не удалось закупить книгу! Возможно, отдел не найден или превышена емкость каталога.")
        else:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
    
    def _sell_book(self):
        dept = self.book_dept_combo.get()
        title = self.sell_title.get().strip()
        author = self.sell_author.get().strip()
        
        try:
            copies = int(self.sell_copies.get())
            if copies <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Предупреждение", "Введите корректное количество экземпляров!")
            return
        
        if dept and title and author:
            if self.store.sell_book(dept, title, author, copies):
                messagebox.showinfo("Успех", "Книга успешно продана!")
                self.sell_title.delete(0, tk.END)
                self.sell_author.delete(0, tk.END)
                self.sell_copies.delete(0, tk.END)
                self._refresh_departments_list()
                self._refresh_stats()
                self._show_books()
            else:
                messagebox.showerror("Ошибка", "Не удалось продать книгу! Возможно, книги нет в наличии или недостаточно экземпляров.")
        else:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
    
    def _show_books(self):
        dept = self.book_dept_combo.get()
        if dept:
            books = self.store.get_department_books(dept)
            self.books_text.delete(1.0, tk.END)
            if books:
                self.books_text.insert(1.0, f"Книги в отделе '{dept}':\n\n")
                for i, book in enumerate(books, 1):
                    self.books_text.insert(tk.END, f"{i}. {book}\n")
            else:
                self.books_text.insert(1.0, f"В отделе '{dept}' нет книг!")
    
    def _show_dept_stats(self):
        dept = self.dept_stats_combo.get()
        if dept:
            titles, copies = self.store.get_department_stats(dept)
            self.dept_stats_label.config(text=f"Отдел '{dept}':\nНаименований: {titles}\nЭкземпляров: {copies}")
