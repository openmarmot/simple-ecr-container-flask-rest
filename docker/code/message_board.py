# https://github.com/openmarmot/simple-ecr-container-flask-rest

#pip install -U flask flask-cors
#python message_board.py


from flask import Flask, request, jsonify, render_template_string, escape
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# CORS is optional. needed if another website will be displaying the api data
CORS(app)
messages = []

# HTML Template for the default page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message Board</title>
</head>
<body>
    <h1>Message Board</h1>
    
    <h2>Instructions</h2>
    <p>To add a message:</p>
    <pre>curl -X POST http://IP_ADDRESS:PORT/messages -H "Content-Type: application/json" -d '{"text": "Your message here"}'</pre>
    <p>To retrieve messages:</p>
    <pre>curl -X GET http://IP_ADDRESS:PORT/messages</pre>
    <p>To clear all messages:</p>
    <pre>curl -X DELETE http://IP_ADDRESS:PORT/messages</pre>
    
    <h2>Messages</h2>
    <div id="message-container">Loading messages...</div>
    
    <button id="clear-button">Clear Messages</button>

    <script>
        // Function to fetch and display messages
        async function fetchMessages() {
            try {
                const response = await fetch('/messages');
                if (!response.ok) throw new Error(`Error: ${response.statusText}`);
                
                const messages = await response.json();
                const messageContainer = document.getElementById('message-container');
                messageContainer.innerHTML = '';

                if (messages.length === 0) {
                    messageContainer.innerHTML = '<p>No messages available.</p>';
                } else {
                    messages.forEach(msg => {
                        const messageElement = document.createElement('p');
                        messageElement.textContent = `${msg.timestamp}: ${msg.text}`;
                        messageContainer.appendChild(messageElement);
                    });
                }
            } catch (error) {
                console.error('Error fetching messages:', error);
                document.getElementById('message-container').innerHTML = 'Error loading messages';
            }
        }

        // Function to clear messages
        async function clearMessages() {
            try {
                const response = await fetch('/messages', { method: 'DELETE' });
                if (!response.ok) throw new Error(`Error: ${response.statusText}`);
                fetchMessages();  // Refresh messages after clearing
            } catch (error) {
                console.error('Error clearing messages:', error);
            }
        }

        // Fetch messages initially and add event listener for clear button
        fetchMessages();
        document.getElementById('clear-button').addEventListener('click', clearMessages);

        // Poll for new messages every 5 seconds
        setInterval(fetchMessages, 5000);  // Adjust time as needed (5000ms = 5s)
    </script>
</body>
</html>

"""

# Route for the default page
@app.route('/')
def index():
    return render_template_string(html_template)

# Endpoint to receive a new message
@app.route('/messages', methods=['POST'])
def add_message():
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    message = {
        "text": escape(data['text']),  # Escape dangerous characters
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    messages.append(message)
    return jsonify({"message": "Message added successfully"}), 201

# Endpoint to retrieve all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages), 200

# Endpoint to clear all messages
@app.route('/messages', methods=['DELETE'])
def clear_messages():
    global messages
    messages = []
    return jsonify({"message": "All messages cleared"}), 200

if __name__ == '__main__':
    app.run(debug=True)
