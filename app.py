from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from learning_chatbot import LearningChatbot
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

learning_chatbot = LearningChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_session', methods=['POST'])
def start_session():
    learning_material = request.json['learning_material']
    response = learning_chatbot.start_conversation(learning_material)
    return jsonify({"response": response})

@socketio.on('user_message')
def handle_user_message(data):
    user_input = data['message']
    conversation_history = data['conversation_history']
    learning_material = data['learning_material']

    def emit_response(text):
        emit('ai_response_chunk', {'text': text})

    def emit_progress(progress_data):
        emit('progress_update', progress_data)

    response = learning_chatbot.handle_user_message(
        user_input, 
        conversation_history, 
        learning_material, 
        emit_response, 
        emit_progress
    )

    emit('conversation_update', {'conversation_history': response['conversation_history']})

@socketio.on('start_session')
def handle_start_session(data):
    learning_material = data['learning_material']

    def emit_response(text):
        emit('ai_response_chunk', {'text': text})

    response = learning_chatbot.start_conversation(learning_material, emit_response)
    emit('conversation_update', {'conversation_history': response['conversation_history']})

if __name__ == '__main__':
    socketio.run(app)
