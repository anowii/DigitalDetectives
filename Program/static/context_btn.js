document.addEventListener("DOMContentLoaded", function() {
    $('#chat-window').on('click', '.context-btn', function () {
        console.log('Button clicked:', $(this).attr('id')); // Debugging
        
        // Check if the clicked button is already active
        if ($(this).hasClass('active')) {
            // If it's active, deactivate it
            $(this).removeClass('active');
        } else {
            // If it's not active, deactivate all buttons and activate the clicked one
            $('.context-btn').removeClass('active');
            $(this).addClass('active');
        }
    });
});