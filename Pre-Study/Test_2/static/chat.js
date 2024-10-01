// This line gets a reference to the HTML element with the id "chat-form"
const chatForm = document.getElementById('chat-form');
// This line gets a reference to the HTML element with the id "user-input"
const userInput = document.getElementById('user-input');

// This line gets a reference to the HTML element with the id "file-input"
const fileInput = document.getElementById('file-input');

// This line gets a reference to the HTML element with the id "chatbox"
const chatbox = document.getElementById('chatbox');

// This line gets a reference to the HTML element with the id "send-btn"
const sendBtn = document.getElementById('send-btn');

// This line adds an event listener to the send button that listens for a click event
sendBtn.addEventListener('click', (e) => {
  // This line prevents the default form submission behavior
  e.preventDefault();

  // This line gets the trimmed value of the user's input
  const userInputValue = userInput.value.trim();

  // This line gets the selected file from the file input
  const file = fileInput.files[0]; // Get the selected file

  // This line checks if the user has entered some input or selected a file
  if (userInputValue !== '' || file) {
    // This line sends a POST request to the '/llm_response' endpoint
    fetch('/llm_response', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: userInputValue, file: file }),
    })
    .then(response => response.json())
    .then((data) => {

      // This line checks if the response from the server contains a response
      if (data.response) {
        // This line gets the response text from the server
        const responseText = data.response;

        // This line creates a new div element to hold the chat entry
        const chatEntry = document.createElement('div');
        chatEntry.className = 'message'; // Add a class to the chat entry

        // Create a span for the user's input
        const userInputDiv = document.createElement('div');
        userInputDiv.className = 'user-input'; // Add user-input class
        userInputDiv.textContent = userInputValue;

        // Create a span for the LLM's response
        const llmResponseDiv = document.createElement('div');
        llmResponseDiv.className = 'llm-response'; // Add llm-response class
        llmResponseDiv.textContent = `LLM: ${responseText}`;

        // This line checks if a file was uploaded
        if (file) {
          // This line creates a span for the uploaded file
          const fileDiv = document.createElement('div');
          fileDiv.className = 'file-upload';
          fileDiv.textContent = `File: ${file.name} (${file.size} bytes)`;
          chatEntry.appendChild(fileDiv);
        }

        // Append the LLM response first, then the user input
        chatEntry.appendChild(llmResponseDiv);
        chatEntry.appendChild(userInputDiv);

        // Append the new message to the bottom of the chatbox
        chatbox.appendChild(chatEntry);
        
        // This line clears the user input and file input fields
        userInput.value = '';
        fileInput.value = '';

        // This line scrolls the chatbox to the bottom
        chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
      } else {
        // This line logs an error message to the console if the response from the server contains an error
        console.error('Error:', data.error); // Display the error message
      }
    })
    .catch((error) => {
      // This line logs any errors that occur during the fetch request to the console
      console.error(error);
    });
  }
});