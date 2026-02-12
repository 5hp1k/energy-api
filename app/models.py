from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Company(db.Model):
    """Модель компании-поставщика энергии"""
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    energy_supply_points = db.relationship('EnergySupplyPoint', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class EnergySupplyPoint(db.Model):
    """Модель точки поставки электроэнергии"""
    __tablename__ = 'energy_supply_points'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    connection_date = db.Column(db.Date, nullable=False)
    max_power_kw = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company_clients = db.relationship('CompanyClient', backref='energy_supply_point', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'company_id': self.company_id,
            'connection_date': self.connection_date.isoformat() if self.connection_date else None,
            'max_power_kw': float(self.max_power_kw) if self.max_power_kw else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CompanyClient(db.Model):
    """Модель клиента компании"""
    __tablename__ = 'company_clients'
    
    id = db.Column(db.Integer, primary_key=True)
    energy_supply_point_id = db.Column(db.Integer, db.ForeignKey('energy_supply_points.id'), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    quantity_power = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'energy_supply_point_id': self.energy_supply_point_id,
            'company_name': self.company_name,
            'quantity_power': float(self.quantity_power) if self.quantity_power else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
