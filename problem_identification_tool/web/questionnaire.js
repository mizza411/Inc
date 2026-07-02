// Problem Identification Questionnaire JavaScript
class QuestionnaireEngine {
    constructor() {
        this.currentQuestion = 0;
        this.responses = {};
        this.allQuestions = [];
        this.visibleQuestions = [];
        this.totalQuestions = 0;
        this.questionnaireId = null;
        this.refParam = null;
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

    getUrlParam(name) {
        try {
            return new URLSearchParams(window.location.search).get(name);
        } catch (_) {
            return null;
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
            const surveyParam = this.getUrlParam('survey');
            const targetId = surveyParam || data.active_questionnaire;
            const activeQuestionnaire = data.questionnaires.find(q => q.id === targetId);

            if (!activeQuestionnaire) {
                throw new Error(`No questionnaire found for id: ${targetId}`);
            }

            this.allQuestions = activeQuestionnaire.questions;
            this.questionnaireId = activeQuestionnaire.id;
            this.settings = activeQuestionnaire.settings || { anonymous: true, allow_skipping: true };
            this.refParam = this.getUrlParam('ref') || this.getUrlParam('utm_source') || null;
            this.refreshVisibleQuestions();
            this.applyQuestionnaireMeta(activeQuestionnaire);
        } catch (error) {
            console.error('Error loading questionnaire:', error);
            // Fallback to hardcoded questions if JSON fails
            this.allQuestions = this.getFallbackQuestions();
            this.questionnaireId = 'general_problems_v1_fallback';
            this.refreshVisibleQuestions();
            this.settings = { anonymous: true, allow_skipping: true };
        }
    }

    applyQuestionnaireMeta(questionnaire) {
        const h1 = document.querySelector('.header h1');
        const desc = document.querySelector('.header p');
        if (h1 && questionnaire.title) {
            h1.textContent = questionnaire.title;
        }
        if (desc && questionnaire.description) {
            desc.textContent = questionnaire.description;
        }
        if (questionnaire.title) {
            document.title = questionnaire.title;
        }
    }

    isQuestionVisible(question) {
        if (!question.show_if) {
            return true;
        }
        const { question_id, value } = question.show_if;
        const response = this.responses[question_id];
        if (Array.isArray(value)) {
            return value.includes(response);
        }
        return response === value;
    }

    getVisibleQuestions() {
        return this.allQuestions.filter(q => this.isQuestionVisible(q));
    }

    refreshVisibleQuestions() {
        this.visibleQuestions = this.getVisibleQuestions();
        this.totalQuestions = this.visibleQuestions.length;
        if (this.currentQuestion >= this.totalQuestions) {
            this.currentQuestion = Math.max(0, this.totalQuestions - 1);
        }
        const container = document.getElementById('stepDots');
        if (container) {
            delete container.dataset.built;
        }
    }

    getCurrentQuestion() {
        return this.visibleQuestions[this.currentQuestion];
    }

    pruneHiddenResponses() {
        this.allQuestions.forEach(q => {
            if (!this.isQuestionVisible(q) && Object.prototype.hasOwnProperty.call(this.responses, q.id)) {
                delete this.responses[q.id];
            }
        });
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
        const question = this.getCurrentQuestion();

        if (!question) {
            this.showCompletion();
            return;
        }

        form.innerHTML = `
            <div class="question active">
                <h3>${this.escapeHtml(question.question)}</h3>
                ${question.help_text ? `<p class="question-help">${this.escapeHtml(question.help_text)}</p>` : ''}
                <div class="options">
                    ${this.renderQuestionInput(question)}
                </div>
                ${question.required ? '' : '<p class="skip-notice">This question is optional — you can skip with Next</p>'}
            </div>
        `;

        this.updateProgress();
        this.updateButtons();
        this.restoreInputState(question);
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

    restoreInputState(question) {
        if (question.type === 'multiple_choice' && this.responses[question.id]) {
            const responseValue = this.responses[question.id];
            if (responseValue.startsWith('Other:')) {
                const otherText = responseValue.replace('Other:', '').trim();
                const otherRadio = document.querySelector(`input[name="${question.id}"][data-is-other="true"]`);
                const otherInputContainer = document.getElementById(`${question.id}_other_input`);
                const otherTextInput = document.getElementById(`${question.id}_other_text`);

                if (otherRadio && otherInputContainer && otherTextInput) {
                    otherRadio.checked = true;
                    otherRadio.closest('.option').classList.add('selected');
                    otherInputContainer.style.display = 'block';
                    otherTextInput.value = otherText;
                }
            } else {
                const selectedRadio = document.querySelector(`input[name="${question.id}"][value="${CSS.escape(responseValue)}"]`);
                if (selectedRadio) {
                    selectedRadio.checked = true;
                    selectedRadio.closest('.option').classList.add('selected');
                }
            }
        }

        if ((question.type === 'email' || question.type === 'short_text') && this.responses[question.id]) {
            const input = document.querySelector(`input[name="${question.id}"]`);
            if (input) {
                input.value = this.responses[question.id];
            }
        }

        if (question.type === 'open_text' && this.responses[question.id]) {
            const textarea = document.querySelector(`textarea[name="${question.id}"]`);
            if (textarea) {
                textarea.value = this.responses[question.id];
            }
        }

        if (question.type === 'rating' && this.responses[question.id]) {
            const ratingOption = document.querySelector(`.rating-option[data-value="${this.responses[question.id]}"]`);
            if (ratingOption) {
                ratingOption.classList.add('selected');
            }
        }
    }

    renderQuestionInput(question) {
        switch (question.type) {
            case 'multiple_choice': {
                const hasOther = question.options.some(opt => opt.toLowerCase() === 'other');
                const optionsHtml = question.options.map(option => `
                    <label class="option">
                        <input type="radio" name="${question.id}" value="${option.replace(/"/g, '&quot;')}" data-is-other="${option.toLowerCase() === 'other'}">
                        ${this.escapeHtml(option)}
                    </label>
                `).join('');

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
            }

            case 'rating': {
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
            }

            case 'open_text':
                return `
                    <textarea
                        class="text-input"
                        name="${question.id}"
                        placeholder="${this.escapeHtml(question.placeholder || 'Please enter your response...')}"
                        rows="4"
                    ></textarea>
                `;

            case 'email':
                return `
                    <input
                        type="email"
                        class="text-input short-input"
                        name="${question.id}"
                        placeholder="${this.escapeHtml(question.placeholder || 'your.email@example.com')}"
                        autocomplete="email"
                    >
                `;

            case 'short_text':
                return `
                    <input
                        type="text"
                        class="text-input short-input"
                        name="${question.id}"
                        placeholder="${this.escapeHtml(question.placeholder || 'Please enter your response...')}"
                    >
                `;

            default:
                return '<p>Unsupported question type</p>';
        }
    }

    setupEventListeners() {
        document.getElementById('nextBtn').addEventListener('click', () => {
            if (this.validateCurrentQuestion()) {
                this.saveCurrentResponse();
                this.nextQuestion();
            }
        });

        document.getElementById('prevBtn').addEventListener('click', () => {
            this.previousQuestion();
        });

        document.addEventListener('change', (e) => {
            if (e.target.type === 'radio') {
                this.updateOptionSelection(e.target);
                this.handleOtherOption(e.target);
            }
        });

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

        if (container.dataset.built !== String(this.totalQuestions)) {
            container.innerHTML = '';
            for (let i = 0; i < this.totalQuestions; i++) {
                const dot = document.createElement('span');
                dot.className = 'step-dot';
                dot.title = `Question ${i + 1}`;
                container.appendChild(dot);
            }
            container.dataset.built = String(this.totalQuestions);
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
                otherInputContainer.style.display = 'block';
                if (otherTextInput) {
                    otherTextInput.focus();
                }
            } else {
                otherInputContainer.style.display = 'none';
                if (otherTextInput) {
                    otherTextInput.value = '';
                }
            }
        }
    }

    selectRating(ratingElement) {
        const question = this.getCurrentQuestion();
        if (!question) return;
        const value = ratingElement.dataset.value;

        document.querySelectorAll('.rating-option').forEach(option => {
            option.classList.remove('selected');
        });

        ratingElement.classList.add('selected');
        this.responses[question.id] = value;
    }

    isValidEmail(value) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }

    validateCurrentQuestion() {
        const question = this.getCurrentQuestion();
        if (!question || !question.required) return true;

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
        } else if (question.type === 'email') {
            const input = document.querySelector(`input[name="${questionId}"]`);
            const value = input?.value.trim() || '';
            if (!value) {
                this.showValidationError('Please enter your email address before continuing.');
                input?.focus();
                return false;
            }
            if (!this.isValidEmail(value)) {
                this.showValidationError('Please enter a valid email address.');
                input?.focus();
                return false;
            }
        } else if (question.type === 'short_text') {
            const input = document.querySelector(`input[name="${questionId}"]`);
            if (!input?.value.trim()) {
                this.showValidationError('Please enter a short answer before continuing.');
                input?.focus();
                return false;
            }
        }

        this.clearValidationError();
        return true;
    }

    saveCurrentResponse() {
        const question = this.getCurrentQuestion();
        if (!question) return;

        const questionId = question.id;

        if (question.type === 'multiple_choice') {
            const selected = document.querySelector(`input[name="${questionId}"]:checked`);
            if (selected) {
                if (selected.dataset.isOther === 'true') {
                    const otherTextInput = document.getElementById(`${questionId}_other_text`);
                    const otherText = otherTextInput ? otherTextInput.value.trim() : '';
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
        } else if (question.type === 'email' || question.type === 'short_text') {
            const input = document.querySelector(`input[name="${questionId}"]`);
            if (input) {
                this.responses[questionId] = input.value.trim();
            }
        }

        this.pruneHiddenResponses();
        this.refreshVisibleQuestions();
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
            questionnaire_id: this.questionnaireId,
            ref: this.refParam,
            responses: this.responses,
            completion_time: Date.now() - this.startTime,
            user_agent: navigator.userAgent,
            anonymous: this.settings.anonymous
        };

        const existingResponses = JSON.parse(localStorage.getItem('questionnaire_responses') || '[]');
        existingResponses.push(responseData);
        localStorage.setItem('questionnaire_responses', JSON.stringify(existingResponses));

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
        const reward = this.settings.completion_reward ||
            'Your responses have been recorded and will help us understand common challenges better.';

        this.clearValidationError();
        form.innerHTML = `
            <div class="completion-message">
                <h2>Thank you!</h2>
                <p>${this.escapeHtml(reward)}</p>
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
    }

    showError(message) {
        const form = document.getElementById('questionnaireForm');
        form.innerHTML = `
            <div class="completion-message">
                <h2 style="color: #dc3545;">Error</h2>
                <p>${this.escapeHtml(message)}</p>
                <button class="btn btn-primary" onclick="location.reload()">Try Again</button>
            </div>
        `;
    }
}

function notifyHeightIfEmbedded() {
    if (typeof notifyHeight === 'function') notifyHeight();
}

document.addEventListener('DOMContentLoaded', () => {
    new QuestionnaireEngine();
});
