
  document.addEventListener('DOMContentLoaded', function() {
    const navbarToggle = document.getElementById('navbarToggle');
    const navbar = document.querySelector('.secondary_navbar');

    navbarToggle.addEventListener('click', function() {
      navbar.classList.toggle('show-navbar');
    });

    // Close navbar when clicking outside
    document.addEventListener('click', function(event) {
      if (!navbar.contains(event.target) && !navbarToggle.contains(event.target)) {
        navbar.classList.remove('show-navbar');
      }
    });
  });
