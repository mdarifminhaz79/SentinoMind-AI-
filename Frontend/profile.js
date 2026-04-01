// profile.js - Neural Profile Creation System

console.log("🧬 SentinoMind Neural Profile Creator Active");

// Check if already logged in
if (localStorage.getItem("sentino_session")) {
    window.location.href = "dashboard.html";
}

// ===== DOM Elements =====
const form = document.getElementById("profileForm");
const steps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".step");
const passwordInput = document.getElementById("profilePassword");
const confirmInput = document.getElementById("confirmPassword");
const securityNextBtn = document.getElementById("securityNextBtn");
const createBtn = document.getElementById("createProfileBtn");
const modal = document.getElementById("successModal");
const usernameInput = document.getElementById("username");
const fullNameInput = document.getElementById("fullName");
const emailInput = document.getElementById("profileEmail");

// ===== Particle Network Background =====
function createParticles() {
    const particlesContainer = document.getElementById("particles");
    if (!particlesContainer) return;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement("div");
        particle.className = "particle";
        particle.style.left = Math.random() * 100 + "%";
        particle.style.top = Math.random() * 100 + "%";
        particle.style.animationDelay = Math.random() * 5 + "s";
        particle.style.width = particle.style.height = Math.random() * 3 + 1 + "px";
        particlesContainer.appendChild(particle);
    }
}
createParticles();

// ===== Step Navigation =====
window.nextStep = function(step) {
    // Validate current step before proceeding
    if (step === 2 && !validateStep1()) {
        showToast("⚠️ Please complete all neural identity fields", "error");
        return;
    }
    
    if (step === 3 && !validateStep2()) {
        showToast("⚠️ Neural security requirements not met", "error");
        return;
    }
    
    // Update steps visibility
    steps.forEach(s => s.classList.remove("active"));
    document.getElementById(`step${step}`).classList.add("active");
    
    // Update progress indicators
    progressSteps.forEach((s, index) => {
        if (index + 1 < step) {
            s.classList.add("completed");
            s.classList.remove("active");
        } else if (index + 1 === step) {
            s.classList.add("active");
            s.classList.remove("completed");
        } else {
            s.classList.remove("active", "completed");
        }
    });
    
    // Neural pulse animation
    animateNeuralPulse();
    
    // Update neural ID preview in step 3
    if (step === 3) {
        updateNeuralIdPreview();
    }
};

window.prevStep = function(step) {
    steps.forEach(s => s.classList.remove("active"));
    document.getElementById(`step${step}`).classList.add("active");
    
    progressSteps.forEach((s, index) => {
        if (index + 1 <= step) {
            s.classList.add("active");
            s.classList.remove("completed");
        } else {
            s.classList.remove("active", "completed");
        }
    });
    
    animateNeuralPulse();
};

// ===== Validation Functions =====
function validateStep1() {
    const fullName = fullNameInput.value.trim();
    const email = emailInput.value.trim();
    const username = usernameInput.value.trim();
    const role = document.getElementById("neuralRole").value;
    
    let isValid = true;
    
    // Validate full name
    if (fullName.length < 3) {
        showFieldError(fullNameInput, "Neural designation too short");
        isValid = false;
    } else {
        showFieldSuccess(fullNameInput);
    }
    
    // Validate email
    if (!isValidEmail(email)) {
        showFieldError(emailInput, "Invalid neural email format");
        isValid = false;
    } else {
        showFieldSuccess(emailInput);
    }
    
    // Validate username
    if (username.length < 4 || !/^[a-zA-Z0-9_]+$/.test(username)) {
        showFieldError(usernameInput, "Username must be 4+ chars (letters, numbers, _)");
        isValid = false;
    } else {
        showFieldSuccess(usernameInput);
    }
    
    // Validate role
    if (!role) {
        showToast("⚠️ Please select a neural function", "error");
        isValid = false;
    }
    
    return isValid;
}

function validateStep2() {
    const password = passwordInput.value;
    const confirm = confirmInput.value;
    
    const requirements = {
        length: password.length >= 8,
        number: /[0-9]/.test(password),
        uppercase: /[A-Z]/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
        match: password === confirm && password !== ""
    };
    
    // Update requirement indicators
    for (let [req, met] of Object.entries(requirements)) {
        const element = document.getElementById(`req-${req}`);
        if (element) {
            const icon = element.querySelector("i");
            if (met) {
                icon.className = "fas fa-check-circle";
                icon.style.color = "var(--success)";
                element.classList.add("met");
            } else {
                icon.className = "far fa-circle";
                icon.style.color = "";
                element.classList.remove("met");
            }
        }
    }
    
    // Update strength meter
    updatePasswordStrength(password);
    
    // Check all requirements met
    const allMet = Object.values(requirements).every(v => v === true);
    securityNextBtn.disabled = !allMet;
    
    return allMet;
}

function validateStep3() {
    return document.getElementById("termsConsent").checked;
}

// ===== Password Strength Meter =====
function updatePasswordStrength(password) {
    const bars = document.querySelectorAll(".strength-bars .bar");
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
    
    bars.forEach((bar, index) => {
        if (index < strength) {
            bar.style.background = index === 0 ? "#ff4d4d" :
                                  index === 1 ? "#ffb800" :
                                  index === 2 ? "#00f0ff" : "#00ff9d";
            bar.style.opacity = "1";
        } else {
            bar.style.background = "";
            bar.style.opacity = "0.3";
        }
    });
}

// ===== Neural ID Preview =====
function updateNeuralIdPreview() {
    const username = usernameInput.value.trim() || "user";
    const timestamp = Date.now().toString().slice(-6);
    const neuralId = `SM-${username.toUpperCase()}-${timestamp}`;
    
    document.querySelector("#neuralIdPreview span").textContent = neuralId;
}

// ===== Password Toggle =====
window.togglePassword = function(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector("i");
    
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
    
    // Neural effect
    btn.style.transform = "scale(1.1)";
    setTimeout(() => btn.style.transform = "scale(1)", 200);
};

// ===== Field Validation Helpers =====
function showFieldError(field, message) {
    field.style.borderColor = "var(--danger)";
    field.style.boxShadow = "0 0 10px var(--danger)";
    
    const validator = field.closest(".input-group").querySelector(".input-validator");
    if (validator) {
        validator.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
        validator.style.color = "var(--danger)";
        validator.style.opacity = "1";
    }
}

function showFieldSuccess(field) {
    field.style.borderColor = "var(--success)";
    field.style.boxShadow = "0 0 10px var(--success)";
    
    const validator = field.closest(".input-group").querySelector(".input-validator");
    if (validator) {
        validator.innerHTML = `<i class="fas fa-check-circle"></i> Valid`;
        validator.style.color = "var(--success)";
        validator.style.opacity = "1";
    }
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ===== Real-time Validation =====
passwordInput.addEventListener("input", () => validateStep2());
confirmInput.addEventListener("input", () => validateStep2());

usernameInput.addEventListener("input", function() {
    if (this.value.length >= 4 && /^[a-zA-Z0-9_]+$/.test(this.value)) {
        showFieldSuccess(this);
    } else {
        showFieldError(this, "Invalid username format");
    }
    updateNeuralIdPreview();
});

emailInput.addEventListener("input", function() {
    if (isValidEmail(this.value)) {
        showFieldSuccess(this);
    } else {
        showFieldError(this, "Invalid email format");
    }
});

fullNameInput.addEventListener("input", function() {
    if (this.value.length >= 3) {
        showFieldSuccess(this);
    } else {
        showFieldError(this, "Name too short");
    }
});

// ===== Form Submission =====
form.addEventListener("submit", async function(e) {
    e.preventDefault();
    
    if (!validateStep3()) {
        showToast("⚠️ Please accept the Neural Network Terms", "error");
        return;
    }
    
    // Disable button
    createBtn.disabled = true;
    createBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Initializing Neural Profile...';
    
    // Neural initialization animation
    animateNeuralInit();
    
    // Simulate neural profile creation
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Generate neural profile data
    const neuralId = document.querySelector("#neuralIdPreview span").textContent;
    const timestamp = new Date().toLocaleTimeString();
    
    // Save to localStorage
    const profileData = {
        fullName: fullNameInput.value.trim(),
        email: emailInput.value.trim(),
        username: usernameInput.value.trim(),
        neuralId: neuralId,
        role: document.getElementById("neuralRole").value,
        modules: {
            main: document.getElementById("moduleMain").checked,
            vision: document.getElementById("moduleVision").checked,
            audio: document.getElementById("moduleAudio").checked,
            predictive: document.getElementById("modulePredictive").checked
        },
        quantumEncryption: document.getElementById("quantumConsent").checked,
        createdAt: new Date().toISOString()
    };
    
    localStorage.setItem("neural_profile", JSON.stringify(profileData));
    
    // Show success modal
    document.getElementById("modalNeuralId").textContent = neuralId;
    document.getElementById("modalTime").textContent = timestamp;
    modal.style.display = "flex";
    
    showToast("✅ Neural profile created successfully!", "success");
});

// ===== Animation Functions =====
function animateNeuralPulse() {
    const cards = document.querySelectorAll(".module-card");
    cards.forEach((card, i) => {
        setTimeout(() => {
            card.style.transform = "scale(1.02)";
            setTimeout(() => card.style.transform = "", 200);
        }, i * 100);
    });
}

function animateNeuralInit() {
    const steps = document.querySelectorAll(".progress-steps .step");
    steps.forEach(step => {
        step.style.animation = "pulse 0.5s 3";
    });
}

// ===== Redirect =====
window.redirectToLogin = function() {
    // Auto-fill login form with email
    localStorage.setItem("new_profile_email", emailInput.value.trim());
    window.location.href = "index.html";
};

// ===== Toast Notification =====
function showToast(message, type = "info") {
    const toastContainer = document.getElementById("toast");
    const toast = document.createElement("div");
    
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 
                         type === 'error' ? 'fa-exclamation-circle' : 
                         'fa-info-circle'}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = "slideOut 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== Initialize =====
document.addEventListener("DOMContentLoaded", function() {
    // Check for prefilled email from login page
    const prefilledEmail = localStorage.getItem("new_profile_email");
    if (prefilledEmail) {
        emailInput.value = prefilledEmail;
        localStorage.removeItem("new_profile_email");
    }
    
    // Focus on first input
    setTimeout(() => {
        fullNameInput.focus();
    }, 500);
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    .slideOut {
        animation: slideOut 0.3s ease forwards;
    }
    
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);