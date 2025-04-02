from logic.scheduling import user_input_to_tasks, task_collision_validation

user_input: str = input("Enter your task: ")
for task in user_input_to_tasks(user_input):
    task_collision_validation(task)
