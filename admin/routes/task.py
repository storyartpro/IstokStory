from flask import Blueprint, request, jsonify, current_app
from src.models.task import db, Task
from datetime import datetime
import json

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        return jsonify({
            'success': True,
            'tasks': [task.to_dict() for task in tasks]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
        
        return jsonify({
            'success': True,
            'task': task.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        
        # Parse deadline if provided
        deadline = None
        if data.get('deadline'):
            try:
                deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid date format for deadline. Use YYYY-MM-DD.'
                }), 400
        
        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            category=data['category'],
            urgency=data['urgency'],
            deadline=deadline,
            status=data.get('status', 'waiting')
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': new_task.to_dict(),
            'message': 'Task created successfully'
        }), 201
    except KeyError as e:
        return jsonify({
            'success': False,
            'message': f'Missing required field: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
        
        data = request.json
        
        if 'title' in data:
            task.title = data['title']
        
        if 'description' in data:
            task.description = data['description']
        
        if 'category' in data:
            task.category = data['category']
        
        if 'urgency' in data:
            task.urgency = data['urgency']
        
        if 'status' in data:
            task.status = data['status']
        
        if 'deadline' in data and data['deadline']:
            try:
                task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid date format for deadline. Use YYYY-MM-DD.'
                }), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': 'Task updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_bp.route('/tasks/category/<category>', methods=['GET'])
def get_tasks_by_category(category):
    try:
        tasks = Task.query.filter_by(category=category).all()
        return jsonify({
            'success': True,
            'tasks': [task.to_dict() for task in tasks]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
