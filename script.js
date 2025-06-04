/**
 * Main JavaScript file for The Causeway Estate website
 * Optimized for performance and modern browsers
 */

// Wait for the page to load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing website...');
    initializeWebsite();
    loadFooter();
});

/**
 * Initialize all website functionality
 */
const initializeWebsite = () => {
    console.log('Initializing website functionality...');
    setActiveNavLink();
    initAllForms();
    initSmoothScroll();
    initMobileNavigation();
};

/**
 * Set active navigation link based on current page
 */
const setActiveNavLink = () => {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.navbar a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });
};

/**
 * Initialize all forms on the page
 */
const initAllForms = () => {
    console.log('Initializing all forms...');
    // No more JS for mini contact forms; let browser handle them natively
    // Initialize main contact form
    initContactForm();
};

/**
 * Initialize main contact form
 */
const initContactForm = () => {
    const form = document.getElementById('contactForm');
    if (!form) return;
    console.log('Initializing main contact form');

    const validateEmail = (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    };
    
    form.addEventListener('submit', async (e) => {
        console.log('Main contact form submitted');
        e.preventDefault();
        
        // Get and sanitize form values
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validate form data
        if (!data.name?.trim() || !data.email?.trim() || !data.message?.trim()) {
            console.log('Form validation failed - missing fields');
            return;
        }

        if (!validateEmail(data.email)) {
            console.log('Form validation failed - invalid email');
            return;
        }
        
        try {
        // Here you would typically send the form data to a server
            // For now, we'll simulate a successful submission
            await new Promise(resolve => setTimeout(resolve, 1000));
        
            showThankYouPopup('Your message has been sent successfully. We\'ll get back to you soon.');
        form.reset();
        } catch (error) {
            console.error('Form submission error:', error);
        }
    });
};

// Add to global scope for the onclick handler
window.closeThankYouPopup = () => {
    console.log('Closing thank you popup');
    const overlay = document.querySelector('.thank-you-overlay');
    const popup = document.querySelector('.thank-you-popup');
    if (overlay) overlay.classList.remove('active');
    if (popup) popup.classList.remove('active');
};

/**
 * Smooth scrolling implementation
 */
const initSmoothScroll = () => {
    document.addEventListener('click', (e) => {
        const anchor = e.target.closest('a[href^="#"]');
        if (!anchor) return;
        
        e.preventDefault();
        const targetId = anchor.getAttribute('href');
        const target = document.querySelector(targetId);
        
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            closeMobileMenu();
        }
    });
};

/**
 * Mobile navigation handling
 */
const initMobileNavigation = () => {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const navbar = document.querySelector('.navbar');
    if (!hamburgerMenu || !navbar) return;
    hamburgerMenu.addEventListener('click', () => {
        const isActive = navbar.classList.toggle('active');
        hamburgerMenu.setAttribute('aria-expanded', isActive);
    });
    // Close menu on window resize (if switching to desktop view)
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (window.innerWidth > 768) {
                closeMobileMenu();
            }
        }, 250);
    });
};

/**
 * Helper function to close mobile menu
 */
const closeMobileMenu = () => {
    const navbar = document.querySelector('.navbar');
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    if (navbar?.classList.contains('active')) {
        navbar.classList.remove('active');
        hamburgerMenu?.setAttribute('aria-expanded', 'false');
    }
};

// Add page load performance tracking
window.addEventListener('load', () => {
    if (window.performance) {
        const timing = window.performance.timing;
        const pageLoadTime = timing.loadEventEnd - timing.navigationStart;
    }
});

// Load footer component
async function loadFooter() {
    try {
        const response = await fetch('components/footer.html');
        const html = await response.text();
        document.querySelector('footer').outerHTML = html;
    } catch (error) {
        console.error('Error loading footer:', error);
            }
} 