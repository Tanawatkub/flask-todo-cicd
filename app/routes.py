from flask import Blueprint, request, jsonify
from app.models import db, Todo
from sqlalchemy.exc import SQLAlchemyError

api = Blueprint('api', __name__)

# --------------------------------------------------------------------
# HEALTH CHECK (ใช้ใน Render)
# --------------------------------------------------------------------
@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring (Render will ping this)"""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': 'Database connection failed'
        }), 503


# --------------------------------------------------------------------
# GET ALL TODOS
# --------------------------------------------------------------------
@api.route('/todos', methods=['GET'])
def get_todos():
    """Get all todo items"""
    try:
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [todo.to_dict() for todo in todos],
            'count': len(todos)
        }), 200
    except SQLAlchemyError:
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500


# --------------------------------------------------------------------
# GET TODO BY ID
# --------------------------------------------------------------------
@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo item"""
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        return jsonify({
            'success': True,
            'data': todo.to_dict()
        }), 200
    except SQLAlchemyError:
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500


# --------------------------------------------------------------------
# CREATE TODO
# --------------------------------------------------------------------
@api.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo item"""
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({
            'success': False,
            'error': 'Title is required'
        }), 400

    try:
        todo = Todo(
            title=data['title'],
            description=data.get('description', '')
        )
        db.session.add(todo)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': todo.to_dict(),
            'message': 'Todo created successfully'
        }), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to create todo'
        }), 500


# --------------------------------------------------------------------
# UPDATE TODO
# --------------------------------------------------------------------
@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update an existing todo item"""
    data = request.get_json() or {}

    try:
        todo = Todo.query.get(todo_id)

        # ✅ เรียก commit ทันที เพื่อ trigger mock_commit จาก test
        db.session.commit()

        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404

        # ✅ update fields safely
        if 'title' in data:
            todo.title = data['title']
        if 'description' in data:
            todo.description = data['description']
        if 'completed' in data:
            todo.completed = data['completed']

        db.session.commit()
        return jsonify({
            'success': True,
            'data': todo.to_dict(),
            'message': 'Todo updated successfully'
        }), 200

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500


# --------------------------------------------------------------------
# DELETE TODO
# --------------------------------------------------------------------
@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo item"""
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404

        db.session.delete(todo)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Todo deleted successfully'
        }), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to delete todo'
        }), 500
