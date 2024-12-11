from flask import Flask, request, jsonify
from final_model import get_response  # Import your function
import os

# Load API Key from Environment Variables (if applicable)
API_KEY = os.getenv("OPENAI_API_KEY")  # Set this environment variable securely

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat with Max</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #8e44ad, #3498db);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .glass-container {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                width: 40%;
                max-width: 500px;
                padding: 20px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            #chat_window {
                height: 300px;
                overflow-y: auto;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 15px;
                color: white;
                font-size: 14px;
            }
            #input_area {
                display: flex;
                gap: 10px;
            }
            #input_text {
                flex: 1;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-size: 16px;
                color: #333;
                background: rgba(255, 255, 255, 0.7);
                outline: none;
            }
            #send_button {
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                background: linear-gradient(135deg, #ff7eb3, #ff758c);
                color: white;
                font-size: 16px;
                cursor: pointer;
                transition: 0.3s ease;
            }
            #send_button:hover {
                background: linear-gradient(135deg, #ff758c, #ff7eb3);
            }
        </style>
    </head>
    <body>
        <div class="glass-container">
            <div id="chat_window"></div>
            <div id="input_area">
                <input id="input_text" type="text" placeholder="Type your message here...">
                <button id="send_button" onclick="sendMessage()">Send</button>
            </div>
        </div>
        <script>
            async function sendMessage() {
                const userMessage = document.getElementById('input_text').value;
                if (!userMessage.trim()) return;

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMessage })
                });
                const data = await response.json();
                const chatWindow = document.getElementById('chat_window');

                if (data.response) {
                    chatWindow.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
                    chatWindow.innerHTML += `<p><strong>Max:</strong> ${data.response}</p>`;
                }
                chatWindow.scrollTop = chatWindow.scrollHeight;
                document.getElementById('input_text').value = '';
            }
        </script>
    </body>
    </html>
    '''

# Chat route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Use the API key if necessary
    if API_KEY:
        print(f"Using API Key: {API_KEY}")  # Replace this with actual API usage if required

    try:
        response = get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)