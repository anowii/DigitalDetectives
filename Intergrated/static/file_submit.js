
// Update the label text when a file is selected
function updateFileName() {
    const fileInput = document.getElementById('uploadFile');
    const fileLabel = document.querySelector('label[for="uploadFile"]');

    if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name; // Display the selected file name
    } else {
        fileLabel.textContent = 'Choose File'; // Reset to default text if no file is selected
    }
}

// Add event listener to the file input
document.getElementById('uploadFile').addEventListener('change', updateFileName);

// Handle from submisson 
document.getElementById('uploadForm').onsubmit = function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('uploadFile');
    const file = fileInput.files[0];

    if (file) {
        // Create a FormData object
        const formData = new FormData();
        formData.append('file', file); // Append the file

        // Send the file to the Flask server via AJAX
        $.ajax({
            type: 'POST',
            url: '/submit-file', // Flask route for file upload
            data: formData,
            contentType: false, // Prevent jQuery from overriding content type
            processData: false, // Prevent jQuery from processing the data
            success: function(response) {
                if (response.status === "success") {
                    alert(`File "${response.filename}" uploaded successfully!`);
                   
                    document.querySelector('label[for="uploadFile"]').textContent = 'Choose File';
                    fileInput.value = ''; // Clear the file input
                } else {
                    alert(`Error: ${response.message}`);
                }
            },
            error: function(error) {
                console.error('Error:', error);
                alert('File upload failed.');
            }
        });
    } else {
        alert('No file selected.');
    }
}