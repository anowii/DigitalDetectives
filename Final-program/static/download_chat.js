document.addEventListener("DOMContentLoaded", () => {
    // Get the "Download Chat" button
    const downloadButton = document.querySelector(".bottom-bar button");

    // Add a click event listener
    downloadButton.addEventListener("click", () => {
        // Make a GET request to the backend to download the chat PDF
        fetch('/download_chat')
            .then(response => {
                if (response.ok) {
                    return response.blob(); // Get the file as a Blob
                } else {
                    throw new Error("Failed to download the chat.");
                }
            })
            .then(blob => {
                // Create a URL for the Blob and initiate the download
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "chat_history.pdf"; // Suggested file name
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url); // Clean up
            })
            .catch(error => {
                console.error("Error downloading the chat:", error);
                alert("Failed to download chat. Please try again.");
            });
    });
});