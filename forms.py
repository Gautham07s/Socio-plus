from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    """
    Form for user registration (both volunteers and organizations)
    """
    name = StringField('Full Name / Organization Name', 
                       validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    role = SelectField('I am a', 
                      choices=[('volunteer', 'Volunteer'), ('organization', 'Organization')],
                      validators=[DataRequired()])
    phone = StringField('Phone Number', 
                       validators=[Length(max=20)])
    location = StringField('Location', 
                          validators=[Length(max=100)])
    
    def validate_email(self, email):
        """Custom validator to check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


class LoginForm(FlaskForm):
    """
    Form for user login
    """
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])


class OpportunityForm(FlaskForm):
    """
    Form for organizations to create volunteer opportunities
    """
    title = StringField('Opportunity Title', 
                       validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', 
                               validators=[DataRequired(), Length(min=20)])
    location = StringField('Location', 
                          validators=[DataRequired(), Length(max=100)])
    date = DateField('Date', 
                    validators=[DataRequired()], 
                    format='%Y-%m-%d')
    duration = StringField('Duration (e.g., 3 hours, Full day)', 
                          validators=[Length(max=50)])
    skills_required = StringField('Skills Required (comma-separated)', 
                                 validators=[Length(max=200)])
    spots_available = IntegerField('Number of Spots Available', 
                                  validators=[DataRequired()], 
                                  default=1)


class ApplicationForm(FlaskForm):
    """
    Form for volunteers to apply to opportunities
    """
    message = TextAreaField('Why do you want to volunteer for this opportunity?', 
                           validators=[DataRequired(), Length(min=20, max=500)])