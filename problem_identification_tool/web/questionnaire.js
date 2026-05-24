// Problem Identification Questionnaire JavaScript
class QuestionnaireEngine {
    constructor() {
        this.currentQuestion = 0;
        this.responses = {};
        this.questions = [];
        this.totalQuestions = 0;
        this.startTime = Date.now();
        this.isTransitioning = false;
        this.init();
    }

    async init() {
        try {
            await this.loadQuestionnaire();
            this.renderQuestion();
            this.setupEventListeners();
            this.updateProgress();
        } catch (error) {
            console.error('Error initializing questionnaire:', error);
            this.showError('Failed to load questionnaire. Please refresh the page.');
        }
    }

    async loadQuestionnaire() {
        try {
            // Try web/data first (for GitHub Pages), then fallback to ../data (for local dev)
            let response = await fetch('./data/questionnaires.json').catch(() => null);
            if (!response || !response.ok) {
                response = await fetch('../data/questionnaires.json');
            }
            const data = await response.json();
            const activeQuestionnaire = data.questionnaires.find(q => q.id === data.active_questionnaire);
            
            if (!activeQuestionnaire) {
                throw new Error('No active questionnaire found');
            }
            
            this.questions = activeQuestionnaire.questions;
            this.totalQuestions = this.questions.length;
            this.settings = activeQuestionnaire.settings;
        } catch (error) {
            console.error('Error loading questionnaire:', error);
            // Fallback to hardcoded questions if JSON fails
            this.questions = this.getFallbackQuestions();
            this.totalQuestions = this.questions.length;
            this.settings = { anonymous: true, allow_skipping: true };
        }
    }

    getFallbackQuestions() {
        return [
            {
                id: "q1",
                type: "multiple_choice",
                question: "What area of your life would you like to improve most?",
                options: [
                    "Work/Career",
                    "Health & Fitness", 
                    "Personal Relationships",
                    "Financial Situation",
                    "Learning & Education",
                    "Technology & Digital Life",
                    "Home & Environment",
                    "Personal Development",
                    "Business/Entrepreneurship",
                    "Other"
                ],
                required: true
            },
            {
                id: "q2",
                type: "rating",
                question: "On a scale of 1-10, how satisfied are you with this area?",
                min: 1,
                max: 10,
                required: true
            },
            {
                id: "q3",
                type: "open_text",
                question: "What specific challenges do you face in this area?",
                placeholder: "Please describe your main challenges...",
                required: true
            },
            {
                id: "q4",
                type: "multiple_choice",
                question: "How often do these challenges affect your daily life?",
                options: [
                    "Constantly",
                    "Daily", 
                    "Weekly",
                    "Monthly",
                    "Rarely"
                ],
                required: true
            }
        ];
    }

    renderQuestion() {
        this.renderQuestionInner();
    }

    renderQuestionInner() {
        const form = document.getElementById('questionnaireForm');
        const question = this.questions[this.currentQuestion];

        if (!question) {
            this.showCompletion();
            return;
        }

        form.innerHTML = `
            <div class="question active">
                <h3>${this.escapeHtml(question.question)}</h3>
                <div class="options">
                    ${this.renderQuestionInput(question)}
                </div>
                ${question.required ? '' : '<p class="skip-notice">This question is optional — you can skip with Next</p>'}
            </div>
        `;

        this.updateProgress();
        this.updateButtons();
        this.restoreOtherInputState(question);
        notifyHeightIfEmbedded();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async transitionToQuestion(updateIndexFn) {
        if (this.isTransitioning) return;
        this.isTransitioning = true;

        const form = document.getElementById('questionnaireForm');
        const current = form.querySelector('.question');
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (current && !reduceMotion) {
            current.classList.remove('active');
            current.classList.add('exiting');
            await new Promise((resolve) => setTimeout(resolve, 200));
        }

        updateIndexFn();
        this.clearValidationError();
        this.renderQuestionInner();
        this.isTransitioning = false;
    }

    restoreOtherInputState(question) {
        if (question.type === 'multiple_choice' && this.responses[question.id]) {
            const responseValue = this.responses[question.id];
            // Check if response starts with "Other:"
            if (responseValue.startsWith('Other:')) {
                const otherText = responseValue.replace('Other:', '').trim();
                const otherRadio = document.querySelector(`input[name="${question.id}"][data-is-other="true"]`);
                const otherInputContainer = document.getElementById(`${question.id}_other_input`);
                const otherTextInput = document.getElementById(`${question.id}_other_text`);
                
                if (otherRadio && otherInputContainer && otherTextInput) {
                    // Select the "Other" radio button
                    otherRadio.checked = true;
                    otherRadio.closest('.option').classList.add('selected');
                    // Show and populate the text input
                    otherInputContainer.style.display = 'block';
                    otherTextInput.value = otherText;
                }
            } else {
                // Restore regular option selection
                const selectedRadio = document.querySelector(`input[name="${question.id}"][value="${responseValue}"]`);
                if (selectedRadio) {
                    selectedRadio.checked = true;
                    selectedRadio.closest('.option').classList.add('selected');
                }
            }
        }
    }

    renderQuestionInput(question) {
        switch (question.type) {
            case 'multiple_choice':
                const hasOther = question.options.some(opt => opt.toLowerCase() === 'other');
                const optionsHtml = question.options.map(option => `
                    <label class="option">
                        <input type="radio" name="${question.id}" value="${option}" data-is-other="${option.toLowerCase() === 'other'}">
                        ${option}
                    </label>
                `).join('');
                
                // Add text input for "Other" option (initially hidden)
                const otherInputHtml = hasOther ? `
                    <div class="other-input-container" id="${question.id}_other_input" style="display: none; margin-top: 15px;">
                        <label for="${question.id}_other_text" style="display: block; margin-bottom: 8px; font-weight: 500;">
                            Please specify:
                        </label>
                        <input 
                            type="text" 
                            id="${question.id}_other_text" 
                            name="${question.id}_other" 
                            class="other-text-input"
                            placeholder="Enter your answer..."
                        >
                    </div>
                ` : '';
                
                return optionsHtml + otherInputHtml;

            case 'rating':
                let ratingHtml = '<div class="rating-scale">';
                for (let i = question.min; i <= question.max; i++) {
                    ratingHtml += `
                        <div class="rating-option" data-value="${i}">
                            <div class="rating-number">${i}</div>
                            <div class="rating-label">${i === question.min ? 'Very Low' : i === question.max ? 'Very High' : ''}</div>
                        </div>
                    `;
                }
                ratingHtml += '</div>';
                return ratingHtml;

            case 'open_text':
                return `
                    <textarea 
                        class="text-input" 
                        name="${question.id}" 
                        placeholder="${question.placeholder || 'Please enter your response...'}"
                        rows="4"
                    ></textarea>
                `;

            default:
                return '<p>Unsupported question type</p>';
        }
    }

    setupEventListeners() {
        // Next button
        document.getElementById('nextBtn').addEventListener('click', () => {
            if (this.validateCurrentQuestion()) {
                this.saveCurrentResponse();
                this.nextQuestion();
            }
        });

        // Previous button
        document.getElementById('prevBtn').addEventListener('click', () => {
            this.previousQuestion();
        });

        // Option selection for multiple choice
        document.addEventListener('change', (e) => {
            if (e.target.type === 'radio') {
                this.updateOptionSelection(e.target);
                // Show/hide "Other" text input
                this.handleOtherOption(e.target);
            }
        });

        // Rating selection
        document.addEventListener('click', (e) => {
            if (e.target.closest('.rating-option')) {
                this.selectRating(e.target.closest('.rating-option'));
                this.clearValidationError();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key !== 'Enter' || e.shiftKey || this.isTransitioning) return;
            const tag = document.activeElement?.tagName;
            if (tag === 'TEXTAREA') return;
            const nextBtn = document.getElementById('nextBtn');
            if (nextBtn && !nextBtn.disabled && nextBtn.offsetParent !== null) {
                e.preventDefault();
                nextBtn.click();
            }
        });

        document.getElementById('questionnaireForm').addEventListener('input', () => {
            this.clearValidationError();
        });
    }

    showValidationError(message) {
        const banner = document.getElementById('validationBanner');
        if (!banner) return;
        banner.textContent = message;
        banner.hidden = false;
        banner.classList.add('visible');
    }

    clearValidationError() {
        const banner = document.getElementById('validationBanner');
        if (!banner) return;
        banner.textContent = '';
        banner.hidden = true;
        banner.classList.remove('visible');
    }

    renderStepDots() {
        const container = document.getElementById('stepDots');
        if (!container || this.totalQuestions < 1) return;

        if (container.dataset.built !== '1') {
            container.innerHTML = '';
            for (let i = 0; i < this.totalQuestions; i++) {
                const dot = document.createElement('span');
                dot.className = 'step-dot';
                dot.title = `Question ${i + 1}`;
                container.appendChild(dot);
            }
            container.dataset.built = '1';
        }

        container.querySelectorAll('.step-dot').forEach((dot, index) => {
            dot.classList.remove('completed', 'current');
            if (index < this.currentQuestion) dot.classList.add('completed');
            if (index === this.currentQuestion) dot.classList.add('current');
        });
    }

    updateOptionSelection(selectedInput) {
        const questionId = selectedInput.name;
        const options = document.querySelectorAll(`input[name="${questionId}"]`);
        options.forEach(option => {
            option.closest('.option').classList.remove('selected');
        });
        selectedInput.closest('.option').classList.add('selected');
    }

    handleOtherOption(selectedInput) {
        const questionId = selectedInput.name;
        const isOther = selectedInput.dataset.isOther === 'true';
        const otherInputContainer = document.getElementById(`${questionId}_other_input`);
        const otherTextInput = document.getElementById(`${questionId}_other_text`);
        
        if (otherInputContainer) {
            if (isOther) {
                // Show the text input when "Other" is selected
                otherInputContainer.style.display = 'block';
                if (otherTextInput) {
                    otherTextInput.focus();
                }
            } else {
                // Hide the text input and clear it when another option is selected
                otherInputContainer.style.display = 'none';
                if (otherTextInput) {
                    otherTextInput.value = '';
                }
            }
        }
    }

    selectRating(ratingElement) {
        const questionId = this.questions[this.currentQuestion].id;
        const value = ratingElement.dataset.value;
        
        // Remove previous selection
        document.querySelectorAll('.rating-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selection to clicked option
        ratingElement.classList.add('selected');
        
        // Store the value
        this.responses[questionId] = value;
    }

    validateCurrentQuestion() {
        const question = this.questions[this.currentQuestion];
        if (!question.required) return true;

        const questionId = question.id;
        
        if (question.type === 'multiple_choice') {
            const selected = document.querySelector(`input[name="${questionId}"]:checked`);
            if (!selected) {
                this.showValidationError('Please select an option before continuing.');
                return false;
            }
            if (selected.dataset.isOther === 'true') {
                const otherTextInput = document.getElementById(`${questionId}_other_text`);
                if (!otherTextInput || !otherTextInput.value.trim()) {
                    this.showValidationError('Please describe what you mean by "Other".');
                    otherTextInput?.focus();
                    return false;
                }
            }
        } else if (question.type === 'rating') {
            if (!this.responses[questionId]) {
                this.showValidationError('Please select a rating on the scale before continuing.');
                return false;
            }
        } else if (question.type === 'open_text') {
            const textarea = document.querySelector(`textarea[name="${questionId}"]`);
            if (!textarea?.value.trim()) {
                this.showValidationError('Please enter a short answer before continuing.');
                textarea?.focus();
                return false;
            }
        }

        this.clearValidationError();
        return true;
    }

    saveCurrentResponse() {
        const question = this.questions[this.currentQuestion];
        const questionId = question.id;
        
        if (question.type === 'multiple_choice') {
            const selected = document.querySelector(`input[name="${questionId}"]:checked`);
            if (selected) {
                // If "Other" is selected, save both the "Other" option and the user's text
                if (selected.dataset.isOther === 'true') {
                    const otherTextInput = document.getElementById(`${questionId}_other_text`);
                    const otherText = otherTextInput ? otherTextInput.value.trim() : '';
                    // Save as "Other: [user's text]"
                    this.responses[questionId] = otherText ? `Other: ${otherText}` : 'Other';
                } else {
                    this.responses[questionId] = selected.value;
                }
            }
        } else if (question.type === 'open_text') {
            const textarea = document.querySelector(`textarea[name="${questionId}"]`);
            if (textarea) {
                this.responses[questionId] = textarea.value.trim();
            }
        }
        // Rating responses are already saved in selectRating method
    }

    nextQuestion() {
        if (this.currentQuestion < this.totalQuestions - 1) {
            this.transitionToQuestion(() => {
                this.currentQuestion++;
            });
        } else {
            this.completeQuestionnaire();
        }
    }

    previousQuestion() {
        if (this.currentQuestion > 0) {
            this.transitionToQuestion(() => {
                this.currentQuestion--;
            });
        }
    }

    updateProgress() {
        const total = Math.max(this.totalQuestions, 1);
        const current = this.currentQuestion + 1;
        const percent = Math.round((current / total) * 100);

        document.getElementById('progressFill').style.width = `${percent}%`;

        const stepLabel = document.getElementById('progressStepLabel');
        const percentLabel = document.getElementById('progressPercentLabel');
        if (stepLabel) stepLabel.textContent = `Question ${current} of ${total}`;
        if (percentLabel) percentLabel.textContent = `${percent}%`;

        const bar = document.getElementById('progressBar');
        if (bar) {
            bar.setAttribute('aria-valuenow', String(current));
            bar.setAttribute('aria-valuemax', String(total));
        }

        this.renderStepDots();
    }

    updateButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const navHint = document.getElementById('navHint');

        prevBtn.style.display = this.currentQuestion === 0 ? 'none' : 'block';

        const isLast = this.currentQuestion === this.totalQuestions - 1;
        nextBtn.textContent = isLast ? 'Complete Survey' : 'Next';
        if (navHint) {
            navHint.textContent = isLast ? 'Press Enter to submit' : 'Press Enter to continue';
        }
    }

    async completeQuestionnaire() {
        try {
            await this.saveResponses();
            this.showCompletion();
        } catch (error) {
            console.error('Error saving responses:', error);
            this.showError('There was an error saving your responses. Please try again.');
        }
    }

    async saveResponses() {
        const responseData = {
            id: this.generateResponseId(),
            timestamp: new Date().toISOString(),
            responses: this.responses,
            completion_time: Date.now() - this.startTime,
            user_agent: navigator.userAgent,
            anonymous: this.settings.anonymous
        };

        // PRIMARY STORAGE: Save to browser localStorage
        // This is the main storage method - works offline and is privacy-first
        // Data is stored in the user's browser and never leaves their device
        const existingResponses = JSON.parse(localStorage.getItem('questionnaire_responses') || '[]');
        existingResponses.push(responseData);
        localStorage.setItem('questionnaire_responses', JSON.stringify(existingResponses));

        // OPTIONAL: Try to send to server (Netlify Function) for centralized storage
        // This will fail on GitHub Pages (which is fine - localStorage is primary)
        // If you need centralized storage, see DATA_STORAGE_GUIDE.md for alternatives
        try {
            const response = await fetch('/.netlify/functions/submit-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(responseData)
            });
            
            if (response.ok) {
                console.log('Response saved to server successfully');
            } else {
                console.log('Server save failed, using localStorage fallback');
            }
        } catch (error) {
            console.log('Server not available, using localStorage fallback');
        }
    }

    generateResponseId() {
        return 'resp_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    showCompletion() {
        const form = document.getElementById('questionnaireForm');
        const buttonGroup = document.querySelector('.button-group');

        this.clearValidationError();
        form.innerHTML = `
            <div class="completion-message">
                <h2>Thank you!</h2>
                <p>Your responses have been recorded and will help us understand common challenges better.</p>
                <p>We appreciate you taking the time to share your insights.</p>
            </div>
        `;

        buttonGroup.style.display = 'none';

        document.getElementById('progressFill').style.width = '100%';
        const stepLabel = document.getElementById('progressStepLabel');
        const percentLabel = document.getElementById('progressPercentLabel');
        if (stepLabel) stepLabel.textContent = 'Complete';
        if (percentLabel) percentLabel.textContent = '100%';
        notifyHeightIfEmbedded();
        
        // NOTE: "View Analytics Dashboard" link is intentionally NOT shown here
        // The dashboard is admin-only and should be accessed directly at:
        // https://mizza411.github.io/Inc/problem_identification_tool/web/dashboard.html
        // Regular users should not see analytics - it's for the survey creator only
    }

    showError(message) {
        const form = document.getElementById('questionnaireForm');
        form.innerHTML = `
            <div class="completion-message">
                <h2 style="color: #dc3545;">❌ Error</h2>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="location.reload()">Try Again</button>
            </div>
        `;
    }
}

function notifyHeightIfEmbedded() {
    if (typeof notifyHeight === 'function') notifyHeight();
}

// Initialize the questionnaire when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new QuestionnaireEngine();
});
