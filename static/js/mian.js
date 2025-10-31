// // Mobile Menu Toggle
// document.addEventListener('DOMContentLoaded', () => {
//     const navbarToggler = document.getElementById('navbarToggler');
//     const navbarMenu = document.getElementById('navbarMenu');
    
//     if (navbarToggler) {
//         navbarToggler.addEventListener('click', () => {
//             navbarMenu.classList.toggle('active');
//             navbarToggler.classList.toggle('active');
//         });
//     }
    
//     // Close mobile menu when clicking outside
//     document.addEventListener('click', (e) => {
//         if (!e.target.closest('.navbar') && navbarMenu.classList.contains('active')) {
//             navbarMenu.classList.remove('active');
//             navbarToggler.classList.remove('active');
//         }
//     });
    
//     // Active nav link highlighting
//     const currentPage = window.location.pathname;
//     document.querySelectorAll('.nav-link').forEach(link => {
//         if (link.getAttribute('href') === currentPage) {
//             link.style.color = 'var(--primary-color)';
//             link.style.backgroundColor = 'rgba(79, 70, 229, 0.1)';
//         }
//     });
// });

// // Smooth Scroll
// document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//     anchor.addEventListener('click', function (e) {
//         e.preventDefault();
//         const target = document.querySelector(this.getAttribute('href'));
//         if (target) {
//             target.scrollIntoView({ behavior: 'smooth' });
//         }
//     });
// });

// // Loading State Helper
// function setLoading(button, isLoading) {
//     if (isLoading) {
//         button.disabled = true;
//         button.dataset.originalText = button.textContent;
//         button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
//     } else {
//         button.disabled = false;
//         button.textContent = button.dataset.originalText;
//     }
// }

// // Toast Notification
// function showToast(message, type = 'success') {
//     const toast = document.createElement('div');
//     toast.className = `toast toast-${type}`;
//     toast.textContent = message;
//     toast.style.cssText = `
//         position: fixed;
//         top: 20px;
//         right: 20px;
//         padding: 16px 24px;
//         background: ${type === 'success' ? '#10B981' : '#EF4444'};
//         color: white;
//         border-radius: 8px;
//         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
//         z-index: 9999;
//         animation: slideIn 0.3s ease-out;
//     `;
    
//     document.body.appendChild(toast);
    
//     setTimeout(() => {
//         toast.style.animation = 'slideOut 0.3s ease-out';
//         setTimeout(() => toast.remove(), 300);
//     }, 3000);
// }

// // Add animations
// const style = document.createElement('style');
// style.textContent = `
//     @keyframes slideIn {
//         from { transform: translateX(100%); opacity: 0; }
//         to { transform: translateX(0); opacity: 1; }
//     }
//     @keyframes slideOut {
//         from { transform: translateX(0); opacity: 1; }
//         to { transform: translateX(100%); opacity: 0; }
//     }
// `;
// document.head.appendChild(style);