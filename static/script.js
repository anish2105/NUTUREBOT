$(document).ready(function() {
    const chatDisplay = $('#chat-display');
    const questionInput = $('#question-input');
    const submitBtn = $('#submit-btn');

    submitBtn.on('click', function() {
        const question = questionInput.val();
        if (question) {
            displayMessage('You', question, 'outgoing');
            
            $.ajax({
                url: '/ask',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ 'question': question }),
                success: function(response) {
                    const answer = response.response;
                    displayMessage('WellnessWhisper', answer, 'incoming');
                }
            });

            questionInput.val('');
        }
    });

    function displayMessage(sender, message, messageClass) {
        const messageDiv = $('<div>').addClass('message').addClass(messageClass);
        const messageContentDiv = $('<div>').addClass('message-content');
        
        // Handle line breaks in the message
        const messageLines = message.split('\n');
        for (let i = 0; i < messageLines.length; i++) {
            const messageTextSpan = $('<span>').addClass('message-text').text(messageLines[i]);
            messageContentDiv.append(messageTextSpan);
            if (i !== messageLines.length - 1) {
                messageContentDiv.append('<br>');
            }
        }
        
        messageDiv.append(messageContentDiv);

        if (sender === 'You') {
            messageDiv.addClass('outgoing');
        } else {
            messageDiv.addClass('incoming');
        }

        chatDisplay.append(messageDiv);
        chatDisplay.scrollTop(chatDisplay[0].scrollHeight);
    }
});
