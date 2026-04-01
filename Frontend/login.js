// login.js - SentinoMind Neural Login System

console.log("🤖 SentinoMind Neural Login System Active");

// Check for existing session
if (localStorage.getItem("sentino_session")) {
    window.location.href = "dashboard.html";
}

// DOM Elements
const loginForm = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const loginBtn = document.getElementById("loginBtn");
const togglePassword = document.getElementById("togglePassword");
const rememberCheck = document.getElementById("remember");
const forgotBtn = document.getElementById("forgotPassword");
const createAccountBtn = document.getElementById("createAccountBtn"); // Changed to button ID

// Load saved email if "remember me" was checked
if (localStorage.getItem("remembered_email")) {
    emailInput.value = localStorage.getItem("remembered_email");
    rememberCheck.checked = true;
}

// Check for newly created profile email
const newProfileEmail = localStorage.getItem("new_profile_email");
if (newProfileEmail) {
    emailInput.value = newProfileEmail;
    localStorage.removeItem("new_profile_email");
    showToast("✅ Neural profile created! Please login", "success");
}

// Toggle password visibility
togglePassword.addEventListener("click", function() {
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
    passwordInput.setAttribute("type", type);
    
    // Toggle icon
    const icon = this.querySelector("i");
    icon.classList.toggle("fa-eye");
    icon.classList.toggle("fa-eye-slash");
    
    // Neural effect
    this.style.transform = "scale(1.1)";
    setTimeout(() => this.style.transform = "scale(1)", 200);
});

// Input validation with neural effects
emailInput.addEventListener("input", function() {
    if (isValidEmail(this.value)) {
        this.style.borderColor = "var(--success)";
        this.style.boxShadow = "0 0 20px var(--success)";
        
        // Add neural pulse to icon
        const icon = this.parentElement.querySelector(".input-icon");
        icon.style.color = "var(--success)";
        icon.style.transform = "scale(1.1)";
        setTimeout(() => icon.style.transform = "scale(1)", 200);
    } else {
        this.style.borderColor = "";
        this.style.boxShadow = "";
        
        const icon = this.parentElement.querySelector(".input-icon");
        icon.style.color = "";
    }
});

passwordInput.addEventListener("input", function() {
    if (this.value.length >= 6) {
        this.style.borderColor = "var(--success)";
        this.style.boxShadow = "0 0 20px var(--success)";
        
        const icon = this.parentElement.querySelector(".input-icon");
        icon.style.color = "var(--success)";
    } else {
        this.style.borderColor = "";
        this.style.boxShadow = "";
        
        const icon = this.parentElement.querySelector(".input-icon");
        icon.style.color = "";
    }
});

// Forgot password handler
forgotBtn.addEventListener("click", function(e) {
    e.preventDefault();
    
    if (emailInput.value && isValidEmail(emailInput.value)) {
        showToast("🔐 Neural recovery code sent to " + emailInput.value, "info");
        
        // Neural animation on the button
        this.style.transform = "scale(1.05)";
        setTimeout(() => this.style.transform = "scale(1)", 200);
    } else {
        showToast("⚠️ Please enter your neural email first", "error");
        emailInput.focus();
    }
});

// Create account button handler - FIXED VERSION
if (createAccountBtn) {
    createAccountBtn.addEventListener("click", function(e) {
        e.preventDefault(); // Prevent any default button behavior
        
        // Neural effect
        this.style.transform = "scale(1.05)";
        this.style.boxShadow = "0 0 30px var(--accent-cyan)";
        
        // Disable button temporarily to prevent double-click
        this.disabled = true;
        
        // Navigate to create profile page after animation
        setTimeout(() => {
            window.location.href = "create-profile.html";
        }, 300);
    });
}

// Login form submission
loginForm.addEventListener("submit", async function(e) {
    e.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    // Validation
    if (!email || !password) {
        showToast("⚠️ Neural credentials required", "error");
        shakeForm();
        return;
    }

    if (!isValidEmail(email)) {
        showToast("📧 Invalid neural signature (email)", "error");
        emailInput.focus();
        shakeForm();
        return;
    }

    if (password.length < 6) {
        showToast("🔑 Password must be at least 6 characters", "error");
        passwordInput.focus();
        shakeForm();
        return;
    }

    // Neural authentication simulation
    await authenticateNeural(email, password);
});

// Email validation
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Shake animation for errors
function shakeForm() {
    loginForm.style.animation = "shake 0.5s ease";
    
    // Neural status dot flashes red
    const statusDot = document.querySelector(".status-dot");
    const originalColor = statusDot.style.backgroundColor;
    statusDot.style.backgroundColor = "var(--danger)";
    statusDot.style.boxShadow = "0 0 20px var(--danger)";
    
    setTimeout(() => {
        loginForm.style.animation = "";
        statusDot.style.backgroundColor = "";
        statusDot.style.boxShadow = "";
    }, 500);
}

// Authentication simulation
async function authenticateNeural(email, password) {
    // Disable form
    loginBtn.disabled = true;
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Accessing Neural Core...';

    // Simulate API call with progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += 20;
        loginBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Neural handshake ${progress}%...`;
    }, 400);

    await new Promise(resolve => setTimeout(resolve, 2000));
    clearInterval(interval);

    // Neural pulse animation
    const statusDot = document.querySelector(".status-dot");
    statusDot.style.animation = "pulse 0.5s 3";
    
    // Check if profile exists (simulated)
    const profileExists = checkProfileExists(email);
    
    if (!profileExists) {
        // Suggest creating profile
        showToast("🔮 Neural profile not found. Create one?", "info");
        loginBtn.disabled = false;
        loginBtn.innerHTML = '<span>Access Neural Core</span><i class="fas fa-arrow-right"></i>';
        
        // Show create account suggestion
        setTimeout(() => {
            if (confirm("No neural profile found. Would you like to create one?")) {
                window.location.href = "create-profile.html";
            }
        }, 500);
        return;
    }
    
    // Success - create session
    localStorage.setItem("sentino_session", Date.now().toString());
    localStorage.setItem("user_email", email);
    
    // Save profile data if exists
    const profileData = localStorage.getItem("neural_profile");
    if (profileData) {
        const profile = JSON.parse(profileData);
        localStorage.setItem("user_name", profile.fullName || email.split('@')[0]);
    }
    
    if (rememberCheck.checked) {
        localStorage.setItem("remembered_email", email);
    } else {
        localStorage.removeItem("remembered_email");
    }

    showToast("✅ Neural connection established!", "success");

    // Update status
    document.querySelector(".neural-status span").textContent = "Neural Grid: Connected";
    document.querySelector(".status-dot").style.backgroundColor = "var(--success)";

    // Neural glow effect
    document.querySelector(".login-card").style.boxShadow = "0 0 50px rgba(0, 240, 255, 0.5)";

    // Redirect with fade out
    document.body.style.opacity = "0";
    document.body.style.transition = "opacity 0.5s";
    
    setTimeout(() => {
        window.location.href = "dashboard.html";
    }, 500);
}

// Check if profile exists (simulated)
function checkProfileExists(email) {
    const profileData = localStorage.getItem("neural_profile");
    if (!profileData) return false;
    
    try {
        const profile = JSON.parse(profileData);
        return profile.email === email;
    } catch {
        return false;
    }
}

// Toast notification system
function showToast(message, type = "info") {
    const toastContainer = document.getElementById("toast");
    const toast = document.createElement("div");
    
    const icons = {
        success: "fa-check-circle",
        error: "fa-exclamation-circle",
        info: "fa-info-circle"
    };
    
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = "slideOut 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add CSS animations if not present
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .toast {
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// Neural grid status simulation
setInterval(() => {
    const statusDot = document.querySelector(".status-dot");
    if (statusDot && !loginBtn.disabled) {
        statusDot.style.opacity = "0.5";
        setTimeout(() => statusDot.style.opacity = "1", 500);
    }
}, 3000);

// Focus on email input on load
window.addEventListener('load', () => {
    setTimeout(() => {
        emailInput.focus();
    }, 500);
});