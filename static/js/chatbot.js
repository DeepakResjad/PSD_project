function toggleChat() {
    const chatbotContainer = document.getElementById('chatbot-container');
    chatbotContainer.classList.toggle('d-none');
}

async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    if (!message) return;

    displayMessage(message, 'user');
    chatInput.value = "";

    // Send message to backend
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    const reply = data.reply || "I'm sorry, I couldn't process that.";
    displayMessage(reply, 'bot');
}

function displayMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
