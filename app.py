import os
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, DiscordReader
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

from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.environ["OPENAI_API_KEY"]
discord_token = os.environ["DISCORD_TOKEN"]
channel_ids = [1116445804064931892, 1116451805954576464, 1116453224203944016, 1116453259108954112, 1116453318932316241, 1116453374204858570, 1116453444828549131, 1118360015850450954, 1118566038431342642]  # Replace with your channel_id

documents_simple_dir = SimpleDirectoryReader('./data').load_data()
documents_discord = DiscordReader(discord_token=discord_token).load_data(channel_ids=channel_ids)

documents = documents_discord + documents_simple_dir

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
