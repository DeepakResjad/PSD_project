let isFirstOpen = true;

// Function to initialize the chatbot with a greeting message
function initializeChat() {
    if (isFirstOpen) {
        displayMessage("Hello! I'm your virtual assistant. How can I help you today?", 'bot');
        isFirstOpen = false;
    }
}

// Send message function to handle user input and bot response
async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    if (!message) return;  // Do nothing if input is empty

    displayMessage(message, 'user');
    chatInput.value = ""; // Clear the input field
    displayMessage("...", 'bot'); // Display loading indicator

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        // Log the response status and data for debugging
        console.log('Response Status:', response.status);
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log('Response Data:', data);

        // Check if 'reply' exists in the response data
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

// Function to display a message in the chat
function displayMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to the latest message
}

// Function to remove the loading indicator (the "..." message)
function removeLoadingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const loadingMessage = Array.from(chatMessages.querySelectorAll('.message.bot'))
        .find(msg => msg.textContent === "...");
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Close the chatbot and redirect to the homepage or main menu
function closeChat() {
    window.location.href = "/"; // Modify this URL to redirect to the desired location
}

// Event listener for the Enter key to send a message
document.getElementById('chat-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Initialize the chatbot when the page loads
window.onload = initializeChat;
