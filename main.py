
from flask import Flask, render_template, jsonify, request

from core_logic.logic.scheduling import user_input_to_tasks, task_collision_validation
from core_logic.logic.smart_assistant import find_available_time_slot

app = Flask(__name__, template_folder='web_app/templates', static_folder='web_app/static')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    user_message = request.form.get('user_message', '')
    selected_mode = request.form.get('mode', 'manual')
    priority_str = request.form.get('priority', 'false')
    is_priority = priority_str.lower() == 'true'

    bot_response_text = ""

    if selected_mode == 'manual':
        for task in user_input_to_tasks(user_message):
            bot_response_text += task_collision_validation(task)
    elif selected_mode == 'smart':
        for task in user_input_to_tasks(find_available_time_slot(user_message)):
            bot_response_text += task_collision_validation(task)

    return jsonify({'response': bot_response_text})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5050)