import tkinter as tk
import random
import json
from tkinter import simpledialog, messagebox
from tkinter.messagebox import showerror, showinfo

# Глобальные переменные
tasks = []
history = []

# Создание окна
window = tk.Tk()
window.title("Random Task Generator")
window.geometry("800x500")

# Label приветствие
welcome_label = tk.Label(window, text="Добро пожаловать в генератор случайных задач!", font=("Arial", 12, "bold"))
welcome_label.pack(pady=10)

# Frame для инструментов добавления
add_frame = tk.Frame(window)
add_frame.place(x=20, y=60)

# Label для добавления задачи
add_label = tk.Label(add_frame, text="Добавление задачи")
add_label.pack()

# Entry для ввода задачи
add_entry = tk.Entry(add_frame, width=25)
add_entry.pack(pady=5)

# Label для выбора категории
choose_label = tk.Label(add_frame, text="Выберите категорию")
choose_label.pack()

# Listbox с категориями
category_lb = tk.Listbox(add_frame, height=4)
category_lb.pack(pady=5)

# Функция загрузки задач из файла
def load_file():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Файл tasks.json повреждён. Используется стандартный набор задач.")
        return []

# Функция сохранения задач в файл
def save_file(tasks_list):
    try:
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(tasks_list, file, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить задачи: {e}")

# Функция загрузки истории
def load_history():
    try:
        with open("history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Файл history.json повреждён. Создаётся новая история.")
        return []

# Функция сохранения истории в файл
def save_history(history_list):
    try:
        # Создаём папку data, если её нет
        import os
        os.makedirs("data", exist_ok=True)
        with open("data/history.json", "w", encoding="utf-8") as file:
            json.dump(history_list, file, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

# Функция добавления новой задачи
def add_task():
    global tasks
    try:
        task = add_entry.get().strip()
        if not task:
            showerror(title="Ошибка", message="Поле для добавления новой задачи пустое")
            return

        category_indx = category_lb.curselection()
        if not category_indx:
            showerror(title="Ошибка", message="Не выбрана категория для добавления")
            return
        else:
            category = category_lb.get(category_indx[0])

        new_task = {"category": category, "task": task}
        tasks.append(new_task)
        save_file(tasks)
        add_entry.delete(0, tk.END)  # Очищаем поле ввода
        showinfo(title="Успех", message="Задача успешно добавлена")
    except Exception as e:
        showerror(title="Ошибка", message=f"Ошибка при добавлении задачи: {e}")

# Кнопка добавления
add_btn = tk.Button(add_frame, text="Добавить", command=add_task)
add_btn.pack(pady=5)

# Frame для результата
result_frame = tk.Frame(window)
result_frame.place(x=250, y=60)

# Label отметки зоны для результата
result_message_label = tk.Label(result_frame, text="Результат:")
result_message_label.pack()

# Label результата
result_label = tk.Label(result_frame, text="", fg="blue", wraplength=300, justify="left")
result_label.pack(pady=5)

# Функция генерации задания
def generate_task():
    global tasks, history
    if not tasks:
        showerror(title="Ошибка", message="Нет доступных задач для генерации")
        return

    # Проверка на наличие фильтрации по категориям
    category_indx = category_lb.curselection()
    filtered_tasks = []

    if category_indx:
        category_filter = category_lb.get(category_indx[0])
        filtered_tasks = [task for task in tasks if task["category"] == category_filter]

        if not filtered_tasks:
            showerror(title="Ошибка", message="Задач в выбранной категории не существует")
            return
    else:
        filtered_tasks = tasks

    chosen_task = random.choice(filtered_tasks)
    result_text = f"{chosen_task['category'].capitalize()}: {chosen_task['task']}"
    result_label.config(text=result_text)

    # Добавляем в историю
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task": chosen_task["task"],
        "category": chosen_task["category"]
    })
    save_history(history)
    update_history_display()

# Кнопка для вывода результата
result_btn = tk.Button(result_frame, text="Сгенерировать", command=generate_task)
result_btn.pack(pady=5)

# Frame для истории генераций
history_frame = tk.Frame(window)
history_frame.place(x=500, y=60)

# Label истории
history_label = tk.Label(history_frame, text="История генераций:")
history_label.pack()

# Текстовое поле для отображения истории
history_text = tk.Text(history_frame, height=15, width=30, wrap=tk.WORD)
history_text.pack(pady=5, side=tk.LEFT)

# Полоса прокрутки для истории
scrollbar = tk.Scrollbar(history_frame, command=history_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
history_text.config(yscrollcommand=scrollbar.set)

# Функция обновления отображения истории
def update_history_display():
    history_text.delete(1.0, tk.END)
    for entry in reversed(history):  # Отображаем с последних записей
        history_text.insert(tk.END, f"{entry['date']}\n{entry['category'].capitalize()}: {entry['task']}\n\n")

# Стандартные задачи
standard_tasks = [
    {"category": "спорт", "task": "Сделать зарядку"},
    {"category": "отдых", "task": "Почитать книгу"},
    {"category": "работа", "task": "Написать приложение на Python"},
    {"category": "учёба", "task": "Написать сочинение"}
]

# Загрузка данных при запуске
tasks = load_file()
if not tasks:
    tasks = standard_tasks
    save_file(tasks)  # Сохраняем стандартные задачи, если файл был пуст

history = load_history()

# Список категорий для Listbox
category_list = ["спорт", "работа", "учёба", "отдых"]
for category in category_list:
    category_lb.insert(tk.END, category)

# Обновляем отображение истории при запуске
update_history_display()

# Запуск программы
window.mainloop()
