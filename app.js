
document.getElementById('guess-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    let guess = document.getElementById('guess-input').value;
    try {
        let response = await axios.post('/guess', {guess: guess});
        let message = "";
        switch(response.data.result) {
            case "ok":
                message = "Great! That's a valid word on the board.";
                break;
            case "not-on-board":
                message = "The word is not on the board.";
                break;
            case "not-a-word":
                message = "That's not a valid word.";
                break;
        }
        document.getElementById('response-message').innerText = message;
    } catch (error) {
        console.error("Error submitting guess:", error);
    }
});
