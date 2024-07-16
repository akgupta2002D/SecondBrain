document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');

    const navbarToggle = document.getElementById('navbarToggle');
    const navbar = document.querySelector('.exam_quest_dashboard_navbar');
    
    console.log('navbarToggle:', navbarToggle);
    console.log('navbar:', navbar);

    if (navbarToggle && navbar) {
        navbarToggle.addEventListener('click', function(event) {
            console.log('Navbar toggle clicked');
            event.stopPropagation();
            navbar.classList.toggle('show-navbar');
            console.log('show-navbar class toggled:', navbar.classList.contains('show-navbar'));
        });

        // Close navbar when clicking outside
        document.addEventListener('click', function(event) {
            console.log('Document clicked');
            if (!navbar.contains(event.target) && !navbarToggle.contains(event.target)) {
                console.log('Clicked outside navbar, removing show-navbar class');
                navbar.classList.remove('show-navbar');
            }
        });
    } else {
        console.error('Navbar toggle or navbar element not found');
    }
});