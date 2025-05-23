from flask import Blueprint, request, jsonify, render_template, send_from_directory
from src.models.task import db, Task
from src.models.content import SiteContent
import os
import json

# Create blueprint for main site integration
main_bp = Blueprint('main', __name__)

@main_bp.route('/update-todo', methods=['POST'])
def update_todo():
    """
    Update the main site's to-do section with the latest tasks from the database
    """
    try:
        # Get all tasks from database
        tasks = Task.query.all()
        tasks_by_category = {
            'design': [],
            'site': [],
            'yandex': [],
            'strategy': []
        }
        
        # Group tasks by category
        for task in tasks:
            task_dict = task.to_dict()
            if task.category in tasks_by_category:
                tasks_by_category[task.category].append(task_dict)
        
        # Generate HTML for each task category
        todo_html = generate_todo_html(tasks_by_category)
        
        # Update the main site's to-do section
        update_main_site_todo(todo_html)
        
        return jsonify({
            'success': True,
            'message': 'Main site updated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@main_bp.route('/manual', methods=['GET'])
def manual():
    """
    Serve the admin panel manual
    """
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'), 'manual.html')

def generate_todo_html(tasks_by_category):
    """
    Generate HTML for the to-do section based on tasks
    """
    html = ""
    
    # Generate HTML for each category
    for category, tasks in tasks_by_category.items():
        if tasks:
            category_title = get_category_title(category)
            html += f'<h3>{category_title}</h3>\n<div class="todo-list">\n'
            
            for task in tasks:
                status_class = f"status-{task['status']}"
                urgency_class = f"urgency-{task['urgency']}"
                
                html += f'''
                <div class="todo-item {status_class} {urgency_class}">
                    <div class="todo-header">
                        <h4>{task['title']}</h4>
                        <div class="todo-meta">
                            <span class="todo-urgency">{get_urgency_text(task['urgency'])}</span>
                            <span class="todo-deadline">{format_deadline(task['deadline'])}</span>
                            <span class="todo-status">{get_status_text(task['status'])}</span>
                        </div>
                    </div>
                    <div class="todo-details">
                        <p>{task['description'] or 'Нет описания'}</p>
                    </div>
                </div>
                '''
            
            html += '</div>\n'
    
    return html

def get_category_title(category):
    """
    Get human-readable category title
    """
    titles = {
        'design': 'Задачи по направлению "Дизайн"',
        'site': 'Задачи по направлению "Сайт"',
        'yandex': 'Задачи по направлению "Яндекс.Бизнес"',
        'strategy': 'Задачи по направлению "Стратегия"'
    }
    return titles.get(category, f'Задачи по направлению "{category}"')

def get_urgency_text(urgency):
    """
    Get human-readable urgency text
    """
    texts = {
        'high': 'Высокая срочность',
        'medium': 'Средняя срочность',
        'low': 'Низкая срочность'
    }
    return texts.get(urgency, 'Неизвестная срочность')

def get_status_text(status):
    """
    Get human-readable status text
    """
    texts = {
        'waiting': 'Ожидание',
        'in-progress': 'В процессе',
        'completed': 'Завершено'
    }
    return texts.get(status, 'Неизвестный статус')

def format_deadline(deadline):
    """
    Format deadline date
    """
    if not deadline:
        return 'Без срока'
    return f'Срок: {deadline}'

def update_main_site_todo(todo_html):
    """
    Update the main site's to-do section HTML
    """
    # Path to the main site's index.html
    main_site_path = '/home/ubuntu/website/index.html'
    
    try:
        # Read the current index.html
        with open(main_site_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the to-do section
        start_marker = '<!-- BEGIN TODO SECTION -->'
        end_marker = '<!-- END TODO SECTION -->'
        
        start_index = content.find(start_marker)
        end_index = content.find(end_marker)
        
        if start_index != -1 and end_index != -1:
            # Replace the to-do section content
            new_content = content[:start_index + len(start_marker)] + '\n' + todo_html + '\n' + content[end_index:]
            
            # Write the updated content back to the file
            with open(main_site_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
        else:
            # If markers not found, try to find the process section and insert the to-do content
            process_section = '<section id="process" class="process">'
            process_index = content.find(process_section)
            
            if process_index != -1:
                # Find the container div after the section tag
                container_start = content.find('<div class="container">', process_index)
                
                if container_start != -1:
                    # Find the end of the section title
                    title_end = content.find('</h2>', container_start)
                    
                    if title_end != -1:
                        # Insert the to-do content after the section title
                        insert_position = title_end + 5  # Length of </h2>
                        new_content = (
                            content[:insert_position] + 
                            f'\n{start_marker}\n{todo_html}\n{end_marker}\n' + 
                            content[insert_position:]
                        )
                        
                        # Write the updated content back to the file
                        with open(main_site_path, 'w', encoding='utf-8') as file:
                            file.write(new_content)
    except Exception as e:
        print(f"Error updating main site: {str(e)}")
        raise
