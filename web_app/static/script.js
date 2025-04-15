document.addEventListener('DOMContentLoaded', function() {

    const modeToggleButton = document.getElementById('mode-toggle-button');
    const modeInput = document.getElementById('mode-input');
    const userInput = document.getElementById('user-input');

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

    const messageForm = document.getElementById('message-form');
    if(messageForm) {
        messageForm.addEventListener('submit', function(event) {
            console.log('Formular wird abgeschickt mit Modus:', modeInput.value);
        });
    }

});