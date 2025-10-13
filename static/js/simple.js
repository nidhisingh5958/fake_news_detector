// Simple, robust JavaScript for fake news detector
let isAnalyzing = false;

document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const textInput = document.getElementById('text-input');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    
    // Analyze button click handler
    analyzeBtn.addEventListener('click', analyzeContent);
    
    // Text input handler
    textInput.addEventListener('input', updateButton);
    
    function updateButton() {
        const hasText = textInput.value.trim().length > 0;
        analyzeBtn.disabled = !hasText || isAnalyzing;
    }
    
    async function analyzeContent() {
        const text = textInput.value.trim();
        
        if (!text || isAnalyzing) return;
        
        isAnalyzing = true;
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        loading.classList.remove('hidden');
        results.classList.add('hidden');
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayResults(data);
            } else {
                alert('Error: ' + (data.error || 'Analysis failed'));
            }
        } catch (error) {
            alert('Network error: ' + error.message);
        } finally {
            isAnalyzing = false;
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-brain"></i> Analyze with AI';
            loading.classList.add('hidden');
        }
    }
    
    function displayResults(data) {
        // Update verdict
        document.getElementById('verdict-level').textContent = data.verdict_level;
        document.getElementById('verdict-message').textContent = data.verdict_message;
        
        // Update scores
        document.getElementById('risk-score').textContent = data.risk_score + '%';
        document.getElementById('credibility-score').textContent = data.credibility_score + '%';
        document.getElementById('risk-bar').style.width = data.risk_score + '%';
        document.getElementById('credibility-bar').style.width = data.credibility_score + '%';
        
        // Update AI prediction
        document.getElementById('ai-result').textContent = data.ai_prediction.prediction;
        document.getElementById('ai-confidence').textContent = data.ai_prediction.confidence + '%';
        
        // Update indicators
        const indicatorsList = document.getElementById('indicators-list');
        indicatorsList.innerHTML = '';
        
        Object.entries(data.risk_indicators).forEach(([name, indicator]) => {
            const div = document.createElement('div');
            div.className = 'indicator-item';
            div.innerHTML = `
                <div class="indicator-header">
                    <span class="indicator-title">${name}</span>
                    <span class="indicator-score">${indicator.score}/100</span>
                </div>
                <div class="indicator-message">${indicator.message}</div>
            `;
            indicatorsList.appendChild(div);
        });
        
        // Update stats
        const features = data.linguistic_features;
        const statsGrid = document.getElementById('stats-grid');
        statsGrid.innerHTML = `
            <div class="stat-item">
                <span class="stat-value">${features.word_count}</span>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">${features.sentence_count}</span>
                <div class="stat-label">Sentences</div>
            </div>
            <div class="stat-item">
                <span class="stat-value">${features.exclamation_count}</span>
                <div class="stat-label">Exclamations</div>
            </div>
        `;
        
        results.classList.remove('hidden');
        results.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Initial button state
    updateButton();
});