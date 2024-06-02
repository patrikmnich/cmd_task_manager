import sys
from dataclasses import dataclass
import datetime
from enum import Enum
from typing import List


class Priority(Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2

    def __str__(self):
        return self.name


@dataclass
class Task:
    name: str
    priority: Priority
    due_date: datetime or None
    is_completed: bool = False

    def serialize(self):
        if self.due_date:
            due_date = self.due_date.strftime('%d-%m-%Y')
        else:
            due_date = None

        return f"{self.name},{self.priority.value},{due_date},{self.is_completed}\n"

    def get_state(self) -> str:
        return "COMPLETED" if self.is_completed else "ACTIVE"


def create_task_from_string(string: str):
    name, priority, due_date, is_completed = string.strip().split(",")

    if due_date != "None":
        due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
    else:
        due_date = None

    is_completed = eval(is_completed)

    return Task(name, Priority(int(priority)), due_date, is_completed)


class TaskManager:
    def __init__(self):
        self.task_list: List[Task] = []

    def add_task(self):
        task_name = input("Task name: ").strip()

        priority = Priority(Priority.LOW)
        while True:
            priority_input = input("Priority (high=0, medium=1, low=2): ").strip()
            if priority_input.lower() not in ["0", "1", "2"]:
                print("Invalid choice.")
                continue

            priority = Priority(int(priority_input))
            break

        due_date = None
        while True:
            inp = input("Does it have due date? (Y/N) ").strip()
            if inp.lower() not in ["y", "n"]:
                print("Invalid choice.")
                continue

            if inp.lower() == "y":
                while True:
                    date_input = input("Due date (dd-MM-YYYY): ").strip()
                    try:
                        due_date = datetime.datetime.strptime(date_input, "%d-%m-%Y")
                        break
                    except:
                        print("Invalid input. Please enter date in format dd-MM-YYYY.")
                        continue
            break

        task = Task(task_name, priority, due_date)
        self.task_list.append(task)

    def complete_task(self):
        if len(self.task_list) == 0:
            print("No active tasks.")
            return

        task_name = input("Enter name of task you want to complete >> ").strip()

        matched_task = None
        for task in self.task_list:
            if task_name.lower() == task.name.lower():
                matched_task = task

        if matched_task:
            matched_task.is_completed = True
            print(f"Task {matched_task.name} completed.")
        else:
            print("This task does not exist.")

    def show_tasks(self, show_active_only: bool = False):
        if len(self.task_list) == 0:
            print("No active tasks.")
            return

        for task in self.task_list:
            if show_active_only and task.is_completed:
                continue
            due_date: datetime = None
            if task.due_date:
                due_date = task.due_date.strftime("%d-%m-%Y")

            print(f"Task: {task.name}, priority: {task.priority}, due date: {due_date}, status: {task.get_state()}")

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            file.writelines([task.serialize() for task in self.task_list])
        print("Tasks saved.")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                tasks = file.readlines()
                self.task_list = [create_task_from_string(task) for task in tasks]

            print("Tasks loaded.")
        except IOError:
            open("tasks.txt")

    def start_manager(self):
        print(f'''
        Welcome to task manager
        Type number and hit enter to perform action
        Options:
            1 - add task
            2 - show active tasks
            3 - show all tasks
            4 - complete task
            5 - save tasks
            6 - load tasks
            7 - quit
        ''')

        while True:
            option = input("Enter your choice >> ").strip()
            print(option)

            match option:
                case "1":
                    self.add_task()
                case "2":
                    self.show_tasks(True)
                case "3":
                    self.show_tasks()
                case "4":
                    self.complete_task()
                case "5":
                    self.save_tasks()
                case "6":
                    self.load_tasks()
                case "7":
                    print("Goodbye.")
                    sys.exit()
                case _:
                    print("Invalid choice.")

            print("")


if __name__ == '__main__':
    task_manager = TaskManager()
    task_manager.start_manager()
