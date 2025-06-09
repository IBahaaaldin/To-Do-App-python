import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = load_tasks()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Title
        tk.Label(self.frame, text="Task Title:").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.frame, width=30)
        self.title_entry.grid(row=0, column=1)

        # Priority
        tk.Label(self.frame, text="Priority (1-5):").grid(row=1, column=0)
        self.priority_entry = tk.Entry(self.frame, width=5)
        self.priority_entry.grid(row=1, column=1, sticky="w")

        # Due date
        tk.Label(self.frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.due_entry = tk.Entry(self.frame, width=15)
        self.due_entry.grid(row=2, column=1, sticky="w")

        # Buttons
        tk.Button(self.frame, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(self.frame, text="Sort by Due Date", command=lambda: self.sort_tasks("due")).grid(row=4, column=0)
        tk.Button(self.frame, text="Sort by Priority", command=lambda: self.sort_tasks("priority")).grid(row=4, column=1)

        self.listbox = tk.Listbox(self.root, width=75)
        self.listbox.pack()

        tk.Button(self.root, text="Mark as Complete", command=self.mark_complete).pack(side="left", padx=10)
        tk.Button(self.root, text="Delete Task", command=self.delete_task).pack(side="left", padx=10)

        self.refresh_list()

    def add_task(self):
        title = self.title_entry.get().strip()
        try:
            priority = int(self.priority_entry.get().strip())
            if priority < 1 or priority > 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Priority must be an integer between 1 and 5.")
            return

        due = self.due_entry.get().strip()
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Input", "Date format must be YYYY-MM-DD.")
            return

        if not title:
            messagebox.showerror("Missing Title", "Task title cannot be empty.")
            return

        self.tasks.append({
            "title": title,
            "priority": priority,
            "due_date": due,
            "completed": False
        })
        save_tasks(self.tasks)
        self.clear_entries()
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            status = "✓" if task["completed"] else "✗"
            self.listbox.insert(tk.END, f"{i+1}. [{status}] {task['title']} (P{task['priority']} - Due {task['due_date']})")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)

    def mark_complete(self):
        try:
            idx = self.listbox.curselection()[0]
            self.tasks[idx]["completed"] = True
            save_tasks(self.tasks)
            self.refresh_list()
        except IndexError:
            messagebox.showerror("No Selection", "Please select a task to mark as complete.")

    def delete_task(self):
        try:
            idx = self.listbox.curselection()[0]
            self.tasks.pop(idx)
            save_tasks(self.tasks)
            self.refresh_list()
        except IndexError:
            messagebox.showerror("No Selection", "Please select a task to delete.")

    def sort_tasks(self, key):
        if key == "priority":
            self.tasks.sort(key=lambda x: x["priority"])
        elif key == "due":
            self.tasks.sort(key=lambda x: x["due_date"])
        save_tasks(self.tasks)
        self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
