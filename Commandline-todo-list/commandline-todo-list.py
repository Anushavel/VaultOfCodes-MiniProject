 
import json
from datetime import datetime, timedelta

TASK_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks):
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
    due_date = due_date if due_date else None
    task = {
        "description": description,
        "due_date": due_date,
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")

def view_tasks(tasks, filter_type=None):
    filtered_tasks = tasks
    if filter_type == 'completed':
        filtered_tasks = [task for task in tasks if task["completed"]]
    elif filter_type == 'pending':
        filtered_tasks = [task for task in tasks if not task["completed"]]
    elif filter_type == 'due_soon':
        now = datetime.now()
        filtered_tasks = [task for task in tasks if task["due_date"] and datetime.strptime(task["due_date"], "%Y-%m-%d") <= now + timedelta(days=3)]

    if not filtered_tasks:
        print("No tasks found.")
        return

    for idx, task in enumerate(filtered_tasks, 1):
        status = "Completed" if task["completed"] else "Pending"
        due_date = task["due_date"] if task["due_date"] else "No due date"
        print(f"{idx}. {task['description']} (Due: {due_date}, Status: {status})")

def mark_task_complete(tasks):
    view_tasks(tasks)
    task_num = int(input("Enter task number to mark complete: ")) - 1
    if 0 <= task_num < len(tasks):
        tasks[task_num]["completed"] = True
        save_tasks(tasks)
        print("Task marked as complete!")
    else:
        print("Invalid task number.")

def edit_task(tasks):
    view_tasks(tasks)
    task_num = int(input("Enter task number to edit: ")) - 1
    if 0 <= task_num < len(tasks):
        new_desc = input("Enter new description or leave blank to keep current: ")
        new_due_date = input("Enter new due date (YYYY-MM-DD) or leave blank: ")
        if new_desc:
            tasks[task_num]["description"] = new_desc
        if new_due_date:
            tasks[task_num]["due_date"] = new_due_date
        save_tasks(tasks)
        print("Task updated!")
    else:
        print("Invalid task number.")

def delete_task(tasks):
    view_tasks(tasks)
    task_num = int(input("Enter task number to delete: ")) - 1
    if 0 <= task_num < len(tasks):
        tasks.pop(task_num)
        save_tasks(tasks)
        print("Task deleted!")
    else:
        print("Invalid task number.")

def main_menu():
    tasks = load_tasks()
    while True:
        print("\n--- To-Do List Manager ---")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. View completed tasks")
        print("4. View pending tasks")
        print("5. View tasks due soon")
        print("6. Mark a task as completed")
        print("7. Edit a task")
        print("8. Delete a task")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_tasks(tasks, filter_type="completed")
        elif choice == "4":
            view_tasks(tasks, filter_type="pending")
        elif choice == "5":
            view_tasks(tasks, filter_type="due_soon")
        elif choice == "6":
            mark_task_complete(tasks)
        elif choice == "7":
            edit_task(tasks)
        elif choice == "8":
            delete_task(tasks)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main_menu()
