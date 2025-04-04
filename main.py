from logic.scheduling import user_input_to_tasks, task_collision_validation
from logic.smart_assistant import find_available_time_slot

print("\n🧠 Welcome to CalMind – your intelligent scheduling assistant.\n")
print("Please choose how you'd like to create your task:\n")
print("1️⃣  Manual Scheduling – you specify the date and time.")
print("2️⃣  Smart Scheduling – you describe the task and its duration, and the assistant finds a fitting time.\n")

mode = input("👉 Type '1' for manual or '2' for smart scheduling: ").strip()

if mode == "1":
    user_input: str = input("📝 Manual, enter the task you'd like to schedule with the date: ")
    for task in user_input_to_tasks(user_input):
        task_collision_validation(task)
elif mode == "2":
    user_input: str = input("🧠 Smart scheduling, enter the task you'd like to schedule: ")
    for task in user_input_to_tasks(find_available_time_slot(user_input)):
        task_collision_validation(task)
else:
    print("❌ Invalid input. Please restart the program and choose 1 or 2.")


