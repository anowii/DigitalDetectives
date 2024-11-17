document.querySelector(".trash-button").addEventListener("click", function () {
    if (confirm("Are you sure you want to delete this session? This will clear the chat and unload any uploaded files.")) {
        fetch('/delete_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    // Clear chat window
                    const chatWindow = document.getElementById("chat-window");
                    chatWindow.innerHTML = "<p>Session cleared. Start a new session by uploading a file.</p>";

                } else {
                    alert("Failed to clear session. Please try again.");
                }
            })
            .catch((error) => console.error("Error:", error));
    }
});