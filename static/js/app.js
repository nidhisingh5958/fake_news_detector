class FakeNewsDetectorApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.updateCharCounter();
    }

    initializeElements() {
        this.urlInput = document.getElementById('url-input');
        this.textInput = document.getElementById('text-input');
        this.analyzeBtn = document.getElementById('analyze-btn');
        this.loading = document.getElementById('loading');
        this.results = document.getElementById('results');
        this.charCount = document.getElementById('char-count');
    }

    bindEvents() {
        this.analyzeBtn.addEventListener('click', () => this.analyzeContent());
        this.textInput.addEventListener('input', () => this.updateCharCounter());
        this.textInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.analyzeContent();
            }
        });
    }

    updateCharCounter() {
        const count = this.textInput.value.length;
        this.charCount.textContent = count.toLocaleString();
        
        // Update button state
        this.analyzeBtn.disabled = count === 0;
    }

    async analyzeContent() {
        const text = this.textInput.value.trim();
        const url = this.urlInput.value.trim();

        if (!text) {
            this.showError('Please enter some text to analyze.');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed');
            }

            this.displayResults(data);
        } catch (error) {
            this.showError(`Analysis failed: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        this.loading.classList.remove('hidden');
        this.results.classList.add('hidden');
        this.analyzeBtn.disabled = true;
    }

    hideLoading() {
        this.loading.classList.add('hidden');
        this.analyzeBtn.disabled = false;
    }

    showError(message) {
        alert(message); // Simple error handling - could be enhanced with a toast system
    }

    displayResults(data) {
        // Update verdict
        this.updateVerdict(data);
        
        // Update scores
        this.updateScores(data);
        
        // Update AI prediction
        this.updateAIPrediction(data);
        
        // Update indicators
        this.updateIndicators(data);
        
        // Update statistics
        this.updateStatistics(data);
        
        // Show results
        this.results.classList.remove('hidden');
        this.results.scrollIntoView({ behavior: 'smooth' });
    }

    updateVerdict(data) {
        const verdictIcon = document.getElementById('verdict-emoji');
        const verdictLevel = document.getElementById('verdict-level');
        const verdictMessage = document.getElementById('verdict-message');

        // Update icon and styling based on risk level
        verdictIcon.className = 'fas ';
        const iconContainer = verdictIcon.parentElement;
        iconContainer.className = 'verdict-icon ';

        if (data.verdict_level === 'HIGH RISK') {
            verdictIcon.classList.add('fa-exclamation-triangle');
            iconContainer.classList.add('high-risk');
        } else if (data.verdict_level === 'MEDIUM RISK') {
            verdictIcon.classList.add('fa-exclamation-circle');
            iconContainer.classList.add('medium-risk');
        } else {
            verdictIcon.classList.add('fa-check-circle');
            iconContainer.classList.add('low-risk');
        }

        verdictLevel.textContent = data.verdict_level;
        verdictMessage.textContent = data.verdict_message;
    }

    updateScores(data) {
        const riskBar = document.getElementById('risk-bar');
        const riskScore = document.getElementById('risk-score');
        const credibilityBar = document.getElementById('credibility-bar');
        const credibilityScore = document.getElementById('credibility-score');

        // Animate score bars
        setTimeout(() => {
            riskBar.style.width = `${data.risk_score}%`;
            credibilityBar.style.width = `${data.credibility_score}%`;
        }, 100);

        riskScore.textContent = `${data.risk_score}%`;
        credibilityScore.textContent = `${data.credibility_score}%`;
    }

    updateAIPrediction(data) {
        const aiSection = document.getElementById('ai-prediction');
        const aiResult = document.getElementById('ai-result');
        const aiConfidence = document.getElementById('ai-confidence');

        if (data.ai_prediction.available) {
            aiSection.classList.remove('hidden');
            aiResult.textContent = data.ai_prediction.prediction;
            aiConfidence.textContent = `${data.ai_prediction.confidence}%`;
            
            // Style based on prediction
            aiResult.className = 'ai-prediction';
            if (data.ai_prediction.prediction === 'Likely Fake') {
                aiResult.style.borderColor = '#dc3545';
                aiResult.style.color = '#dc3545';
            } else {
                aiResult.style.borderColor = '#28a745';
                aiResult.style.color = '#28a745';
            }
        } else {
            aiSection.classList.add('hidden');
        }
    }

    updateIndicators(data) {
        const indicatorsList = document.getElementById('indicators-list');
        indicatorsList.innerHTML = '';

        Object.entries(data.risk_indicators).forEach(([name, indicator]) => {
            const indicatorElement = this.createIndicatorElement(name, indicator);
            indicatorsList.appendChild(indicatorElement);
        });
        
        // Add news relevance info if available
        if (data.news_relevance) {
            this.addNewsRelevanceInfo(data.news_relevance);
        }
    }

    createIndicatorElement(name, indicator) {
        const div = document.createElement('div');
        div.className = 'indicator-item';
        
        // Determine risk level
        let riskLevel = 'low';
        if (indicator.score >= 60) riskLevel = 'high';
        else if (indicator.score >= 30) riskLevel = 'medium';
        
        div.classList.add(riskLevel);

        div.innerHTML = `
            <div class="indicator-header">
                <span class="indicator-title">${name}</span>
                <span class="indicator-score ${riskLevel}">${riskLevel.toUpperCase()} - ${Math.round(indicator.score)}/100</span>
            </div>
            <div class="indicator-message">${indicator.message}</div>
        `;

        return div;
    }

    updateStatistics(data) {
        const statsGrid = document.getElementById('stats-grid');
        const features = data.linguistic_features;

        const stats = [
            { label: 'Word Count', value: features.word_count.toLocaleString() },
            { label: 'Sentences', value: features.sentence_count },
            { label: 'Avg Words/Sentence', value: features.avg_sentence_length.toFixed(1) },
            { label: 'Capital Letters', value: `${(features.caps_ratio * 100).toFixed(1)}%` },
            { label: 'Exclamations', value: features.exclamation_count },
            { label: 'Questions', value: features.question_count }
        ];

        statsGrid.innerHTML = stats.map(stat => `
            <div class="stat-item">
                <span class="stat-value">${stat.value}</span>
                <div class="stat-label">${stat.label}</div>
            </div>
        `).join('');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FakeNewsDetectorApp();
});