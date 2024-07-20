
// Call this function when the page loads
document.addEventListener('DOMContentLoaded', fetchQuestionList);
document.addEventListener('DOMContentLoaded', function() {

    
    const questionTypeSelect = document.getElementById('id_question_type');
    const dynamicFields = document.getElementById('dynamicFields');
    const imagePreview = document.getElementById('imagePreview');
    const questionForm = document.getElementById('questionForm');

    questionTypeSelect.addEventListener('change', function() {
        const selectedType = this.value;
        dynamicFields.innerHTML = '';

        switch(selectedType) {
            case 'MCQ':
            case 'IMG':
                addMultipleChoiceFields(selectedType);
                break;
            case 'TF':
                addTrueFalseField();
                break;
            case 'FIB':
                addFillInTheBlanksField();
                break;
            // For 'SA' and 'LA', we don't need to add any fields
        }
    });

    function addMultipleChoiceFields(type) {
        const choices = ['A', 'B', 'C', 'D'];
        choices.forEach(choice => {
            const field = document.createElement('div');
            field.className = 'form-group';
            field.innerHTML = `
                <label for="id_choice_${choice.toLowerCase()}">Choice ${choice}:</label>
                ${type === 'IMG' 
                    ? `<input type="file" name="choice_${choice.toLowerCase()}_image" id="id_choice_${choice.toLowerCase()}_image" class="form-control-file">
                       <div id="choiceImagePreview${choice}"></div>`
                    : `<input type="text" name="choice_${choice.toLowerCase()}" id="id_choice_${choice.toLowerCase()}" class="form-control">`
                }
                <span class="error-message" id="error_choice_${choice.toLowerCase()}"></span>
            `;
            dynamicFields.appendChild(field);
        });

        const correctChoiceField = document.createElement('div');
        correctChoiceField.className = 'form-group';
        correctChoiceField.innerHTML = `
            <label for="id_correct_choice">Correct Choice:</label>
            <select name="correct_choice" id="id_correct_choice" class="form-control">
                <option value="">Select correct choice</option>
                ${choices.map(choice => `<option value="${choice}">${choice}</option>`).join('')}
            </select>
            <span class="error-message" id="error_correct_choice"></span>
        `;
        dynamicFields.appendChild(correctChoiceField);
    }

    function addTrueFalseField() {
        const field = document.createElement('div');
        field.className = 'form-group';
        field.innerHTML = `
            <label for="id_is_true">Correct Answer:</label>
            <select name="is_true" id="id_is_true" class="form-control">
                <option value="">Select correct answer</option>
                <option value="true">True</option>
                <option value="false">False</option>
            </select>
            <span class="error-message" id="error_is_true"></span>
        `;
        dynamicFields.appendChild(field);
    }

    function addFillInTheBlanksField() {
        const field = document.createElement('div');
        field.className = 'form-group';
        field.innerHTML = `
            <label for="id_blanks_answer">Correct Answer (use underscores for blanks):</label>
            <input type="text" name="blanks_answer" id="id_blanks_answer" class="form-control">
            <span class="error-message" id="error_blanks_answer"></span>
        `;
        dynamicFields.appendChild(field);
    }

    // Image preview functionality
    function readURL(input, previewDiv) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.maxWidth = '200px';
                previewDiv.innerHTML = '';
                previewDiv.appendChild(img);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    document.getElementById('id_image').addEventListener('change', function() {
        readURL(this, imagePreview);
    });

    dynamicFields.addEventListener('change', function(e) {
        if (e.target.type === 'file' && e.target.name.startsWith('choice_')) {
            const choiceLetter = e.target.name.charAt(6).toUpperCase();
            readURL(e.target, document.getElementById(`choiceImagePreview${choiceLetter}`));
        }
    });

    // Form submission handling
    questionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccessMessage('Question created successfully!');
                this.reset();
                clearImagePreviews();
                updateQuestionList(data.question);
            } else {
                displayErrors(data.errors);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage('An error occurred. Please try again.');
        });
    });

    function showSuccessMessage(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'alert alert-success';
        successDiv.textContent = message;
        questionForm.prepend(successDiv);
        setTimeout(() => successDiv.remove(), 5000);
    }

    function showErrorMessage(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.textContent = message;
        questionForm.prepend(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    function clearImagePreviews() {
        imagePreview.innerHTML = '';
        document.querySelectorAll('[id^="choiceImagePreview"]').forEach(el => el.innerHTML = '');
    }

    function displayErrors(errors) {
        // Clear previous errors
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');

        // Display new errors
        for (const field in errors) {
            const errorMessage = errors[field].join(' ');
            const errorElement = document.getElementById(`error_${field}`);
            if (errorElement) {
                errorElement.textContent = errorMessage;
            }
        }
    }

    function updateQuestionList(question) {
        fetchQuestionList();  // Fetch the entire updated list
    }

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

function fetchQuestionList() {
    fetch('/exam-quest/questions/')  // Adjust this URL to match your actual URL
        .then(response => response.json())
        .then(data => {
            const listContainer = document.getElementById('questionListContainer');
            listContainer.innerHTML = '';  // Clear existing list
            data.questions.forEach(question => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <strong>${question.text}</strong><br>
                    Topic: ${question.topic}<br>
                    Difficulty: ${question.difficulty}<br>
                    Type: ${question.question_type}
                `;
                listContainer.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching questions:', error));
}
