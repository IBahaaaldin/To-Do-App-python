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

def display_tasks(tasks, show_all=True):
    if not tasks:
        print("No tasks available.")
        return
    print("\nYour Tasks:")
    for i, task in enumerate(tasks):
        if show_all or not task["completed"]:
            status = "✓" if task["completed"] else "✗"
            print(f"{i+1}. [{status}] {task['title']} (Priority: {task['priority']}, Due: {task['due_date']})")

def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    try:
        priority = int(input("Enter priority (1–5): ").strip())
        if priority < 1 or priority > 5:
            raise ValueError
    except ValueError:
        print("Invalid priority. Must be a number between 1 and 5.")
        return

    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    task = {
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")

def mark_task_complete(tasks):
    display_tasks(tasks, show_all=False)
    try:
        idx = int(input("Enter the task number to mark complete: ")) - 1
        if idx < 0 or idx >= len(tasks):
            raise IndexError
    except (ValueError, IndexError):
        print("Invalid task number.")
        return
    tasks[idx]["completed"] = True
    save_tasks(tasks)
    print("Task marked as complete.")

def delete_task(tasks):
    display_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        if idx < 0 or idx >= len(tasks):
            raise IndexError
    except (ValueError, IndexError):
        print("Invalid task number.")
        return
    tasks.pop(idx)
    save_tasks(tasks)
    print("Task deleted.")

def sort_tasks(tasks):
    key = input("Sort by (priority/due/title): ").strip().lower()
    if key not in ["priority", "due", "title"]:
        print("Invalid sort key.")
        return
    if key == "priority":
        tasks.sort(key=lambda x: x["priority"])
    elif key == "due":
        tasks.sort(key=lambda x: x["due_date"])
    else:
        tasks.sort(key=lambda x: x["title"].lower())
    save_tasks(tasks)
    print(f"Tasks sorted by {key}.")

def main():
    tasks = load_tasks()
    while True:
        print("\n==== To-Do List ====")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as complete")
        print("4. Delete task")
        print("5. Sort tasks")
        print("6. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_task_complete(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            sort_tasks(tasks)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
