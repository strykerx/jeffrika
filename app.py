import os
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex
from flask import Flask, request, render_template
import openai
import json
from flask import jsonify

app = Flask(__name__)

class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        openai.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        response = self.index.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message['content']
    
    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)

openai_api_key = os.getenv("OPENAI_API_KEY")

documents = SimpleDirectoryReader('./data').load_data()

index = GPTVectorStoreIndex.from_documents(documents)

# Swap out your index below for whatever knowledge base you want
bot = Chatbot(openai_api_key, index=index)
bot.load_chat_history("chat_history.json")

@app.route("/", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        query_engine = index.as_query_engine()
        response = query_engine.query(user_input)
        bot.save_chat_history("chat_history.json")
        return jsonify(user_input=user_input, bot_response=response.response, chat_history=bot.chat_history)
    return render_template('chat.html')


if __name__ == "__main__":
    app.run(debug=True)
