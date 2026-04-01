// Dashboard State
let sidebarCollapsed = false;
let profileMenuOpen = false;
let activeTab = 'dashboard';

// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');
    
    if (!isLoggedIn || isLoggedIn !== 'true') {
        // Redirect to login page if not authenticated
        window.location.href = 'index.html';
        return;
    }
    
    // Load user data
    loadUserData();
    
    // Initialize dashboard
    initializeCharts();
    loadDashboardData();
    setupEventListeners();
});

// Load user data from session
function loadUserData() {
    const userName = sessionStorage.getItem('userName') || 'John';
    const userEmail = sessionStorage.getItem('userEmail') || 'john@example.com';
    
    // Update profile name
    const profileName = document.getElementById('profileName');
    if (profileName) {
        profileName.textContent = userName;
    }
    
    // Update welcome name
    const welcomeName = document.getElementById('welcomeName');
    if (welcomeName) {
        welcomeName.textContent = userName.split(' ')[0];
    }
    
    // Update avatar
    const avatar = document.getElementById('profileAvatar');
    if (avatar) {
        avatar.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(userName)}&background=6c5ce7&color=fff&size=40`;
    }
}

// Toggle Sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
    sidebarCollapsed = !sidebarCollapsed;
}

// Toggle Profile Menu
function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    menu.classList.toggle('show');
    profileMenuOpen = !profileMenuOpen;
}

// Close profile menu when clicking outside
document.addEventListener('click', function(e) {
    if (profileMenuOpen && !e.target.closest('.profile-dropdown')) {
        document.getElementById('profileMenu').classList.remove('show');
        profileMenuOpen = false;
    }
});

// Switch Tabs
function switchTab(tabName) {
    // Update active tab in sidebar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.closest('.nav-item').classList.add('active');
    
    // Show selected tab content
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabName + '-tab').classList.add('active');
    
    activeTab = tabName;
}

// Initialize Charts
function initializeCharts() {
    // Activity Chart
    const ctx1 = document.getElementById('activityChart');
    if (ctx1) {
        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'News Fetched',
                    data: [65, 78, 82, 94, 88, 72, 91],
                    borderColor: '#6c5ce7',
                    backgroundColor: 'rgba(108, 92, 231, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Posts Published',
                    data: [45, 52, 48, 61, 58, 43, 67],
                    borderColor: '#00b894',
                    backgroundColor: 'rgba(0, 184, 148, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                },
                scales: {
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                }
            }
        });
    }

    // Distribution Chart
    const ctx2 = document.getElementById('distributionChart');
    if (ctx2) {
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Facebook', 'Twitter', 'LinkedIn', 'Instagram'],
                datasets: [{
                    data: [45, 25, 20, 10],
                    backgroundColor: [
                        '#1877f2',
                        '#1da1f2',
                        '#0077b5',
                        '#e4405f'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                }
            }
        });
    }
}

// Load Dashboard Data
function loadDashboardData() {
    showNotification('Loading dashboard data...', 'info');
    
    setTimeout(() => {
        showNotification('Dashboard updated', 'success');
    }, 1000);
}

// Toggle API Key Visibility
function toggleVisibility(id) {
    const input = document.getElementById(id);
    const icon = event.target;
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    }
}

// API Functions
function openApiConfig() {
    switchTab('api-keys');
}

function testAllConnections() {
    showNotification('Testing all API connections...', 'info');
    
    setTimeout(() => {
        showNotification('All connections successful!', 'success');
    }, 2000);
}

function saveAllKeys() {
    showNotification('Saving all API keys...', 'info');
    
    setTimeout(() => {
        showNotification('API keys saved successfully!', 'success');
    }, 1500);
}

// Quick Actions
function runAutomation() {
    showNotification('Starting automation process...', 'info');
    
    setTimeout(() => {
        showNotification('Automation completed successfully!', 'success');
    }, 3000);
}

function scheduleAutomation() {
    showNotification('Opening scheduler...', 'info');
}

function fetchNews() {
    showNotification('Fetching latest news...', 'info');
    
    setTimeout(() => {
        showNotification('12 new articles fetched!', 'success');
    }, 2000);
}

function generateSummary() {
    showNotification('Generating summaries...', 'info');
    
    setTimeout(() => {
        showNotification('Summaries generated!', 'success');
    }, 2500);
}

function createImages() {
    showNotification('Generating images...', 'info');
    
    setTimeout(() => {
        showNotification('8 images created!', 'success');
    }, 3000);
}

function postToFacebook() {
    showNotification('Posting to Facebook...', 'info');
    
    setTimeout(() => {
        showNotification('Posted successfully!', 'success');
    }, 2000);
}

// Profile Functions
function showProfile() {
    showNotification('Opening profile settings...', 'info');
    toggleProfileMenu();
}

function showSettings() {
    showNotification('Opening system settings...', 'info');
    toggleProfileMenu();
}

function showActivity() {
    showNotification('Opening activity log...', 'info');
    toggleProfileMenu();
}

// Logout
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        showNotification('Logging out...', 'info');
        
        // Clear session
        sessionStorage.clear();
        
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
    }
}

// Notification System
function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icon = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    }[type];
    
    notification.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Event Listeners
function setupEventListeners() {
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            document.getElementById('sidebar').classList.add('collapsed');
        }
    });
}

// Export functions
window.toggleSidebar = toggleSidebar;
window.toggleProfileMenu = toggleProfileMenu;
window.switchTab = switchTab;
window.toggleVisibility = toggleVisibility;
window.openApiConfig = openApiConfig;
window.testAllConnections = testAllConnections;
window.saveAllKeys = saveAllKeys;
window.runAutomation = runAutomation;
window.scheduleAutomation = scheduleAutomation;
window.fetchNews = fetchNews;
window.generateSummary = generateSummary;
window.createImages = createImages;
window.postToFacebook = postToFacebook;
window.showProfile = showProfile;
window.showSettings = showSettings;
window.showActivity = showActivity;
window.handleLogout = handleLogout;