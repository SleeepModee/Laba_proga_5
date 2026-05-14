import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

# --- НАСТРОЙКИ ТЁМНОЙ ТЕМЫ ---
BG_COLOR = "#2b2b2b"      
BTN_COLOR = "#3c3f41"     
TEXT_COLOR = "#a9b7c6"    
FG_COLOR = "#ffffff"      

# --- ФУНКЦИИ КНОПОК ---

def run_generation():
    messagebox.showinfo("Генерация", "Сейчас начнется генерация файла. Это займет пару минут.")
    try:
        subprocess.run(["python", "Generation.py"], check=True)
        messagebox.showinfo("Успех", "Генерация 1 ГБ файла завершена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить генерацию:\n{e}")

def run_cpp_sort():
    key = sort_var.get()
    messagebox.showinfo("C++ Сортировка", f"Запускаем C++ (Сортировка по: {key}). Ждите...")
    try:
        # Запускаем экзешник и передаем ему выбранный ключ сортировки
        subprocess.run(["sort.exe", key], check=True) 
        messagebox.showinfo("Успех", "C++ сортировка завершена! Файл: sorted_cpp.csv")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить sort.exe. Вы скомпилировали код?\n{e}")

def run_py_sort():
    key = sort_var.get()
    messagebox.showinfo("Python Сортировка", f"Запускаем Python (Сортировка по: {key}). Ждите...")
    try:
        # Запускаем питон и передаем ему выбранный ключ сортировки
        subprocess.run(["python", "sort.py", key], check=True)
        messagebox.showinfo("Успех", "Python сортировка завершена! Файл: sorted_python.csv")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить sort.py:\n{e}")

def view_file():
    filepath = filedialog.askopenfilename(title="Выберите файл для проверки", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if not filepath:
        return

    text_area.delete(1.0, tk.END) 
    text_area.insert(tk.END, f"--- Открыт файл: {os.path.basename(filepath)} ---\n\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i in range(20): # Читаем только верхушку файла для безопасности
                line = f.readline()
                if not line:
                    break
                text_area.insert(tk.END, line)
    except Exception as e:
        text_area.insert(tk.END, f"Ошибка чтения файла: {e}")

# --- СОЗДАНИЕ ИНТЕРФЕЙСА ---
root = tk.Tk()
root.title("Внешняя сортировка (Big Data)")
root.geometry("600x600")
root.configure(bg=BG_COLOR)

title_label = tk.Label(root, text="Панель управления сортировкой", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=FG_COLOR)
title_label.pack(pady=15)

# --- ПАНЕЛЬ ВЫБОРА КЛЮЧА ---
sort_var = tk.StringVar(value="level") 

sort_frame = tk.Frame(root, bg=BG_COLOR)
sort_frame.pack(pady=10)

tk.Label(sort_frame, text="Ключ сортировки:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(sort_frame, text="Уровень", variable=sort_var, value="level", bg=BG_COLOR, fg="black", selectcolor=TEXT_COLOR).pack(side=tk.LEFT)
tk.Radiobutton(sort_frame, text="Имя", variable=sort_var, value="name", bg=BG_COLOR, fg="black", selectcolor=TEXT_COLOR).pack(side=tk.LEFT)
tk.Radiobutton(sort_frame, text="Винрейт", variable=sort_var, value="winrate", bg=BG_COLOR, fg="black", selectcolor=TEXT_COLOR).pack(side=tk.LEFT)

# --- КНОПКИ ДЕЙСТВИЙ ---
btn_gen = tk.Button(root, text="1. Сгенерировать data.csv (Python)", font=("Arial", 12), bg=BTN_COLOR, fg=FG_COLOR, command=run_generation)
btn_gen.pack(pady=5, fill=tk.X, padx=50)

btn_cpp = tk.Button(root, text="2. Запустить сортировку C++", font=("Arial", 12), bg=BTN_COLOR, fg=FG_COLOR, command=run_cpp_sort)
btn_cpp.pack(pady=5, fill=tk.X, padx=50)

btn_py = tk.Button(root, text="3. Запустить сортировку Python", font=("Arial", 12), bg=BTN_COLOR, fg=FG_COLOR, command=run_py_sort)
btn_py.pack(pady=5, fill=tk.X, padx=50)

btn_view = tk.Button(root, text="4. Посмотреть результат (Проверка)", font=("Arial", 12), bg="#4a6e4d", fg=FG_COLOR, command=view_file)
btn_view.pack(pady=15, fill=tk.X, padx=50)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=12, font=("Consolas", 10), bg="#1e1e1e", fg=TEXT_COLOR)
text_area.pack(pady=10, padx=20)

root.mainloop()