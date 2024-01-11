from flask import Flask, request, jsonify

import locale
from model_trainer import ModelTrainer
from chat_bot import ChatBot

locale.setlocale(locale.LC_TIME, 'sr_RS.UTF-8')
locale.setlocale(locale.LC_CTYPE, 'sr_RS.UTF-8')

app = Flask(__name__)

chat_bot = ChatBot()


@app.route('/chat', methods=['POST'])
def chat():
    json_data = request.get_json()
    return chat_bot.get_response_function(json_data["input"])

@app.route('/train', methods=['GET'])
def train():
    ModelTrainer().train_model()
    return jsonify({'response': "Training model"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
