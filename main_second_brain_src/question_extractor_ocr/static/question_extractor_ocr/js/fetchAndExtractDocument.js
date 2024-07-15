document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const extractBtn = document.getElementById('extract-btn');
    const fileDisplay = document.getElementById('file-display');
    const extractedText = document.getElementById('extracted-text');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(uploadForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                extractBtn.style.display = 'block';
                extractBtn.setAttribute('data-file-id', data.file_id);
                fileDisplay.innerHTML = `<img src="${data.file_url}" style="max-width:100%;">`;
                
            } else {
                alert('Upload failed');
            }
        });
    });

    extractBtn.addEventListener('click', function() {
        const fileId = this.getAttribute('data-file-id');
        const formData = new FormData();
        formData.append('file_id', fileId);

        fetch('/ocr/extract/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                extractedText.innerText = data.extracted_text;
            } else {
                alert('Extraction failed');
            }
        });
    });
});