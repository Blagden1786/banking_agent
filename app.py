from flask import Flask, render_template_string, request, jsonify

from agents.orchestrator_agent import Orchestrator

app = Flask(__name__)

# Simple chatbot logic
def generate_reply(user_message, agent: Orchestrator):
    output = agent.current_agent(user_message, True)

    if output == 'ENDCHAT' or output.endswith("COMPLETE"):
        output = output.removesuffix("COMPLETE") + "\nThanks for using this service today!! Hope to see you soon."

    return output

# HTML Template
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Simple Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f7f7; display: flex; justify-content: center; align-items: center; height: 100vh; }
        #chat-container { background: white; padding: 20px; width: 400px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.2); }
        #messages { height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
        .user { text-align: right; color: blue; margin: 5px 0; }
        .bot { text-align: left; color: green; margin: 5px 0; }
        input { width: 80%; padding: 10px; }
        button { width: 18%; padding: 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; border-radius: 5px; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div id="chat-container">
        <h2>💬 Python Chatbot</h2>
        <div id="messages"></div>
        <input type="text" id="userInput" placeholder="Type a message..." autofocus>
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage('user', message);
            input.value = '';

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            addMessage('bot', data.reply);
        }

        function addMessage(sender, text) {
            const msgDiv = document.createElement('div');
            msgDiv.className = sender;
            msgDiv.textContent = (sender === 'user' ? 'You: ' : 'Bot: ') + text;
            document.getElementById('messages').appendChild(msgDiv);
            document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    reply = generate_reply(user_msg, orces)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    orces = Orchestrator()

    app.run(debug=True)
