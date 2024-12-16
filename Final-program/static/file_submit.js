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

$(document).ready(function () {
    $('#uploadForm').on('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        const fileInput = document.getElementById('uploadFile');
        const file = fileInput.files[0];
        const uploadButton = document.getElementById('upload-btn'); // The upload button

        if (file) {
            // Disable the button to prevent multiple submissions
            uploadButton.disabled = true;

            // Update progress message
            $('#messageContent').text("Processing your file...");

            // Create a FormData object
            const formData = new FormData(this);

            // Send the file to the Flask server via AJAX
            $.ajax({
                type: 'POST',
                url: '/submit-file', // Flask route for file upload
                data: formData,
                contentType: false, // Prevent jQuery from overriding content type
                processData: false, // Prevent jQuery from processing the data
                success: function (response) {
                    if (response.status === "success") {
                        $('#messageContent').text(`File "${response.filename}" uploaded successfully!`);

                        // Reset file input and label
                        document.querySelector('label[for="uploadFile"]').textContent = 'Choose File';
                        fileInput.value = ''; // Clear the file input
                    } else {
                        $('#messageContent').text(`Error: ${response.message}`);
                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                    $('#messageContent').text('File upload failed.');
                },
                complete: function () {
                    // Re-enable the button once the upload is complete
                    uploadButton.disabled = false;
                }
            });
        } else {
            alert('No file selected.');
        }
    });
});