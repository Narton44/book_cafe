from command_line_interface import ConsoleApp
from graphical_user_interface import WindowApp
import tkinter as tk


def main():
    """
    Основная функция программы, предоставляющая выбор режима работы:
    консольное приложение или оконное приложение (Tkinter)(02.00).
    Запрашивает ввод до тех пор, пока пользователь не выберет корректный вариант.
    """
    print("Выберите режим работы:\n0 - Выход из программы\n1 - Консольное приложение\n2 - Оконное приложение (Tkinter)")
    
    while True:
        try:
            choice = input("Выберите 0, 1 или 2: ")
            if choice == '0':
                print("До скорого!")
                return
            elif choice == '1':
                app = ConsoleApp()
                app.run()
                break
            elif choice == '2':
                root = tk.Tk()
                app = WindowApp(root)
                root.mainloop()
                break
            else:
                print("Неверный выбор, выберите 0, 1 или 2!")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            break

if __name__ == "__main__":
    main()