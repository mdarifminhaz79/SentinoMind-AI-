// State Management
let isLoggedIn = false;

// Check if user is already logged in (from session)
document.addEventListener('DOMContentLoaded', function() {
    // Check if user was previously logged in
    const loggedIn = sessionStorage.getItem('isLoggedIn');
    if (loggedIn === 'true') {
        redirectToDashboard();
    }
});

// Login Handler
function handleLogin() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const loginBtn = document.getElementById('loginBtn');

    if (!email || !password) {
        showNotification('Please enter both email and password', 'error');
        return;
    }

    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }

    // Password validation (minimum 6 characters)
    if (password.length < 6) {
        showNotification('Password must be at least 6 characters', 'error');
        return;
    }

    // Show loading state
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
    loginBtn.disabled = true;

    // Simulate API call
    setTimeout(() => {
        // Store login state
        sessionStorage.setItem('isLoggedIn', 'true');
        sessionStorage.setItem('userEmail', email);
        sessionStorage.setItem('userName', email.split('@')[0]);
        
        // Show success message
        showNotification('Login successful! Redirecting...', 'success');
        
        // Redirect to dashboard
        setTimeout(() => {
            redirectToDashboard();
        }, 1000);
    }, 1500);
}

// Redirect to Dashboard
function redirectToDashboard() {
    window.location.href = 'dashboard.html';
}

// Social Login Handler
function handleSocialLogin(provider) {
    const loginBtn = document.querySelector('.social-btn.' + provider);
    const originalText = loginBtn.innerHTML;
    
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';
    loginBtn.disabled = true;
    
    showNotification(`Connecting to ${provider}...`, 'info');
    
    setTimeout(() => {
        // Store login state
        sessionStorage.setItem('isLoggedIn', 'true');
        sessionStorage.setItem('userName', provider === 'gmail' ? 'John Doe' : 'Jane Smith');
        sessionStorage.setItem('authProvider', provider);
        
        showNotification(`Successfully logged in with ${provider}!`, 'success');
        
        setTimeout(() => {
            redirectToDashboard();
        }, 1000);
    }, 1500);
}

// Toggle Password Visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Show Forgot Password
function showForgotPassword(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    
    if (!email) {
        showNotification('Please enter your email address', 'error');
        return;
    }
    
    showNotification(`Password reset link sent to ${email}`, 'success');
}

// Show Sign Up
function showSignUp(e) {
    e.preventDefault();
    showNotification('Redirecting to sign up page...', 'info');
    
    setTimeout(() => {
        window.location.href = 'signup.html';
    }, 1000);
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Add icon based on type
    let icon = '';
    switch(type) {
        case 'success':
            icon = 'fa-check-circle';
            break;
        case 'error':
            icon = 'fa-exclamation-circle';
            break;
        case 'info':
            icon = 'fa-info-circle';
            break;
    }
    
    notification.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 3000);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Handle Enter key
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        handleLogin();
    }
});

// Export functions for global use
window.handleLogin = handleLogin;
window.handleSocialLogin = handleSocialLogin;
window.togglePassword = togglePassword;
window.showForgotPassword = showForgotPassword;
window.showSignUp = showSignUp;