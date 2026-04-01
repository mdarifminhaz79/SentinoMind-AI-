// dashboard.js - SentinoMind Automation System

console.log("🤖 SentinoMind Automation System Active");

// Session Protection
if (!localStorage.getItem("sentino_session")) {
    window.location.href = "index.html";
}

// DOM Elements
const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");
const logoutBtn = document.getElementById("logoutBtn");
const contentArea = document.getElementById("content-area");
const userEmailSpan = document.getElementById("userEmail");
const systemTimeSpan = document.getElementById("systemTime");

// Load user data
const userEmail = localStorage.getItem("user_email") || "operator@sentinomind.ai";
userEmailSpan.textContent = userEmail;

// ===== SIDEBAR TOGGLE =====
menuBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    
    const icon = menuBtn.querySelector("i");
    if (sidebar.classList.contains("open")) {
        icon.className = "fas fa-times";
        menuBtn.style.left = "360px";
    } else {
        icon.className = "fas fa-bars";
        menuBtn.style.left = "20px";
    }
});

// Close sidebar on outside click
document.addEventListener("click", (e) => {
    if (!sidebar.contains(e.target) && !menuBtn.contains(e.target) && sidebar.classList.contains("open")) {
        sidebar.classList.remove("open");
        menuBtn.querySelector("i").className = "fas fa-bars";
        menuBtn.style.left = "20px";
    }
});

// ===== UPDATE SYSTEM TIME =====
function updateSystemTime() {
    const now = new Date();
    systemTimeSpan.textContent = now.toLocaleTimeString() + " UTC";
}
updateSystemTime();
setInterval(updateSystemTime, 1000);

// ===== TOGGLE API KEY VISIBILITY =====
document.querySelectorAll(".toggle-visibility").forEach(btn => {
    btn.addEventListener("click", function() {
        const targetId = this.dataset.target;
        const input = document.getElementById(targetId);
        const icon = this.querySelector("i");
        
        if (input.type === "password") {
            input.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        } else {
            input.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
    });
});

// ===== CONNECT AI PROVIDERS =====
const connectBtn = document.getElementById("connectAIBtn");
const hfInput = document.getElementById("hfApi");
const groqInput = document.getElementById("groqApi");
const togetherInput = document.getElementById("togetherApi");

connectBtn.addEventListener("click", async function() {
    const icon = this.querySelector("i");
    const text = this.querySelector("span");
    
    // Check if at least one API key is provided
    const hfKey = hfInput.value.trim();
    const groqKey = groqInput.value.trim();
    const togetherKey = togetherInput.value.trim();
    
    if (!hfKey && !groqKey && !togetherKey) {
        showToast("⚠️ Please enter at least one AI provider API key", "error");
        return;
    }
    
    // Disable button
    this.disabled = true;
    icon.className = "fas fa-spinner fa-spin";
    text.textContent = "Connecting to AI Providers...";
    
    // Simulate connection to each provider
    const connections = [];
    
    if (hfKey) connections.push(connectProvider("hf", hfKey));
    if (groqKey) connections.push(connectProvider("groq", groqKey));
    if (togetherKey) connections.push(connectProvider("together", togetherKey));
    
    await Promise.all(connections);
    
    // Reset button
    icon.className = "fas fa-plug";
    text.textContent = "Connect AI Providers";
    this.disabled = false;
    
    showToast("✅ AI Providers connected successfully", "success");
});

function connectProvider(provider, key) {
    return new Promise(resolve => {
        setTimeout(() => {
            const statusDot = document.getElementById(`${provider}Status`);
            const statusText = document.getElementById(`${provider}StatusText`);
            
            if (statusDot && statusText) {
                statusDot.className = "status-badge online";
                statusText.textContent = "Connected";
                
                // Save to localStorage (in real app, encrypt this)
                localStorage.setItem(`${provider}_api_key`, key);
            }
            resolve();
        }, 1000);
    });
}

// Load saved API keys
function loadSavedKeys() {
    const providers = ['hf', 'groq', 'together'];
    providers.forEach(provider => {
        const savedKey = localStorage.getItem(`${provider}_api_key`);
        if (savedKey) {
            const input = document.getElementById(`${provider}Api`);
            if (input) {
                input.value = savedKey;
                // Auto-connect on load
                setTimeout(() => {
                    const statusDot = document.getElementById(`${provider}Status`);
                    const statusText = document.getElementById(`${provider}StatusText`);
                    if (statusDot && statusText) {
                        statusDot.className = "status-badge online";
                        statusText.textContent = "Connected";
                    }
                }, 500);
            }
        }
    });
}
loadSavedKeys();

// ===== PAGE SWITCHING =====
function showPage(page) {
    // Update active nav link
    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.remove("active");
    });
    event.target.closest(".nav-link").classList.add("active");
    
    // Neural transition effect
    contentArea.style.opacity = "0";
    contentArea.style.transform = "translateY(10px)";
    
    setTimeout(() => {
        switch(page) {
            case "dashboard":
                contentArea.innerHTML = getDashboardHTML();
                initializeDashboardFeatures();
                break;
                
            case "history":
                contentArea.innerHTML = getHistoryHTML();
                break;
                
            case "settings":
                contentArea.innerHTML = getSettingsHTML();
                break;
        }
        
        // Fade in new content
        contentArea.style.opacity = "1";
        contentArea.style.transform = "translateY(0)";
        contentArea.style.transition = "all 0.5s";
    }, 300);
}

// ===== DASHBOARD HTML =====
function getDashboardHTML() {
    return `
        <div class="dashboard-header">
            <h1><i class="fas fa-newspaper"></i> News Automation</h1>
            <p class="neural-text">Fetch news, generate content, and post to Facebook</p>
        </div>
        
        <!-- FACEBOOK CONFIGURATION SECTION -->
        <div class="facebook-section glass-card">
            <h2><i class="fab fa-facebook"></i> Facebook Integration</h2>
            
            <div class="input-group floating-label">
                <input type="text" id="fbApiKey" required placeholder=" " value="${localStorage.getItem('fb_api_key') || ''}">
                <label for="fbApiKey">Facebook API Key</label>
                <i class="fab fa-facebook input-icon"></i>
            </div>
            
            <div class="input-group floating-label">
                <input type="text" id="fbPageId" required placeholder=" " value="${localStorage.getItem('fb_page_id') || ''}">
                <label for="fbPageId">Facebook Page ID</label>
                <i class="fas fa-id-card input-icon"></i>
            </div>
            
            <button class="save-fb-btn" id="saveFbConfig">
                <i class="fas fa-save"></i>
                <span>Save Facebook Configuration</span>
            </button>
        </div>
        
        <!-- NEWS FETCH AND POST SECTION -->
        <div class="automation-section glass-card">
            <h2><i class="fas fa-robot"></i> Automation Controls</h2>
            
            <div class="news-controls">
                <div class="input-group floating-label">
                    <input type="text" id="newsTopic" placeholder=" ">
                    <label for="newsTopic">News Topic (e.g., technology, sports)</label>
                    <i class="fas fa-tag input-icon"></i>
                </div>
                
                <div class="input-group floating-label">
                    <select id="postFrequency">
                        <option value="now">Now</option>
                        <option value="hourly">Every Hour</option>
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                    </select>
                    <label for="postFrequency">Posting Frequency</label>
                    <i class="fas fa-clock input-icon"></i>
                </div>
            </div>
            
            <div class="action-buttons">
                <button class="action-btn fetch-btn" id="fetchNewsBtn">
                    <i class="fas fa-search"></i>
                    <span>Fetch News</span>
                </button>
                
                <button class="action-btn generate-btn" id="generatePostBtn">
                    <i class="fas fa-magic"></i>
                    <span>Generate Post</span>
                </button>
                
                <button class="action-btn post-btn" id="postToFacebookBtn">
                    <i class="fab fa-facebook"></i>
                    <span>Post to Facebook</span>
                </button>
                
                <button class="action-btn auto-btn" id="startAutomationBtn">
                    <i class="fas fa-play"></i>
                    <span>Start Automation</span>
                </button>
            </div>
        </div>
        
        <!-- PREVIEW SECTION -->
        <div class="preview-section glass-card" id="previewSection" style="display: none;">
            <h3><i class="fas fa-eye"></i> Generated Post Preview</h3>
            <div id="postPreview"></div>
            <div id="imagePreview"></div>
        </div>
        
        <!-- NEWS RESULTS -->
        <div class="news-results glass-card" id="newsResults" style="display: none;">
            <h3><i class="fas fa-newspaper"></i> Latest News</h3>
            <div id="newsList"></div>
        </div>
    `;
}

// ===== HISTORY HTML =====
function getHistoryHTML() {
    const history = JSON.parse(localStorage.getItem('post_history') || '[]');
    
    return `
        <h1><i class="fas fa-history"></i> Post History</h1>
        <p class="neural-text">Your automated posts</p>
        
        <div class="history-list">
            ${history.length > 0 ? 
                history.map(post => `
                    <div class="history-item glass-card">
                        <div class="history-header">
                            <span class="post-date">${post.date}</span>
                            <span class="post-status ${post.status}">${post.status}</span>
                        </div>
                        <p class="post-preview">${post.content.substring(0, 100)}...</p>
                        <div class="post-meta">
                            <span><i class="fab fa-facebook"></i> ${post.platform}</span>
                            <span><i class="fas fa-chart-line"></i> ${post.engagement || '0'} engagements</span>
                        </div>
                    </div>
                `).join('') :
                '<p class="no-history">No posts yet. Start automating!</p>'
            }
        </div>
    `;
}

// ===== SETTINGS HTML =====
function getSettingsHTML() {
    return `
        <h1><i class="fas fa-cog"></i> Settings</h1>
        <p class="neural-text">Configure your automation</p>
        
        <div class="settings-section glass-card">
            <h3>Content Settings</h3>
            
            <label class="toggle-setting">
                <span>Include images in posts</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="includeImages" checked>
                    <span class="toggle-slider"></span>
                </label>
            </label>
            
            <label class="toggle-setting">
                <span>Auto-schedule posts</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="autoSchedule">
                    <span class="toggle-slider"></span>
                </label>
            </label>
            
            <div class="input-group floating-label">
                <input type="number" id="maxPosts" value="5" min="1" max="20">
                <label for="maxPosts">Maximum posts per day</label>
            </div>
            
            <button class="save-settings-btn" id="saveSettings">
                <i class="fas fa-save"></i>
                <span>Save Settings</span>
            </button>
        </div>
    `;
}

// ===== DASHBOARD FEATURES INITIALIZATION =====
function initializeDashboardFeatures() {
    // Save Facebook config
    const saveFbBtn = document.getElementById("saveFbConfig");
    if (saveFbBtn) {
        saveFbBtn.addEventListener("click", function() {
            const fbApi = document.getElementById("fbApiKey").value.trim();
            const fbPage = document.getElementById("fbPageId").value.trim();
            
            if (!fbApi || !fbPage) {
                showToast("⚠️ Please enter both Facebook API Key and Page ID", "error");
                return;
            }
            
            localStorage.setItem("fb_api_key", fbApi);
            localStorage.setItem("fb_page_id", fbPage);
            
            showToast("✅ Facebook configuration saved", "success");
        });
    }
    
    // Fetch news
    const fetchBtn = document.getElementById("fetchNewsBtn");
    if (fetchBtn) {
        fetchBtn.addEventListener("click", simulateFetchNews);
    }
    
    // Generate post
    const generateBtn = document.getElementById("generatePostBtn");
    if (generateBtn) {
        generateBtn.addEventListener("click", simulateGeneratePost);
    }
    
    // Post to Facebook
    const postBtn = document.getElementById("postToFacebookBtn");
    if (postBtn) {
        postBtn.addEventListener("click", simulatePostToFacebook);
    }
    
    // Start automation
    const autoBtn = document.getElementById("startAutomationBtn");
    if (autoBtn) {
        autoBtn.addEventListener("click", function() {
            const topic = document.getElementById("newsTopic")?.value;
            if (!topic) {
                showToast("⚠️ Please enter a news topic first", "error");
                return;
            }
            
            showToast("🔄 Automation started for topic: " + topic, "success");
            this.innerHTML = '<i class="fas fa-pause"></i><span>Stop Automation</span>';
        });
    }
}

// ===== SIMULATION FUNCTIONS =====
function simulateFetchNews() {
    const topic = document.getElementById("newsTopic")?.value;
    if (!topic) {
        showToast("⚠️ Please enter a news topic", "error");
        return;
    }
    
    showToast(`🔍 Fetching latest ${topic} news...`, "info");
    
    setTimeout(() => {
        const newsResults = document.getElementById("newsResults");
        const newsList = document.getElementById("newsList");
        
        if (newsResults && newsList) {
            newsResults.style.display = "block";
            
            // Simulated news results
            newsList.innerHTML = `
                <div class="news-item">
                    <h4>Breaking: Major development in ${topic}</h4>
                    <p>Scientists announce breakthrough in ${topic} research...</p>
                    <small>Source: Tech News • 2 hours ago</small>
                </div>
                <div class="news-item">
                    <h4>${topic} industry shows record growth</h4>
                    <p>New report shows 40% increase in ${topic} adoption...</p>
                    <small>Source: Business Daily • 5 hours ago</small>
                </div>
                <div class="news-item">
                    <h4>Future of ${topic}: What experts predict</h4>
                    <p>Leading voices share insights on ${topic} trends...</p>
                    <small>Source: Industry Watch • 1 day ago</small>
                </div>
            `;
        }
        
        showToast("✅ News fetched successfully", "success");
    }, 2000);
}

function simulateGeneratePost() {
    const topic = document.getElementById("newsTopic")?.value;
    if (!topic) {
        showToast("⚠️ Please enter a news topic", "error");
        return;
    }
    
    // Check if AI providers are connected
    const hfConnected = document.getElementById("hfStatusText")?.textContent === "Connected";
    const groqConnected = document.getElementById("groqStatusText")?.textContent === "Connected";
    
    if (!hfConnected && !groqConnected) {
        showToast("⚠️ Please connect at least one AI provider first", "error");
        return;
    }
    
    showToast("🤖 Generating post content...", "info");
    
    setTimeout(() => {
        const previewSection = document.getElementById("previewSection");
        const postPreview = document.getElementById("postPreview");
        
        if (previewSection && postPreview) {
            previewSection.style.display = "block";
            
            // Simulated AI-generated content
            postPreview.innerHTML = `
                <div class="generated-content">
                    <h3>${topic.toUpperCase()} Update: Breaking News</h3>
                    <p>🚀 Exciting developments in the world of ${topic}! Industry leaders are revolutionizing how we approach innovation and growth.</p>
                    <p>💡 Key highlights from today's announcements show a 45% increase in efficiency and groundbreaking new applications that will change everything.</p>
                    <p>🔮 What does this mean for you? Stay tuned for more updates as we continue to monitor this rapidly evolving story.</p>
                    <div class="post-footer">
                        <span>#${topic} #Innovation #TechNews</span>
                    </div>
                </div>
            `;
            
            // Simulate image generation
            const imagePreview = document.getElementById("imagePreview");
            if (imagePreview) {
                imagePreview.innerHTML = `
                    <div class="image-placeholder">
                        <i class="fas fa-image"></i>
                        <span>AI Generated Image for ${topic}</span>
                    </div>
                `;
            }
        }
        
        showToast("✅ Post generated successfully", "success");
    }, 3000);
}

function simulatePostToFacebook() {
    const fbApi = localStorage.getItem("fb_api_key");
    const fbPage = localStorage.getItem("fb_page_id");
    
    if (!fbApi || !fbPage) {
        showToast("⚠️ Please configure Facebook API and Page ID first", "error");
        return;
    }
    
    const previewSection = document.getElementById("previewSection");
    if (!previewSection || previewSection.style.display === "none") {
        showToast("⚠️ Please generate a post first", "error");
        return;
    }
    
    showToast("📤 Posting to Facebook...", "info");
    
    setTimeout(() => {
        // Save to history
        const history = JSON.parse(localStorage.getItem('post_history') || '[]');
        history.unshift({
            date: new Date().toLocaleString(),
            content: "Generated post about " + document.getElementById("newsTopic")?.value,
            status: "published",
            platform: "Facebook",
            engagement: Math.floor(Math.random() * 100)
        });
        localStorage.setItem('post_history', JSON.stringify(history.slice(0, 20)));
        
        showToast("✅ Post published successfully to Facebook!", "success");
    }, 2000);
}

// ===== LOGOUT =====
logoutBtn.addEventListener("click", async function(e) {
    e.preventDefault();
    
    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Disconnecting...';
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    localStorage.removeItem("sentino_session");
    localStorage.removeItem("user_email");
    
    showToast("👋 Session terminated", "info");
    
    document.body.style.opacity = "0";
    document.body.style.transition = "opacity 0.5s";
    
    setTimeout(() => {
        window.location.href = "index.html";
    }, 500);
});

// ===== TOAST NOTIFICATION =====
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
    
    setTimeout(() => {
        toast.style.animation = "slideOut 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Initialize dashboard
showPage("dashboard");