document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("guess-form");
    const timerDisplay = document.getElementById("timer");
    const validGuessesList = document.getElementById("valid-guesses");
    const gameEndEvent = new Event('gameEnd');
    const gameEndMessage = document.getElementById("game-end-message");
    const timerInterval = setInterval(updateTimer, 1000);  // Update every second
    const newGameButton = document.getElementById("new-game-button");

    let score = 0;
    let timeLeft = 60;  // 60 seconds timer

    // Function to update the timer display and check for game end
    function updateTimer() {
        if (!timerDisplay) return;
        else {
            timeLeft -= 1;  // Decrement the timer by 1 second
            timerDisplay.textContent = `${timeLeft}`;  // Update the displayed timer
        }
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            if (form) form.style.display = 'none';  // Hide the guess form
            if (gameEndMessage) gameEndMessage.style.display = 'block';  // Show the game end message
            
            // Dispatch the gameEnd event
            document.dispatchEvent(gameEndEvent);
        }
    }
        
    async function handleFormSubmit(event) {
        event.preventDefault();

        // Get the user's guess from the input field
        const guessInput = document.getElementById("guess-input");
        const guess = guessInput ? guessInput.value : "";
        
        // Send the guess to the backend for validation using axios
        try {
            const response = await axios.post("/check-guess", { guess: guess });
            const result = response.data.result;

            // Update score and valid guesses list for valid words
            if (result === "ok") {
                score += guess.length;
                const scoreDisplay = document.getElementById("score");
                if (scoreDisplay) scoreDisplay.textContent = score;

                // Append to the valid guesses list
                if (validGuessesList) {
                    const li = document.createElement("li");
                    li.textContent = guess;
                    validGuessesList.appendChild(li);
                }
            }

            // Displaying the response from the backend
            alert(result);

        } catch (error) {
            console.error("Error submitting guess:", error);
        }

        // Clear the input field for the next guess
        if (guessInput) guessInput.value = '';
    }

    if (form) form.addEventListener("submit", handleFormSubmit);
});

// Assuming this code runs when the game timer ends
document.addEventListener('gameEnd', function() {
    const scoreElement = document.getElementById("score");
    const finalScore = scoreElement ? parseInt(scoreElement.textContent, 10) : 0;

    try {
        axios.post("/end-game", { score: finalScore }).then(response => {
            const highscoreElement = document.getElementById("highscore");
            if (highscoreElement) {
                highscoreElement.textContent = response.data.highscore;
            }

            // Show the "New Game" button
            if (gameEndMessage) gameEndMessage.style.display = 'block';
        });
    } catch (error) {
        console.error("Error sending final score:", error);
    }
});

