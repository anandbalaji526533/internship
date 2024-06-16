import json
import os
from datetime import datetime

class Task:
    def __init__(self, description, priority='low', due_date=None):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
    
    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, task_dict):
        task = cls(
            description=task_dict['description'],
            priority=task_dict['priority'],
            due_date=task_dict['due_date']
        )
        task.completed = task_dict['completed']
        return task

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
            return [Task.from_dict(task) for task in tasks_data]
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f)

def add_task(tasks, description, priority='low', due_date=None):
    tasks.append(Task(description, priority, due_date))
    save_tasks(tasks)

def remove_task(tasks, task_index):
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
        save_tasks(tasks)

def mark_task_completed(tasks, task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index].mark_completed()
        save_tasks(tasks)

def display_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks):
        status = "Completed" if task.completed else "Not Completed"
        due_date = task.due_date if task.due_date else "No due date"
        print(f"{i + 1}. [{task.priority}] {task.description} - Due: {due_date} - {status}")

def main():
    tasks = load_tasks()

    while True:
        print("\nTo-Do List:")
        display_tasks(tasks)

        print("\nOptions:")
        print("1. Add task")
        print("2. Remove task")
        print("3. Mark task as completed")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter task description: ")
            priority = input("Enter task priority (high, medium, low): ").lower()
            due_date = input("Enter task due date (YYYY-MM-DD) or leave blank: ")
            due_date = due_date if due_date else None
            add_task(tasks, description, priority, due_date)
        elif choice == '2':
            task_index = int(input("Enter task number to remove: ")) - 1
            remove_task(tasks, task_index)
        elif choice == '3':
            task_index = int(input("Enter task number to mark as completed: ")) - 1
            mark_task_completed(tasks, task_index)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
