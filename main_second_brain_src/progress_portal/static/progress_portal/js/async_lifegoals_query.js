document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/progress_portal/api/life_goals/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        const contentDiv = document.getElementById('life_goals_display');
        data.forEach(item => {
            const lifeGoalList = document.createElement('ul');
            const lifeGoalLink = document.createElement('a');
            lifeGoalLink.href = `/life_goal/${item.id}`; // Adjust the href as needed
            lifeGoalLink.classList.add('life_goal_title');
            lifeGoalLink.textContent = item.life_goal;
            
            const lifeGoalListItem = document.createElement('li');
            lifeGoalListItem.appendChild(lifeGoalLink);
            lifeGoalList.appendChild(lifeGoalListItem);

            item.projects.forEach(project => {
                const projectListItem = document.createElement('li');
                const projectLink = document.createElement('a');
                projectLink.href = `/project/${project.id}`; // Adjust the href as needed
                projectLink.classList.add('project_title');
                projectLink.textContent = project.title;
                projectListItem.appendChild(projectLink);
                lifeGoalList.appendChild(projectListItem);
            });

            contentDiv.appendChild(lifeGoalList);
        });
    } catch (error) {
        console.error('Error fetching life goals and projects:', error);
    }
});
