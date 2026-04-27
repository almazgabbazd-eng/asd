import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import random
import os
from datetime import datetime

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("700x500")

        # Предопределённые задачи с типами
        self.predefined_tasks = [
            {"task": "Прочитать статью", "type": "Учёба"},
            {"task": "Сделать зарядку", "type": "Спорт"},
            {"task": "Написать отчёт", "type": "Работа"},
            {"task": "Изучить новый язык программирования", "type": "Учёба"},
            {"task": "Пробежать 5 км", "type": "Спорт"},
            {"task": "Провести встречу с командой", "type": "Работа"},
            {"task": "Попрактиковаться в английском", "type": "Учёба"},
            {"task": "Посетить спортзал", "type": "Спорт"},
            {"task": "Подготовить презентацию", "type": "Работа"}
        ]

        self.history = []
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        """Настройка интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Фрейм генерации задач
        generate_frame = ttk.LabelFrame(main_frame, text="Генерация задач", padding="10")
        generate_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Button(generate_frame, text="Сгенерировать случайную задачу",
                  command=self.generate_random_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(generate_frame, text="Добавить свою задачу",
                  command=self.add_custom_task).pack(side=tk.LEFT, padx=5)

        # Фильтр по типу
        ttk.Label(generate_frame, text="Фильтр:").pack(side=tk.LEFT, padx=(20, 5))
        self.filter_combo = ttk.Combobox(generate_frame,
                                      values=["Все", "Учёба", "Спорт", "Работа"],
                                      state="readonly")
        self.filter_combo.set("Все")
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        self.filter_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        # Результат генерации
        self.result_label = ttk.Label(main_frame, text="",
                                  wraplength=600, font=("Arial", 12, "bold"),
                                  foreground="blue")
        self.result_label.grid(row=1, column=0, columnspan=2, pady=10)

        # История сгенерированных задач
        history_frame = ttk.LabelFrame(main_frame, text="История задач", padding="10")
        history_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        columns = ("Дата", "Задача", "Тип")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Кнопка очистки истории
        clear_btn = ttk.Button(history_frame, text="Очистить историю", command=self.clear_history)
        clear_btn.grid(row=1, column=0, pady=(10, 0))

    def validate_task(self, task_text):
        """Валидация ввода задачи"""
        if not task_text.strip():
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return False
        return True

    def generate_random_task(self):
        """Генерация случайной задачи"""
        filter_type = self.filter_combo.get()

        # Фильтруем задачи по типу
        if filter_type == "Все":
            available_tasks = self.predefined_tasks
        else:
            available_tasks = [task for task in self.predefined_tasks if task["type"] == filter_type]


        if not available_tasks:
            messagebox.showwarning("Предупреждение", "Нет задач для выбранного фильтра!")
            return

        selected_task = random.choice(available_tasks)

        # Добавляем в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            "date": timestamp,
            "task": selected_task["task"],
            "type": selected_task["type"]
        }
        self.history.append(history_entry)

        # Отображаем результат
        self.result_label.config(text=f"{selected_task['task']} ({selected_task['type']})")

        # Обновляем таблицу истории
        self.update_history_table()
        self.save_history()

    def add_custom_task(self):
        """Добавление пользовательской задачи"""
        task_dialog = simpledialog.askstring("Добавление задачи", "Введите задачу:")
        if task_dialog:
            type_dialog = simpledialog.askstring("Тип задачи",
                                              "Выберите тип:\n1 — Учёба\n2 — Спорт\n3 — Работа")
            type_map = {"1": "Учёба", "2": "Спорт", "3": "Работа"}
            selected_type = type_map.get(type_dialog, "Другое")

            if self.validate_task(task_dialog):
                # Добавляем в предопределённые задачи
                self.predefined_tasks.append({"task": task_dialog, "type": selected_type})
                messagebox.showinfo("Успех", "Задача добавлена в список!")

    def update_history_table(self):
        """Обновление таблицы истории"""
        self.history_tree.delete(*self.history_tree.get_children())

        filter_type = self.filter_combo.get()
        filtered_history = self.history


        if filter_type != "Все":
            filtered_history = [entry for entry in self.history if entry["type"] == filter_type]
        for entry in filtered_history:
            self.history_tree.insert("", "end", values=(
                entry["date"],
                entry["task"],
                entry["type"]
            ))

    def apply_filter(self, event=None):
        """Применение фильтра к истории"""
        self.update_history_table()

    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history = []
            self.update_history_table()
            self.save_history()
            messagebox.showinfo("Успех", "История очищена!")

    def save_history(self):
        """Сохранение истории в JSON-файл"""
        os.makedirs('data', exist_ok=True)
        try:
            with open('data/history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")
            if __name__ == '__main__':
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()

