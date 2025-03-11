// Function to load HTML components
async function loadComponent(elementId, componentPath) {
    return new Promise(async (resolve, reject) => {
        try {
            const response = await fetch(componentPath);
            if (!response.ok) {
                throw new Error(`Failed to load ${componentPath}: ${response.status} ${response.statusText}`);
            }
            const html = await response.text();
            const targetElement = document.getElementById(elementId);
            
            if (!targetElement) {
                throw new Error(`Element with id "${elementId}" not found`);
            }

            targetElement.innerHTML = html;

            // If this is the navbar, initialize mobile menu functionality
            if (elementId === 'navbar') {
                initializeMobileMenu();
            }
            // If this is the footer, set the current year
            if (elementId === 'footer') {
                const yearElement = document.getElementById('currentYear');
                if (yearElement) {
                    yearElement.textContent = new Date().getFullYear();
                }
            }

            resolve();
        } catch (error) {
            console.error(`Error loading component ${componentPath}:`, error);
            reject(error);
        }
    });
}

// Initialize mobile menu functionality
function initializeMobileMenu() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileMenuBackdrop = document.querySelector('.mobile-menu-backdrop');
    const body = document.body;

    if (!mobileMenuButton || !mobileMenu || !mobileMenuBackdrop) {
        console.error('Mobile menu elements not found');
        return;
    }

    function toggleMobileMenu() {
        const isOpen = mobileMenu.classList.contains('hidden');
        mobileMenu.classList.toggle('hidden');
        mobileMenuBackdrop.classList.toggle('hidden');
        mobileMenuButton.setAttribute('aria-expanded', !isOpen);
        
        if (!isOpen) {
            body.style.overflow = 'auto';
        } else {
            body.style.overflow = 'hidden';
        }
    }

    mobileMenuButton.addEventListener('click', toggleMobileMenu);
    mobileMenuBackdrop.addEventListener('click', toggleMobileMenu);

    // Close mobile menu on window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 640) {
            mobileMenu.classList.add('hidden');
            mobileMenuBackdrop.classList.add('hidden');
            mobileMenuButton.setAttribute('aria-expanded', 'false');
            body.style.overflow = 'auto';
        }
    });

    // Close mobile menu when clicking a link
    document.querySelectorAll('.mobile-menu a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            mobileMenuBackdrop.classList.add('hidden');
            mobileMenuButton.setAttribute('aria-expanded', 'false');
            body.style.overflow = 'auto';
        });
    });
} 