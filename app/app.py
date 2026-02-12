import os
from flask import Flask, jsonify
from models import db
from routes import register_routes
from error_handlers import register_error_handlers


app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@db:5432/energy_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db.init_app(app)

# Регистрация маршрутов
register_routes(app)

# Регистрация обработчиков ошибок
register_error_handlers(app)


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка состояния API"""
    return jsonify({
        'status': 'healthy',
        'message': 'Energy Supply API is running'
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
