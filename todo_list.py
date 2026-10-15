import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path

TASKS_FILE = Path(__file__).with_name("todo_tasks.txt")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("420x420")

        tk.Label(root, text="To-Do List", font=("Arial", 18, "bold")).pack(pady=12)

        entry_row = tk.Frame(root)
        entry_row.pack(pady=5)

        self.task_entry = tk.Entry(entry_row, width=28, font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        tk.Button(entry_row, text="Add Task", command=self.add_task).pack(side=tk.LEFT)

        self.task_list = tk.Listbox(root, width=42, height=12, font=("Arial", 12))
        self.task_list.pack(padx=12, pady=12)

        button_row = tk.Frame(root)
        button_row.pack(pady=5)

        tk.Button(button_row, text="Update", command=self.update_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row, text="Delete", command=self.delete_task).pack(side=tk.LEFT, padx=5)

        self.load_tasks()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def load_tasks(self):
        if TASKS_FILE.exists():
            tasks = TASKS_FILE.read_text(encoding="utf-8").splitlines()
            for task in tasks:
                if task.strip():
                    self.task_list.insert(tk.END, task)

    def save_tasks(self):
        tasks = self.task_list.get(0, tk.END)
        TASKS_FILE.write_text("\n".join(tasks), encoding="utf-8")

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Empty task", "Please enter a task.")
            return

        self.task_list.insert(tk.END, task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()

    def update_task(self):
        selection = self.task_list.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Select a task to update.")
            return

        index = selection[0]
        current_task = self.task_list.get(index)
        new_task = simpledialog.askstring("Update task", "Edit the selected task:", initialvalue=current_task)

        if new_task and new_task.strip():
            self.task_list.delete(index)
            self.task_list.insert(index, new_task.strip())
            self.save_tasks()

    def delete_task(self):
        selection = self.task_list.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Select a task to delete.")
            return

        self.task_list.delete(selection[0])
        self.save_tasks()

    def close_app(self):
        self.save_tasks()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    TodoApp(window)
    window.mainloop()