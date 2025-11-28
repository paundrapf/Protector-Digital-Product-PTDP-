// PTDP Landing Page - Gen-Z Vibes JavaScript

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.style.boxShadow = 'none';
    } else {
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
    }
    
    lastScroll = currentScroll;
});

// Scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('.feature-card, .step, .download-card, .faq-item').forEach(el => {
    observer.observe(el);
});

// Download functions
function downloadViewer(platform) {
    // Show notification
    showNotification(`Downloading PTDP Viewer for ${platform}... 🚀`);
    
    // In production, this would trigger actual download
    const downloadUrls = {
        windows: '/downloads/PTDP-Viewer-Windows.exe',
        mac: '/downloads/PTDP-Viewer-macOS.dmg',
        linux: '/downloads/PTDP-Viewer-Linux.AppImage'
    };
    
    // Simulate download
    setTimeout(() => {
        console.log(`Download started for ${platform} viewer`);
        showNotification(`Download started! Check your downloads folder 📥`, 'success');
    }, 500);
}

function downloadCreator(platform) {
    showNotification(`Downloading PTDP Creator for ${platform}... 🎨`);
    
    const downloadUrls = {
        windows: '/downloads/PTDP-Creator-Windows.exe',
        mac: '/downloads/PTDP-Creator-macOS.dmg',
        linux: '/downloads/PTDP-Creator-Linux.AppImage'
    };
    
    setTimeout(() => {
        console.log(`Download started for ${platform} creator`);
        showNotification(`Download started! Time to create some magic ✨`, 'success');
    }, 500);
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notification if any
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Add styles if not exist
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 100px;
                right: 24px;
                z-index: 10000;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 20px 24px;
                color: white;
                font-family: 'Inter', sans-serif;
                font-size: 16px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                animation: slideInRight 0.4s ease-out, fadeOut 0.4s ease-out 4.6s;
                max-width: 400px;
            }
            
            .notification.success {
                border-color: #4CAF50;
                background: rgba(76, 175, 80, 0.1);
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
            }
            
            .notification-close {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                opacity: 0.7;
                transition: opacity 0.3s;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .notification-close:hover {
                opacity: 1;
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes fadeOut {
                to {
                    opacity: 0;
                    transform: translateX(400px);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Particle effect on hero
function createParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    particlesContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
    `;
    
    hero.appendChild(particlesContainer);
    
    // Create floating particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: rgba(255, 107, 157, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float-particle ${Math.random() * 10 + 10}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        particlesContainer.appendChild(particle);
    }
    
    // Add particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float-particle {
            0%, 100% {
                transform: translate(0, 0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Mouse parallax effect
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth) - 0.5;
    mouseY = (e.clientY / window.innerHeight) - 0.5;
    
    // Apply parallax to floating cards
    document.querySelectorAll('.floating-card').forEach((card, index) => {
        const speed = (index + 1) * 10;
        card.style.transform = `
            translateX(${mouseX * speed}px) 
            translateY(${mouseY * speed}px)
        `;
    });
});

// Counter animation for stats
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = counter.textContent;
        const isPercentage = target.includes('%');
        const isPlus = target.includes('+');
        const numericValue = parseInt(target.replace(/[^0-9]/g, ''));
        
        let current = 0;
        const increment = numericValue / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= numericValue) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                let displayValue = Math.floor(current);
                if (isPlus) displayValue += 'K+';
                if (isPercentage) displayValue += '%';
                counter.textContent = displayValue;
            }
        }, 30);
    });
}

// Trigger counter animation when in view
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.hero-stats');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// Initialize effects
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    
    // Add loading animation
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

// Easter egg - Konami code
let konamiCode = [];
const konamiPattern = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join('') === konamiPattern.join('')) {
        showNotification('🎮 Cheat code activated! You\'re a real one 💯', 'success');
        document.body.style.animation = 'rainbow 2s ease-in-out';
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes rainbow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }
});

// Performance optimization - Lazy load images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

console.log('%c PTDP Protection System ', 'background: linear-gradient(135deg, #FF6B9D, #C371F6); color: white; font-size: 20px; font-weight: bold; padding: 10px;');
console.log('%c Built with 💜 by Gen-Z for Gen-Z ', 'color: #FF6B9D; font-size: 14px;');
console.log('%c No cap, this is the future of PDF protection 🔥 ', 'color: #C371F6; font-size: 12px;');

// Download handlers
document.addEventListener('DOMContentLoaded', () => {
    const downloadButtons = document.querySelectorAll('.download-btn');
    
    downloadButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const type = btn.dataset.type;
            const platform = btn.dataset.platform || 'Linux';
            const filename = `PTDP-${type}-${platform}`;
            const filesize = type === 'Viewer' ? '32.3 MB' : '31.4 MB';
            
            showNotification(`Starting download: PTDP ${type} for ${platform} (${filesize}) 🚀`);
            
            // Trigger actual download
            const link = document.createElement('a');
            link.href = `/downloads/${filename}`;
            link.download = filename;
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Show success message
            setTimeout(() => {
                showNotification(`✓ Downloaded! File: ${filename}`);
            }, 1000);
        });
    });
});

// Windows installer download
function downloadInstaller(platform) {
    showNotification(`🪟 Preparing Windows installer download...`);
    
    setTimeout(() => {
        const link = document.createElement('a');
        link.href = `downloads/PTDP-Setup-${platform}.exe`;
        link.download = `PTDP-Setup-${platform}.exe`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showNotification('✓ Download started! Check your Downloads folder.');
        
        // Show additional info
        setTimeout(() => {
            showNotification('💡 Run the installer to install both Creator & Viewer');
        }, 2000);
    }, 500);
}

// Portable executable download (SUPER USER FRIENDLY!)
function downloadPortable(type) {
    const filename = `PTDP-${type}.exe`;
    
    showNotification(`🚀 Downloading ${type}...`);
    
    setTimeout(() => {
        const link = document.createElement('a');
        link.href = `downloads/${filename}`;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showNotification(`✓ ${filename} downloaded!`);
        
        // Show usage instructions
        setTimeout(() => {
            showNotification(`💡 Just double-click ${filename} to run - no installation needed!`);
        }, 1500);
        
        // Remind about Windows warning
        setTimeout(() => {
            showNotification('ℹ️ If Windows shows a warning, click "More info" → "Run anyway"');
        }, 3500);
    }, 500);
}
