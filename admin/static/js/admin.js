// Admin panel JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const loginContainer = document.getElementById('login-container');
    const adminContainer = document.getElementById('admin-container');
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');
    const usernameDisplay = document.getElementById('username-display');
    const logoutBtn = document.getElementById('logout-btn');
    const saveMessage = document.getElementById('saveMessage');
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const addTaskForm = document.getElementById('addTaskForm');
    const designTasksList = document.getElementById('designTasks');
    const siteTasksList = document.getElementById('siteTasks');
    const yandexTasksList = document.getElementById('yandexTasks');
    const strategyTasksList = document.getElementById('strategyTasks');
    const editTaskModal = document.getElementById('editTaskModal');
    const editTaskForm = document.getElementById('editTaskForm');
    const closeModalBtn = document.querySelector('.close');
    
    // API Base URL
    const API_BASE_URL = '/api';
    
    // Check if user is logged in
    function checkAuth() {
        const token = localStorage.getItem('token');
        if (token) {
            // Verify token validity
            fetch(`${API_BASE_URL}/auth/profile`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAdminPanel(data.user);
                } else {
                    showLoginForm();
                }
            })
            .catch(error => {
                console.error('Auth check error:', error);
                showLoginForm();
            });
        } else {
            showLoginForm();
        }
    }
    
    // Show login form
    function showLoginForm() {
        loginContainer.style.display = 'block';
        adminContainer.style.display = 'none';
        localStorage.removeItem('token');
    }
    
    // Show admin panel
    function showAdminPanel(user) {
        loginContainer.style.display = 'none';
        adminContainer.style.display = 'block';
        usernameDisplay.textContent = user.username;
        
        // Load tasks
        loadTasks();
        
        // Load content
        loadContent();
    }
    
    // Handle login form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                localStorage.setItem('token', data.token);
                showAdminPanel(data.user);
                loginError.style.display = 'none';
            } else {
                loginError.textContent = data.message;
                loginError.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            loginError.textContent = 'Ошибка при попытке входа. Попробуйте позже.';
            loginError.style.display = 'block';
        });
    });
    
    // Handle logout
    logoutBtn.addEventListener('click', function() {
        showLoginForm();
    });
    
    // Tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Hide all tab contents
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Show the corresponding tab content
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Load tasks from API
    function loadTasks() {
        const token = localStorage.getItem('token');
        
        fetch(`${API_BASE_URL}/tasks`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear task lists
                designTasksList.innerHTML = '';
                siteTasksList.innerHTML = '';
                yandexTasksList.innerHTML = '';
                strategyTasksList.innerHTML = '';
                
                // Sort tasks by category
                data.tasks.forEach(task => {
                    const taskElement = createTaskElement(task);
                    
                    switch(task.category) {
                        case 'design':
                            designTasksList.appendChild(taskElement);
                            break;
                        case 'site':
                            siteTasksList.appendChild(taskElement);
                            break;
                        case 'yandex':
                            yandexTasksList.appendChild(taskElement);
                            break;
                        case 'strategy':
                            strategyTasksList.appendChild(taskElement);
                            break;
                    }
                });
            } else {
                console.error('Failed to load tasks:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading tasks:', error);
        });
    }
    
    // Create task element
    function createTaskElement(task) {
        const taskItem = document.createElement('div');
        taskItem.className = 'task-item';
        taskItem.dataset.id = task.id;
        
        const taskInfo = document.createElement('div');
        taskInfo.className = 'task-info';
        
        const taskTitle = document.createElement('div');
        taskTitle.className = 'task-title';
        taskTitle.textContent = task.title;
        
        const taskMeta = document.createElement('div');
        taskMeta.className = 'task-meta';
        
        // Urgency span
        const urgencySpan = document.createElement('span');
        urgencySpan.className = `status-${task.urgency}`;
        urgencySpan.textContent = getUrgencyText(task.urgency);
        
        // Deadline span
        const deadlineSpan = document.createElement('span');
        deadlineSpan.textContent = task.deadline ? `Срок: ${formatDate(task.deadline)}` : 'Без срока';
        
        // Status span
        const statusSpan = document.createElement('span');
        statusSpan.className = `status-${task.status}`;
        statusSpan.textContent = getStatusText(task.status);
        
        taskMeta.appendChild(urgencySpan);
        taskMeta.appendChild(document.createTextNode(' | '));
        taskMeta.appendChild(deadlineSpan);
        taskMeta.appendChild(document.createTextNode(' | '));
        taskMeta.appendChild(statusSpan);
        
        taskInfo.appendChild(taskTitle);
        taskInfo.appendChild(taskMeta);
        
        const taskActions = document.createElement('div');
        taskActions.className = 'task-actions';
        
        const editButton = document.createElement('button');
        editButton.className = 'btn-primary edit-task';
        editButton.textContent = 'Редактировать';
        editButton.addEventListener('click', function() {
            openEditTaskModal(task);
        });
        
        const deleteButton = document.createElement('button');
        deleteButton.className = 'btn-danger delete-task';
        deleteButton.textContent = 'Удалить';
        deleteButton.addEventListener('click', function() {
            deleteTask(task.id);
        });
        
        taskActions.appendChild(editButton);
        taskActions.appendChild(deleteButton);
        
        taskItem.appendChild(taskInfo);
        taskItem.appendChild(taskActions);
        
        return taskItem;
    }
    
    // Format date
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU');
    }
    
    // Get urgency text
    function getUrgencyText(urgency) {
        switch(urgency) {
            case 'high': return 'Высокая срочность';
            case 'medium': return 'Средняя срочность';
            case 'low': return 'Низкая срочность';
            default: return 'Неизвестная срочность';
        }
    }
    
    // Get status text
    function getStatusText(status) {
        switch(status) {
            case 'waiting': return 'Ожидание';
            case 'in-progress': return 'В процессе';
            case 'completed': return 'Завершено';
            default: return 'Неизвестный статус';
        }
    }
    
    // Add task form submission
    addTaskForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const token = localStorage.getItem('token');
        const taskData = {
            title: document.getElementById('taskTitle').value,
            description: document.getElementById('taskDescription').value,
            category: document.getElementById('taskCategory').value,
            urgency: document.getElementById('taskUrgency').value,
            deadline: document.getElementById('taskDeadline').value || null,
            status: document.getElementById('taskStatus').value
        };
        
        fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(taskData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reset form
                addTaskForm.reset();
                
                // Show success message
                showSaveMessage();
                
                // Reload tasks
                loadTasks();
                
                // Update main site
                updateMainSite();
            } else {
                console.error('Failed to add task:', data.message);
            }
        })
        .catch(error => {
            console.error('Error adding task:', error);
        });
    });
    
    // Open edit task modal
    function openEditTaskModal(task) {
        // Fill form with task data
        document.getElementById('editTaskId').value = task.id;
        document.getElementById('editTaskTitle').value = task.title;
        document.getElementById('editTaskDescription').value = task.description || '';
        document.getElementById('editTaskCategory').value = task.category;
        document.getElementById('editTaskUrgency').value = task.urgency;
        document.getElementById('editTaskDeadline').value = task.deadline || '';
        document.getElementById('editTaskStatus').value = task.status;
        
        // Show modal
        editTaskModal.style.display = 'block';
    }
    
    // Close modal when clicking on X
    closeModalBtn.addEventListener('click', function() {
        editTaskModal.style.display = 'none';
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === editTaskModal) {
            editTaskModal.style.display = 'none';
        }
    });
    
    // Edit task form submission
    editTaskForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const token = localStorage.getItem('token');
        const taskId = document.getElementById('editTaskId').value;
        const taskData = {
            title: document.getElementById('editTaskTitle').value,
            description: document.getElementById('editTaskDescription').value,
            category: document.getElementById('editTaskCategory').value,
            urgency: document.getElementById('editTaskUrgency').value,
            deadline: document.getElementById('editTaskDeadline').value || null,
            status: document.getElementById('editTaskStatus').value
        };
        
        fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(taskData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close modal
                editTaskModal.style.display = 'none';
                
                // Show success message
                showSaveMessage();
                
                // Reload tasks
                loadTasks();
                
                // Update main site
                updateMainSite();
            } else {
                console.error('Failed to update task:', data.message);
            }
        })
        .catch(error => {
            console.error('Error updating task:', error);
        });
    });
    
    // Delete task
    function deleteTask(taskId) {
        if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
            const token = localStorage.getItem('token');
            
            fetch(`${API_BASE_URL}/tasks/${taskId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showSaveMessage();
                    
                    // Reload tasks
                    loadTasks();
                    
                    // Update main site
                    updateMainSite();
                } else {
                    console.error('Failed to delete task:', data.message);
                }
            })
            .catch(error => {
                console.error('Error deleting task:', error);
            });
        }
    }
    
    // Load content
    function loadContent() {
        const token = localStorage.getItem('token');
        
        fetch(`${API_BASE_URL}/content`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Fill content forms
                data.content.forEach(item => {
                    const inputId = `${item.section}${capitalizeFirstLetter(item.key)}`;
                    const input = document.getElementById(inputId);
                    if (input) {
                        input.value = item.value;
                    }
                });
            } else {
                console.error('Failed to load content:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading content:', error);
        });
    }
    
    // Capitalize first letter
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    // Show save message
    function showSaveMessage() {
        saveMessage.style.display = 'block';
        setTimeout(() => {
            saveMessage.style.display = 'none';
        }, 3000);
    }
    
    // Update main site
    function updateMainSite() {
        // This function will be called after any task changes
        // It will update the main site's to-do section via fetch API
        fetch('/update-todo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Main site updated:', data);
        })
        .catch(error => {
            console.error('Error updating main site:', error);
        });
    }
    
    // Initialize
    checkAuth();
});
