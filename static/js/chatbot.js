let isFirstOpen = true;

function toggleChat() {
    const chatbotContainer = document.getElementById('chatbot-container');

    // Toggle visibility of chatbot container
    chatbotContainer.classList.toggle('d-none');

    // Display initial bot greeting if opening for the first time
    if (!chatbotContainer.classList.contains('d-none') && isFirstOpen) {
        displayMessage("Hello! I'm your virtual assistant. How can I help you today?", 'bot');
        isFirstOpen = false; // Ensures the greeting only shows the first time
    }
}

async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    if (!message) return;

    displayMessage(message, 'user');
    chatInput.value = "";
    displayMessage("...", 'bot'); // Temporary loading indicator

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        // Log the response to see if it's successful and contains the expected JSON
        console.log('Response Status:', response.status); // Log status
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log('Response Data:', data); // Log the parsed JSON data

        // Check if the reply exists in the response
        if (!data || !data.reply) {
            console.error('No reply found in response data:', data);
            removeLoadingIndicator();
            displayMessage("I'm sorry, I couldn't process that.", 'bot');
            return;
        }

        const reply = data.reply;

        // Remove loading indicator and display the reply
        removeLoadingIndicator();
        displayMessage(reply, 'bot');
    } catch (error) {
        console.error('Error in sendMessage:', error);
        removeLoadingIndicator();
        displayMessage("There was an error connecting to the server.", 'bot');
    }
}

function displayMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeLoadingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const loadingMessage = Array.from(chatMessages.querySelectorAll('.message.bot'))
        .find(msg => msg.textContent === "...");
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Event listener for sending message on Enter key press
document.getElementById('chat-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
