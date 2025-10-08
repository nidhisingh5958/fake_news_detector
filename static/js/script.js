// DOM Elements
const newsForm = document.getElementById('newsForm');
const newsText = document.getElementById('newsText');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.getElementById('btnText');
const spinner = document.getElementById('spinner');
const result = document.getElementById('result');
const error = document.getElementById('error');
const exampleBtns = document.querySelectorAll('.example-btn');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for navigation links
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

    // Add navbar background on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        }
    });

    // Animate stats on scroll
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStats();
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const statsSection = document.getElementById('stats');
    if (statsSection) {
        observer.observe(statsSection);
    }
});

// Example buttons functionality
exampleBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        const exampleText = this.getAttribute('data-text');
        newsText.value = exampleText;
        newsText.focus();
        
        // Add visual feedback
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });
});

// Form submission
newsForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const text = newsText.value.trim();
    
    if (!text) {
        showError('Please enter some text to analyze.');
        return;
    }
    
    if (text.length < 10) {
        showError('Please enter at least 10 characters for accurate analysis.');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideError();
    hideResult();
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Add delay for better UX
            setTimeout(() => {
                showResult(data);
                setLoadingState(false);
            }, 800);
        } else {
            setLoadingState(false);
            showError(data.error || 'An error occurred while analyzing the text.');
        }
    } catch (err) {
        setLoadingState(false);
        showError('Network error. Please check your connection and try again.');
    }
});

function setLoadingState(loading) {
    analyzeBtn.disabled = loading;
    
    if (loading) {
        btnText.innerHTML = '<i class="fas fa-cog fa-spin me-2"></i>Analyzing...';
        spinner.classList.remove('d-none');
        analyzeBtn.style.transform = 'scale(0.98)';
    } else {
        btnText.innerHTML = '<i class="fas fa-brain me-2"></i>Analyze with AI';
        spinner.classList.add('d-none');
        analyzeBtn.style.transform = 'scale(1)';
    }
}

function showResult(data) {
    const prediction = document.getElementById('prediction');
    const confidenceIcon = document.getElementById('confidenceIcon');
    const realProgress = document.getElementById('realProgress');
    const fakeProgress = document.getElementById('fakeProgress');
    const realPercent = document.getElementById('realPercent');
    const fakePercent = document.getElementById('fakePercent');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');
    
    // Set prediction text and styling
    const isReal = data.prediction === 'Real News';
    prediction.textContent = data.prediction;
    prediction.className = isReal ? 'text-success' : 'text-danger';
    
    // Set confidence icon
    const confidence = data.confidence;
    let iconClass, iconColor;
    
    if (confidence >= 90) {
        iconClass = 'fas fa-check-circle';
        iconColor = '#48bb78';
    } else if (confidence >= 70) {
        iconClass = 'fas fa-exclamation-circle';
        iconColor = '#ed8936';
    } else {
        iconClass = 'fas fa-question-circle';
        iconColor = '#f56565';
    }
    
    confidenceIcon.innerHTML = `<i class="${iconClass}" style="color: ${iconColor}"></i>`;
    
    // Animate progress bars
    setTimeout(() => {
        realProgress.style.width = data.real_probability + '%';
        fakeProgress.style.width = data.fake_probability + '%';
        confidenceBar.style.width = confidence + '%';
    }, 100);
    
    // Set percentage text with animation
    animateNumber(realPercent, 0, data.real_probability, 1000);
    animateNumber(fakePercent, 0, data.fake_probability, 1000);
    
    // Set confidence text
    confidenceText.textContent = `${confidence.toFixed(1)}%`;
    
    // Show result with animation
    result.classList.remove('d-none');
    
    // Scroll to result
    setTimeout(() => {
        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 300);
}

function showError(message) {
    const errorText = document.getElementById('errorText');
    errorText.textContent = message;
    error.classList.remove('d-none');
    
    // Auto hide error after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    error.classList.add('d-none');
}

function hideResult() {
    result.classList.add('d-none');
}

// Animate numbers
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = start + (end - start) * easeOutCubic(progress);
        element.textContent = current.toFixed(1) + '%';
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Easing function
function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
}

// Animate stats
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach((stat, index) => {
        setTimeout(() => {
            stat.style.transform = 'scale(1.1)';
            stat.style.transition = 'transform 0.3s ease';
            
            setTimeout(() => {
                stat.style.transform = 'scale(1)';
            }, 300);
        }, index * 200);
    });
}

// Add typing effect for textarea placeholder
let placeholderIndex = 0;
const placeholders = [
    "Enter news article text here...",
    "Paste a news headline or article...",
    "Try: 'Scientists discover new planet'...",
    "Example: 'Breaking news from reliable source'..."
];

function rotatePlaceholder() {
    if (newsText && document.activeElement !== newsText) {
        newsText.placeholder = placeholders[placeholderIndex];
        placeholderIndex = (placeholderIndex + 1) % placeholders.length;
    }
}

// Rotate placeholder every 3 seconds
setInterval(rotatePlaceholder, 3000);

// Add character counter
newsText.addEventListener('input', function() {
    const length = this.value.length;
    const minLength = 10;
    
    // Remove existing counter
    const existingCounter = document.querySelector('.char-counter');
    if (existingCounter) {
        existingCounter.remove();
    }
    
    // Add counter if text is entered
    if (length > 0) {
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.style.cssText = `
            position: absolute;
            bottom: 10px;
            right: 15px;
            font-size: 0.8rem;
            color: ${length >= minLength ? '#48bb78' : '#f56565'};
            background: white;
            padding: 2px 8px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        `;
        counter.textContent = `${length} characters`;
        
        this.parentElement.style.position = 'relative';
        this.parentElement.appendChild(counter);
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (newsText.value.trim()) {
            newsForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to clear
    if (e.key === 'Escape') {
        newsText.value = '';
        hideResult();
        hideError();
        newsText.focus();
    }
});

// Add tooltip for keyboard shortcuts
const shortcutTooltip = document.createElement('div');
shortcutTooltip.innerHTML = `
    <small class="text-muted">
        <i class="fas fa-keyboard me-1"></i>
        Tips: <kbd>Ctrl+Enter</kbd> to analyze, <kbd>Esc</kbd> to clear
    </small>
`;
shortcutTooltip.style.cssText = 'text-align: center; margin-top: 10px;';
newsForm.appendChild(shortcutTooltip);