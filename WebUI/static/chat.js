$(document).ready(function () {
    // Send the message to the chat window and backend
    $('#send-btn').click(function () {
        var message = $('#text-input').val();

        if (message.trim() !== "") {
            var messageElement = $('<div></div>').text(message);
            $('#chat-window').append(messageElement);

            // Send the message to the backend
            $.ajax({
                type: 'POST',
                url: '/forward_message',
                data: JSON.stringify({ message: message }),
                contentType: 'application/json',
                success: function (response) {
                    console.log('Message forwarded to backend:', response);
                },
                error: function (error) {
                    console.error('Error forwarding message:', error);
                }
            });

            $('#text-input').val('');  // Clear input
        }
    });

    // Poll for new messages every 3 seconds
    setInterval(function () {
        $.ajax({
            type: 'GET',
            url: '/get_messages',
            success: function (data) {
                // Clear the chat window and append all messages
                $('#chat-window').empty();
                data.forEach(function (message) {
                    var messageElement = $('<div></div>').text(message);
                    $('#chat-window').append(messageElement);
                });
            },
            error: function (error) {
                console.error('Error fetching messages:', error);
            }
        });
    }, 3000);  // Poll every 3 seconds

    // Enable sending the message by pressing 'Enter'
    $('#text-input').keypress(function (e) {
        if (e.which === 13) {  // Enter key
            $('#send-btn').click();
        }
    });
});
