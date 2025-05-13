// Header content
const headerContent = `
<nav class="navbar">
    <a href="index.html">Home</a>
    <a href="menu.html">Menu</a>
    <a href="about.html">About</a>
    <a href="catering.html">Catering</a>
    <a href="events.html">Events</a>
    <a href="contact.html">Contact</a>
</nav>
`;

// Footer content
const footerContent = `
<footer>
    <div class="contact-section">
        <div>
            <h3>Location</h3>
        <p>Herefordshire Golf Club</p>
        <p>The Causeway</p>
        <p>Hereford</p>
        <p>HR1 1DF</p>
    </div>
        <div>
            <h3>Opening Times</h3>
            <p>Monday - Sunday</p>
            <p>10:00 - 16:00</p>
    </div>
        <div>
            <h3>Contact</h3>
        <p>Phone: 01432 265 000</p>
            <p>Email: elaijah@causewayestate.com</p>
        </div>
    </div>
    <p>&copy; 2024 The Causeway Estate Catering. All rights reserved.</p>
</footer>
`;

// Function to include HTML content
document.addEventListener('DOMContentLoaded', function() {
    // Include header
    const headerElements = document.querySelectorAll('[include-html="components/header.html"]');
    headerElements.forEach(element => {
        element.innerHTML = headerContent;
    });
    
    // Include footer
    const footerElements = document.querySelectorAll('[include-html="components/footer.html"]');
    footerElements.forEach(element => {
        element.innerHTML = footerContent;
    });
}); 