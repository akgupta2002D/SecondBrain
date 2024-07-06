async function handleLifeGoalClick(event) {
    event.preventDefault();
    console.log("handleLifeGoalClick triggered"); // Debug log
    const lifeGoalId = event.currentTarget.dataset.id;
    try {
        const response = await fetch(`/progress_portal/life_goal/${lifeGoalId}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const lifeGoalData = await response.json();
        console.log("Life goal data fetched:", lifeGoalData); // Debug log
        displayLifeGoalData(lifeGoalData);
    } catch (error) {
        console.error('Error fetching life goal data:', error);
    }
}

async function handleProjectClick(event) {
    event.preventDefault();
    console.log("handleProjectClick triggered"); // Debug log
    const projectId = event.currentTarget.dataset.id;
    try {
        const response = await fetch(`/progress_portal/projects/${projectId}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const projectData = await response.json();
        console.log("Project data fetched:", projectData); // Debug log
        displayProjectData(projectData);
    } catch (error) {
        console.error('Error fetching project data:', error);
    }
}

function displayLifeGoalData(data) {
    const taskViewDiv = document.querySelector('.task_view');
    if (!taskViewDiv) {
        console.error("task_view div not found"); // Debug log
        return;
    }
    taskViewDiv.innerHTML = ''; // Clear previous content
    const newDiv = document.createElement('div');
    newDiv.classList.add('life_goal_detail');
    newDiv.innerHTML = `
        <div class="life_goal_header">
            <img src="${data.icon}" class="life_goal_icon">
            <h2>${data.life_goal}</h2>
        </div>
        <p>${data.description}</p>
        <h2 class="project_label">Projects</h2>
        <div class="line"></div>
        <ul>
            ${data.projects.map(project => `
                <li>
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                </li>
            `).join('')}
        </ul>
    `;
    console.log("Appending life goal data to task_view div"); // Debug log
    taskViewDiv.appendChild(newDiv);
}

function displayProjectData(data) {
    const taskViewDiv = document.querySelector('.task_view');
    if (!taskViewDiv) {
        console.error("task_view div not found"); // Debug log
        return;
    }
    taskViewDiv.innerHTML = ''; // Clear previous content
    const newDiv = document.createElement('div');
    newDiv.classList.add('project_detail');
    newDiv.innerHTML = `
        <h2>${data.title}</h2>
        <p>${data.description}</p>
        <h2 class="project_label">Todo:</h2>
        <div class="line"></div>
        <ul>
            ${data.todo_items.map(item => `
                <li>
                    <label class="custom-checkbox">
                        <input name="dummy" type="checkbox" ${item.completed ? 'checked' : ''}>
                        <span class="checkmark"></span>
                    </label>
                    <h3>${item.title}</h3>
                    
                    <p>${item.description}</p> 

                    <div class="priority">
                            <label>
                                Priority:
                                <select>
                                    <option value="1" ${item.priority === 'Low' ? 'selected' : ''}>Low</option>
                                    <option value="2" ${item.priority === 'Medium' ? 'selected' : ''}>Medium</option>
                                    <option value="3" ${item.priority === 'High' ? 'selected' : ''}>High</option>
                                </select>
                            </label>
                        </div>
                    ${item.files ? `<a href="${item.files}" target="_blank">View File</a>` : ''}
                </li>
            `).join('')}
        </ul>
    `;
    console.log("Appending project data to task_view div"); // Debug log
    taskViewDiv.appendChild(newDiv);
}
