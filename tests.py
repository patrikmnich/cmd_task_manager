from main import TaskManager, Task, Priority


def test():
    task_manager = TaskManager()
    task_manager.task_list.append(Task("test task", Priority(Priority.HIGH), None))
    assert len(task_manager.task_list) == 1
    assert task_manager.task_list[0].name == "test task"
    assert task_manager.task_list[0].priority == Priority.HIGH
