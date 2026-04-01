console.log("SentinoMind AI Script: Active");

const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault(); 
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const btn = document.querySelector('.login-btn');

        if (email && password) {
            console.log("Inputs validated. Starting transition...");
            
            // UI Feedback
            btn.innerHTML = "<span>Initializing Neural Core...</span>";
            btn.style.opacity = "0.7";
            btn.style.pointerEvents = "none"; 

            // Single Redirect Logic
            setTimeout(() => {
                console.log("Attempting to load: dashboard.html");
                window.location.assign("dashboard.html"); 
            }, 1200);
            
        } else {
            alert("Credentials required to access SentinoMind AI.");
        }
    });
} else {
    console.error("Error: Could not find 'loginForm' on this page.");
}
// 1. Grab the elements
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');

// 2. Check if they exist before adding the listener
if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => {
        console.log("Menu button clicked!"); // Check your browser console (F12) for this
        sidebar.classList.toggle('open');
        
        // Dynamic icon change
        menuBtn.innerText = sidebar.classList.contains('open') ? '✕' : '☰';
    });
} else {
    console.error("Could not find menuBtn or sidebar in the HTML.");
}