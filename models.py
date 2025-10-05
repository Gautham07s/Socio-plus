from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User model for both Volunteers and Organizations
    UserMixin provides default implementations for Flask-Login
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'volunteer' or 'organization'
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    # If user is an organization, they can post opportunities
    opportunities = db.relationship('Opportunity', backref='organization', lazy=True, cascade='all, delete-orphan')
    # If user is a volunteer, they can submit applications
    applications = db.relationship('Application', backref='volunteer', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash password before storing"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Opportunity(db.Model):
    """
    Volunteer opportunities posted by organizations
    """
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(50))  # e.g., "3 hours", "Full day"
    skills_required = db.Column(db.String(200))
    spots_available = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='open')  # 'open', 'closed', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to organization that posted it
    org_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    applications = db.relationship('Application', backref='opportunity', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Opportunity {self.title}>'


class Application(db.Model):
    """
    Applications submitted by volunteers for opportunities
    """
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)  # Cover letter / why they want to volunteer
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    
    # Ensure a user can only apply once to each opportunity
    __table_args__ = (db.UniqueConstraint('user_id', 'opportunity_id', name='unique_application'),)
    
    def __repr__(self):
        return f'<Application {self.id} - Status: {self.status}>'