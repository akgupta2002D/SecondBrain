// dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Load classes on page load
    fetchClasses();

    // Event delegation for dynamic elements
    document.getElementById('class-list').addEventListener('click', handleClassClick);
    document.getElementById('subject-list').addEventListener('click', handleSubjectClick);
});

function fetchClasses() {
    fetch('/get_classes/')
        .then(response => response.json())
        .then(classes => {
            const classListHtml = classes.map(c => `<li class="class-item" data-id="${c.id}">${c.name}</li>`).join('');
            document.getElementById('class-list').innerHTML = classListHtml;
        })
        .catch(error => console.error('Error:', error));
}

function handleClassClick(event) {
    if (event.target.classList.contains('class-item')) {
        const classId = event.target.dataset.id;
        fetch(`/get_subjects/${classId}/`)
            .then(response => response.json())
            .then(subjects => {
                const subjectListHtml = subjects.map(s => `<li class="subject-item" data-id="${s.id}">${s.name}</li>`).join('');
                document.getElementById('subject-list').innerHTML = subjectListHtml;
                document.getElementById('topic-list').innerHTML = '';
                document.getElementById('exam-list').innerHTML = '';
            })
            .catch(error => console.error('Error:', error));
    }
}

function handleSubjectClick(event) {
    if (event.target.classList.contains('subject-item')) {
        const subjectId = event.target.dataset.id;
        Promise.all([
            fetch(`/get_topics/${subjectId}/`).then(response => response.json()),
            fetch(`/get_exams/${subjectId}/`).then(response => response.json())
        ])
        .then(([topics, exams]) => {
            const topicListHtml = topics.map(t => `<li>${t.name}</li>`).join('');
            document.getElementById('topic-list').innerHTML = topicListHtml;
            
            const examListHtml = exams.map(e => `<li>${e.title}</li>`).join('');
            document.getElementById('exam-list').innerHTML = examListHtml;
        })
        .catch(error => console.error('Error:', error));
    }
}