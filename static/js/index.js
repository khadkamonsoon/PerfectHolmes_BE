document.addEventListener('DOMContentLoaded', function() {
    const reservationButton = document.getElementById('reservationButton');
    reservationButton.addEventListener('click', function(event) {
        event.preventDefault();
        window.location.href = 'login/'; // 이동하고자 하는 URL 경로
    });
    
});
