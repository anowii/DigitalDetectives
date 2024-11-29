document.addEventListener("DOMContentLoaded", function() {
    $('#chat-window').on('click', '.context-btn', function () {
        
        // Check if the clicked button is already active
        if ($(this).hasClass('active')) {
            // If it's active, deactivate it
            $(this).removeClass('active');
            // Call python function to reset json mode(bool) to default
        } else {
            // If it's not active, deactivate all buttons and activate the clicked one
            $('.context-btn').removeClass('active');
            $(this).addClass('active');


            // Fetch Query of message the button is attatched to
            var buttonId = $(this).attr('id').replace('context-btn-', '');
            var aiMessageElement = $('#ai-message-' + buttonId);
            var aiMessageText = aiMessageElement.text();
            var start = -1;

            start = aiMessageText.indexOf("SELECT")
            end = aiMessageText.indexOf(":name", start)
            var query = aiMessageText.slice(start, end)
            
            console.log('Button clicked:', $(this).attr('id'), query);
            if (start !== -1){
                // Call python function to create json from query here
                // Call python function to set json mode (bool) to "context" or something similar
            }else{
                console.log('No Query found');
            }

        }
    });
});