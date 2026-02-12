from flask import Flask
from routes.companies import companies_bp
from routes.energy_supply_points import energy_supply_points_bp
from routes.company_clients import company_clients_bp


def register_routes(app: Flask):
    """Регистрация всех blueprints в приложении"""
    app.register_blueprint(companies_bp, url_prefix='/api/companies')
    app.register_blueprint(energy_supply_points_bp, url_prefix='/api/energy-supply-points')
    app.register_blueprint(company_clients_bp, url_prefix='/api/company-clients')