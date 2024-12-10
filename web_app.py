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
    </head>
    <body style="font-family: Arial, sans-serif;">
        <h1>Chat with Max</h1>
        <div id="chat_window" style="border: 1px solid #ccc; padding: 10px; width: 60%; height: 300px; overflow-y: auto; margin-bottom: 10px;"></div>
        <input id="input_text" type="text" style="width: 60%; height: 30px;" placeholder="Type your message here...">
        <button onclick="sendMessage()" style="height: 36px;">Send</button>
        <script>
            async function sendMessage() {
                const userMessage = document.getElementById('input_text').value;
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMessage })
                });
                const data = await response.json();
                if (data.response) {
                    // Display messages in the chat window
                    const chatWindow = document.getElementById('chat_window');
                    chatWindow.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
                    chatWindow.innerHTML += `<p><strong>Max:</strong> ${data.response}</p>`;
                    chatWindow.scrollTop = chatWindow.scrollHeight;  // Auto-scroll to the bottom
                }
                document.getElementById('input_text').value = '';  // Clear input field
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
    app.run(debug=False)