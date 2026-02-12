from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import HTTPException
from models import db


class APIError(Exception):
    """Базовый класс для API ошибок"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv


class ValidationError(APIError):
    """Ошибка валидации данных"""
    
    def __init__(self, message, payload=None):
        super().__init__(message, status_code=400, payload=payload)


class NotFoundError(APIError):
    """Ресурс не найден"""
    
    def __init__(self, message="Resource not found", payload=None):
        super().__init__(message, status_code=404, payload=payload)


class DatabaseError(APIError):
    """Ошибка базы данных"""
    
    def __init__(self, message="Database error occurred", payload=None):
        super().__init__(message, status_code=500, payload=payload)


def register_error_handlers(app):
    """
    Регистрация всех обработчиков ошибок для приложения Flask.
    
    Args:
        app: экземпляр Flask приложения
    """
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Обработчик кастомных API ошибок"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Обработчик ошибок валидации"""
        response = jsonify({
            'error': error.message,
            'type': 'ValidationError'
        })
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        """Обработчик ошибок 'не найдено'"""
        response = jsonify({
            'error': error.message,
            'type': 'NotFoundError'
        })
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        """Обработчик ошибок базы данных"""
        db.session.rollback()
        response = jsonify({
            'error': error.message,
            'type': 'DatabaseError'
        })
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        """Обработчик HTTP 404"""
        return jsonify({
            'error': 'Resource not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        """Обработчик HTTP 400"""
        return jsonify({
            'error': 'Bad request',
            'status_code': 400,
            'message': str(error) if hasattr(error, 'description') else 'Invalid request data'
        }), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Обработчик HTTP 405"""
        return jsonify({
            'error': 'Method not allowed',
            'status_code': 405
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Обработчик HTTP 500"""
        db.session.rollback()
        return jsonify({
            'error': 'Internal server error',
            'status_code': 500
        }), 500
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Обработчик ошибок целостности БД (дубликаты, внешние ключи и т.д.)"""
        db.session.rollback()
        
        error_message = 'Database integrity error'
        
        error_str = str(error.orig) if hasattr(error, 'orig') else str(error)
        
        if 'unique constraint' in error_str.lower() or 'duplicate key' in error_str.lower():
            error_message = 'Record with this data already exists'
        elif 'foreign key constraint' in error_str.lower():
            error_message = 'Related record not found or cannot be deleted due to existing references'
        elif 'not null constraint' in error_str.lower():
            error_message = 'Required field is missing'
        
        return jsonify({
            'error': error_message,
            'type': 'IntegrityError',
            'status_code': 400
        }), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        """Обработчик общих ошибок SQLAlchemy"""
        db.session.rollback()
        
        return jsonify({
            'error': 'Database operation failed',
            'type': 'SQLAlchemyError',
            'status_code': 500
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Обработчик HTTP исключений Werkzeug"""
        return jsonify({
            'error': error.description,
            'status_code': error.code
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Обработчик всех необработанных исключений"""
        db.session.rollback()
        
        # наверное на проде надо будет убрать
        if app.config.get('DEBUG'):
            error_message = str(error)
        else:
            error_message = 'An unexpected error occurred'
        
        return jsonify({
            'error': error_message,
            'type': 'InternalError',
            'status_code': 500
        }), 500
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Обработчик ошибок ValueError"""
        return jsonify({
            'error': str(error),
            'type': 'ValueError',
            'status_code': 400
        }), 400
    
    @app.errorhandler(KeyError)
    def handle_key_error(error):
        """Обработчик ошибок KeyError"""
        return jsonify({
            'error': f'Missing required field: {str(error)}',
            'type': 'KeyError',
            'status_code': 400
        }), 400
    
    @app.errorhandler(TypeError)
    def handle_type_error(error):
        """Обработчик ошибок TypeError"""
        return jsonify({
            'error': f'Invalid data type: {str(error)}',
            'type': 'TypeError',
            'status_code': 400
        }), 400
