from logic.task_analysis import interpret_user_input, structured_output_from_user_input, tasks_from_structured_output

userMsg: str = input("Enter your task: ")
interpret_user_input: str = interpret_user_input(userMsg)
structured_output: dict = structured_output_from_user_input(interpret_user_input)
tasks = tasks_from_structured_output(structured_output)
for task in tasks:
    print(task)

