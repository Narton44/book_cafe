# ======================== Главная функция ========================
from command_line_interface import ConsoleApp
from graphical_user_interface import WindowApp
import tkinter as tk


def main():
    print("Выберите режим работы:")
    print("1. Консольное приложение")
    print("2. Оконное приложение (Tkinter)")
    
    choice = input("Ваш выбор (1 или 2): ")
    
    if choice == '1':
        app = ConsoleApp()
        app.run()
    elif choice == '2':
        root = tk.Tk()
        app = WindowApp(root)
        root.mainloop()
    else:
        print("Неверный выбор!")

if __name__ == "__main__":
    main()