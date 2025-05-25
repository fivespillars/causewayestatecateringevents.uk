/**
 * Main JavaScript file for The Causeway Estate website
 * Optimized for performance and modern browsers
 */

// Wait for the page to load
document.addEventListener('DOMContentLoaded', () => {
    initializeWebsite();
});

/**
 * Initialize all website functionality
 */
const initializeWebsite = () => {
    setActiveNavLink();
        initContactForm();
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
 * Contact form initialization and handling
 */
const initContactForm = () => {
    const form = document.getElementById('contactForm');
    if (!form) return;

    const showMessage = (type, text) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        form.insertAdjacentElement('beforebegin', messageDiv);
        setTimeout(() => messageDiv.remove(), 5000);
    };

    const validateEmail = (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    };
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get and sanitize form values
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validate form data
        if (!data.name?.trim() || !data.email?.trim() || !data.message?.trim()) {
            showMessage('error', 'Please fill in all fields');
            return;
        }

        if (!validateEmail(data.email)) {
            showMessage('error', 'Please enter a valid email address');
            return;
        }
        
        try {
        // Here you would typically send the form data to a server
            // For now, we'll simulate a successful submission
            await new Promise(resolve => setTimeout(resolve, 1000));
        
            showMessage('success', 'Thank you for your message! We will get back to you soon.');
        form.reset();
        } catch (error) {
            console.error('Form submission error:', error);
            showMessage('error', 'Sorry, there was an error sending your message. Please try again later.');
        }
    });
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
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const navbar = document.querySelector('.navbar');
    
    if (!mobileMenuButton || !navbar) return;

    mobileMenuButton.addEventListener('click', () => {
        navbar.classList.toggle('active');
        const isExpanded = navbar.classList.contains('active');
        mobileMenuButton.setAttribute('aria-expanded', isExpanded);
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
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    
    if (navbar?.classList.contains('active')) {
        navbar.classList.remove('active');
        mobileMenuButton?.setAttribute('aria-expanded', 'false');
            }
};

// Add page load performance tracking
window.addEventListener('load', () => {
    if (window.performance) {
        const timing = window.performance.timing;
        const pageLoadTime = timing.loadEventEnd - timing.navigationStart;
        console.log(`Page load time: ${pageLoadTime}ms`);
    }
});

document.addEventListener('DOMContentLoaded', function() {
  const hamburgerMenu = document.querySelector('.hamburger-menu');
  const navbar = document.querySelector('.navbar');

  hamburgerMenu.addEventListener('click', function() {
    navbar.style.display = navbar.style.display === 'none' ? 'flex' : 'none';
  });
}); 