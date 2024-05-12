document.addEventListener('DOMContentLoaded', function () {
    var messagesContainer = document.querySelector('.messages-container');

    if (messagesContainer) {
        setTimeout(function () {
            messagesContainer.style.opacity = '0';
            setTimeout(function () {
                messagesContainer.style.display = 'none';
            }, 500);
        }, 5000); // Disappear after 5 seconds
    }
});