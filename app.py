import tkinter as tk
import random
import json
from datetime import datetime
from tkinter import messagebox
from tkinter.messagebox import showerror, showinfo


# КОНСТАНТЫ
TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.json"
WINDOW_TITLE = "Random Task Generator"
WINDOW_SIZE = "800x500"
STANDARD_TASKS = [
    {"category": "спорт", "task": "Сделать зарядку"},
    {"category": "отдых", "task": "Почитать книгу"},
    {"category": "работа", "task": "Написать приложение на Python"},
    {"category": "учёба", "task": "Написать сочинение"}
]
CATEGORIES = ["спорт", "работа", "учёба", "отдых"]


# Глобальные переменные
tasks = []
history = []

def load_file(filename):
    """Загружает данные из JSON‑файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", f"Файл {filename} повреждён. Используется стандартный набор задач.")
        return []

def save_file(tasks_list, filename):
    """Сохраняет данные в JSON‑файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(tasks_list, file, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить задачи: {e}")


def load_history():
    """Загружает историю генераций."""
    return load_file(HISTORY_FILE)

def save_history(history_list):
    """Сохраняет историю генераций."""
    save_file(history_list, HISTORY_FILE)

def init_data():
    """Инициализирует данные при запуске программы."""
    global tasks, history
    tasks = load_file(TASKS_FILE)
    if not tasks:
        tasks = STANDARD_TASKS
        save_file(tasks, TASKS_FILE)
    history = load_history()

def create_welcome_label(parent):
    """Создаёт приветственную надпись."""
    welcome_label = tk.Label(
        parent,
        text="Добро пожаловать в генератор случайных задач!",
        font=("Arial", 12, "bold")
    )
    welcome_label.pack(pady=10)
    return welcome_label

def create_add_frame(parent):
    """Создаёт фрейм для добавления задач."""
    add_frame = tk.Frame(parent)
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
    for category in CATEGORIES:
        category_lb.insert(tk.END, category)
    category_lb.pack(pady=5)


    return add_frame, add_entry, category_lb

def create_result_frame(parent):
    """Создаёт фрейм для отображения результата."""
    result_frame = tk.Frame(parent)
    result_frame.place(x=250, y=60)

    # Label отметки зоны для результата
    result_message_label = tk.Label(result_frame, text="Результат:")
    result_message_label.pack()

    # Label результата
    result_label = tk.Label(
        result_frame,
        text="",
        fg="blue",
        wraplength=300,
        justify="left"
    )
    result_label.pack(pady=5)

    return result_frame, result_label

def create_history_frame(parent):
    """Создаёт фрейм для истории генераций."""
    history_frame = tk.Frame(parent)
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


    return history_frame, history_text

def add_task(add_entry, category_lb):
    """Добавляет новую задачу с проверкой на дубликаты."""
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

        # Проверка на дублирование: ищем задачу с таким же текстом и категорией
        is_duplicate = any(
            existing_task["task"].strip().lower() == task.lower()
            and existing_task["category"] == category
            for existing_task in tasks
        )

        if is_duplicate:
            showerror(
                title="Ошибка",
                message="Задача с таким текстом уже существует в этой категории"
            )
            return

        new_task = {"category": category, "task": task}
        tasks.append(new_task)
        save_file(tasks, TASKS_FILE)
        add_entry.delete(0, tk.END)  # Очищаем поле ввода
        showinfo(title="Успех", message="Задача успешно добавлена")
    except Exception as e:
        showerror(title="Ошибка", message=f"Ошибка при добавлении задачи: {e}")


def generate_task(result_label, history_text):
    """Генерирует случайную задачу и добавляет в историю."""
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
    update_history_display(history_text)

def update_history_display(history_text):
    """Обновляет отображение истории."""
    history_text.delete(1.0, tk.END)
    for entry in reversed(history):  # Отображаем с последних записей
        history_text.insert(
            tk.END,
            f"{entry['date']}\n{entry['category'].capitalize()}: {entry['task']}\n\n"
        )

def main():
    """Основная функция запуска приложения."""
    # Создание
