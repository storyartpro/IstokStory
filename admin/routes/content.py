from flask import Blueprint, request, jsonify, current_app
from src.models.content import db, SiteContent

content_bp = Blueprint('content', __name__)

@content_bp.route('/content', methods=['GET'])
def get_all_content():
    try:
        content_items = SiteContent.query.all()
        return jsonify({
            'success': True,
            'content': [item.to_dict() for item in content_items]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@content_bp.route('/content/<section>', methods=['GET'])
def get_content_by_section(section):
    try:
        content_items = SiteContent.query.filter_by(section=section).all()
        return jsonify({
            'success': True,
            'content': [item.to_dict() for item in content_items]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@content_bp.route('/content/<section>/<key>', methods=['GET'])
def get_content_item(section, key):
    try:
        content_item = SiteContent.query.filter_by(section=section, key=key).first()
        if not content_item:
            return jsonify({
                'success': False,
                'message': 'Content item not found'
            }), 404
        
        return jsonify({
            'success': True,
            'content': content_item.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@content_bp.route('/content', methods=['POST'])
def create_content():
    try:
        data = request.json
        
        # Check if content already exists
        existing = SiteContent.query.filter_by(
            section=data['section'], 
            key=data['key']
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'message': 'Content with this section and key already exists'
            }), 400
        
        new_content = SiteContent(
            section=data['section'],
            key=data['key'],
            value=data.get('value', '')
        )
        
        db.session.add(new_content)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'content': new_content.to_dict(),
            'message': 'Content created successfully'
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

@content_bp.route('/content/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    try:
        content_item = SiteContent.query.get(content_id)
        if not content_item:
            return jsonify({
                'success': False,
                'message': 'Content item not found'
            }), 404
        
        data = request.json
        
        if 'section' in data:
            content_item.section = data['section']
        
        if 'key' in data:
            content_item.key = data['key']
        
        if 'value' in data:
            content_item.value = data['value']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'content': content_item.to_dict(),
            'message': 'Content updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@content_bp.route('/content/<int:content_id>', methods=['DELETE'])
def delete_content(content_id):
    try:
        content_item = SiteContent.query.get(content_id)
        if not content_item:
            return jsonify({
                'success': False,
                'message': 'Content item not found'
            }), 404
        
        db.session.delete(content_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Content deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
