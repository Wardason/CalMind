from logic.task_analysis import interpret_user_input, task_from_user_input

userMsg: str = input("Enter your task: ")
interpret_user_input: str = interpret_user_input(userMsg)
print(interpret_user_input)
task: str = task_from_user_input(interpret_user_input)
