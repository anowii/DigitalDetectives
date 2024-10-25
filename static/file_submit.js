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