document.addEventListener('DOMContentLoaded', function() {

    const modeToggleButton = document.getElementById('mode-toggle-button');
    const modeInput = document.getElementById('mode-input');
    const userInput = document.getElementById('user-input');
    const messageForm = document.getElementById('message-form');
    const chatHistory = document.getElementById('chat-history');
    const quickActionButton = document.getElementById('quick-action-button');
    const priorityInput = document.getElementById('priority-input');

    if (modeToggleButton && modeInput) {
        modeToggleButton.addEventListener('click', function() {
            const currentMode = modeInput.value;
            if (currentMode === 'manual') {
                modeToggleButton.textContent = 'Smart';
                modeInput.value = 'smart';
            } else {
                modeToggleButton.textContent = 'Manual';
                modeInput.value = 'manual';
            }
            if(userInput) { userInput.focus(); }
        });
    }

    if (quickActionButton && priorityInput) {
        quickActionButton.addEventListener('click', function() {
            quickActionButton.classList.toggle('active');
            const isActive = quickActionButton.classList.contains('active');
            priorityInput.value = isActive ? 'true' : 'false';
            console.log('Blitz-Button Status:', isActive, 'Input Value:', priorityInput.value);
            if(userInput) { userInput.focus(); }
        });
    }

    if(messageForm && userInput && chatHistory) {
        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const messageText = userInput.value.trim();
            const formData = new FormData(messageForm);

            if (messageText !== '') {

                const userMessageDiv = document.createElement('div');
                userMessageDiv.classList.add('message', 'user-message');
                const userParagraph = document.createElement('p');
                userParagraph.textContent = messageText;
                userMessageDiv.appendChild(userParagraph);
                chatHistory.appendChild(userMessageDiv);
                chatHistory.scrollTop = chatHistory.scrollHeight;

                userInput.value = '';
                if(userInput) { userInput.focus(); }

                fetch('/process_message', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data && data.response) {
                        const botMessageDiv = document.createElement('div');
                        botMessageDiv.classList.add('message', 'bot-message');
                        const botParagraph = document.createElement('p');
                        botParagraph.textContent = data.response;
                        botMessageDiv.appendChild(botParagraph);
                        chatHistory.appendChild(botMessageDiv);
                        chatHistory.scrollTop = chatHistory.scrollHeight;
                    } else {
                         throw new Error('Invalid response format from server');
                    }
                })
                .catch(error => {
                    console.error('Fetch Error:', error);
                    const errorDiv = document.createElement('div');
                    errorDiv.classList.add('message', 'bot-message');
                    const errorParagraph = document.createElement('p');
                    errorParagraph.textContent = "Entschuldigung, ich konnte keine Antwort erhalten.";
                    errorDiv.appendChild(errorParagraph);
                    chatHistory.appendChild(errorDiv);
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                });
            } else {
                 if(userInput) { userInput.focus(); }
            }
        });
    }
});