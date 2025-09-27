// Problem Identification Questionnaire JavaScript
class QuestionnaireEngine {
    constructor() {
        this.currentQuestion = 0;
        this.responses = {};
        this.questions = [];
        this.totalQuestions = 0;
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
            const response = await fetch('../data/questionnaires.json');
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
            },
            {
                id: "q5",
                type: "open_text",
                question: "What would be your ideal solution to these challenges?",
                placeholder: "Describe what would help you most...",
                required: false
            }
        ];
    }

    renderQuestion() {
        const form = document.getElementById('questionnaireForm');
        const question = this.questions[this.currentQuestion];
        
        if (!question) {
            this.showCompletion();
            return;
        }

        form.innerHTML = `
            <div class="question active">
                <h3>${question.question}</h3>
                <div class="options">
                    ${this.renderQuestionInput(question)}
                </div>
                ${question.required ? '' : '<p class="skip-notice">This question is optional</p>'}
            </div>
        `;

        this.updateProgress();
        this.updateButtons();
    }

    renderQuestionInput(question) {
        switch (question.type) {
            case 'multiple_choice':
                return question.options.map(option => `
                    <label class="option">
                        <input type="radio" name="${question.id}" value="${option}">
                        ${option}
                    </label>
                `).join('');

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
            }
        });

        // Rating selection
        document.addEventListener('click', (e) => {
            if (e.target.closest('.rating-option')) {
                this.selectRating(e.target.closest('.rating-option'));
            }
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
                alert('Please select an option before continuing.');
                return false;
            }
        } else if (question.type === 'rating') {
            if (!this.responses[questionId]) {
                alert('Please select a rating before continuing.');
                return false;
            }
        } else if (question.type === 'open_text') {
            const textarea = document.querySelector(`textarea[name="${questionId}"]`);
            if (!textarea.value.trim()) {
                alert('Please provide a response before continuing.');
                return false;
            }
        }

        return true;
    }

    saveCurrentResponse() {
        const question = this.questions[this.currentQuestion];
        const questionId = question.id;
        
        if (question.type === 'multiple_choice') {
            const selected = document.querySelector(`input[name="${questionId}"]:checked`);
            if (selected) {
                this.responses[questionId] = selected.value;
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
            this.currentQuestion++;
            this.renderQuestion();
        } else {
            this.completeQuestionnaire();
        }
    }

    previousQuestion() {
        if (this.currentQuestion > 0) {
            this.currentQuestion--;
            this.renderQuestion();
        }
    }

    updateProgress() {
        const progress = ((this.currentQuestion + 1) / this.totalQuestions) * 100;
        document.getElementById('progressFill').style.width = `${progress}%`;
    }

    updateButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.style.display = this.currentQuestion === 0 ? 'none' : 'block';
        
        if (this.currentQuestion === this.totalQuestions - 1) {
            nextBtn.textContent = 'Complete Survey';
        } else {
            nextBtn.textContent = 'Next';
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

        // Try to save to JSON file (this would require a backend in production)
        // For now, we'll store in localStorage as a fallback
        const existingResponses = JSON.parse(localStorage.getItem('questionnaire_responses') || '[]');
        existingResponses.push(responseData);
        localStorage.setItem('questionnaire_responses', JSON.stringify(existingResponses));

        // Try to send to Netlify Function with localStorage fallback
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
        
        form.innerHTML = `
            <div class="completion-message">
                <h2>✅ Thank You!</h2>
                <p>Your responses have been recorded and will help us understand common challenges better.</p>
                <p>We appreciate you taking the time to share your insights!</p>
            </div>
        `;
        
        buttonGroup.style.display = 'none';
        
        // Hide progress bar
        document.getElementById('progressFill').style.width = '100%';
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

// Initialize the questionnaire when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new QuestionnaireEngine();
});
