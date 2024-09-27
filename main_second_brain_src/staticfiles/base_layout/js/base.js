document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");
    
    const toggleButton = document.getElementById('navbar_toogle');
    const navbar = document.getElementById('base_navbar');

    console.log("toggleButton:", toggleButton);
    console.log("navbar:", navbar);

    if (toggleButton && navbar) {
        toggleButton.addEventListener('click', function() {
            console.log("Toggle button clicked");
            navbar.classList.toggle('visible');
            toggleButton.classList.toggle('flipped');
        });
    } else {
        console.error('Element not found');
    }
});
