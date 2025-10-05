from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, User, Opportunity, Application
from forms import RegistrationForm, LoginForm, OpportunityForm, ApplicationForm
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


# ========== PUBLIC ROUTES ==========

@app.route('/')
def index():
    """Homepage"""
    # Get statistics for homepage
    stats = {
        'total_opportunities': Opportunity.query.filter_by(status='open').count(),
        'total_volunteers': User.query.filter_by(role='volunteer').count(),
        'total_organizations': User.query.filter_by(role='organization').count()
    }
    
    # Get 6 most recent opportunities
    recent_opportunities = Opportunity.query.filter_by(status='open').order_by(
        Opportunity.created_at.desc()
    ).limit(6).all()
    
    return render_template('index.html', stats=stats, recent_opportunities=recent_opportunities)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data,
            phone=form.phone.data,
            location=form.location.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created successfully! Welcome, {user.name}!', 'success')
        login_user(user)
        
        # Redirect based on role
        if user.role == 'volunteer':
            return redirect(url_for('volunteer_dashboard'))
        else:
            return redirect(url_for('org_dashboard'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to the page they were trying to access, or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.role == 'volunteer':
                return redirect(url_for('volunteer_dashboard'))
            else:
                return redirect(url_for('org_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


@app.route('/opportunities')
def opportunities():
    """Browse all opportunities"""
    all_opportunities = Opportunity.query.filter_by(status='open').order_by(
        Opportunity.date
    ).all()
    return render_template('opportunities.html', opportunities=all_opportunities)


@app.route('/opportunity/<int:opp_id>', methods=['GET', 'POST'])
def opportunity_detail(opp_id):
    """View opportunity details and apply"""
    opportunity = Opportunity.query.get_or_404(opp_id)
    form = ApplicationForm()
    
    # Check if user has already applied
    has_applied = False
    application_status = None
    
    if current_user.is_authenticated and current_user.role == 'volunteer':
        existing_app = Application.query.filter_by(
            user_id=current_user.id,
            opportunity_id=opp_id
        ).first()
        
        if existing_app:
            has_applied = True
            application_status = existing_app.status
    
    return render_template(
        'opportunity_detail.html',
        opportunity=opportunity,
        form=form,
        has_applied=has_applied,
        application_status=application_status
    )


# ========== VOLUNTEER ROUTES ==========

@app.route('/volunteer/dashboard')
@login_required
def volunteer_dashboard():
    """Volunteer dashboard"""
    if current_user.role != 'volunteer':
        flash('Access denied. Volunteers only.', 'danger')
        return redirect(url_for('index'))
    
    # Get all applications by this volunteer
    applications = Application.query.filter_by(user_id=current_user.id).order_by(
        Application.applied_at.desc()
    ).all()
    
    # Calculate statistics
    accepted_count = sum(1 for app in applications if app.status == 'accepted')
    pending_count = sum(1 for app in applications if app.status == 'pending')
    
    return render_template(
        'volunteer_dashboard.html',
        applications=applications,
        accepted_count=accepted_count,
        pending_count=pending_count
    )


@app.route('/apply/<int:opp_id>', methods=['POST'])
@login_required
def apply(opp_id):
    """Submit application for an opportunity"""
    if current_user.role != 'volunteer':
        flash('Only volunteers can apply to opportunities.', 'danger')
        return redirect(url_for('opportunity_detail', opp_id=opp_id))
    
    opportunity = Opportunity.query.get_or_404(opp_id)
    
    # Check if already applied
    existing_app = Application.query.filter_by(
        user_id=current_user.id,
        opportunity_id=opp_id
    ).first()
    
    if existing_app:
        flash('You have already applied to this opportunity.', 'warning')
        return redirect(url_for('opportunity_detail', opp_id=opp_id))
    
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            user_id=current_user.id,
            opportunity_id=opp_id,
            message=form.message.data,
            status='pending'
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('volunteer_dashboard'))
    
    flash('Error submitting application. Please try again.', 'danger')
    return redirect(url_for('opportunity_detail', opp_id=opp_id))


# ========== ORGANIZATION ROUTES ==========

@app.route('/organization/dashboard')
@login_required
def org_dashboard():
    """Organization dashboard"""
    if current_user.role != 'organization':
        flash('Access denied. Organizations only.', 'danger')
        return redirect(url_for('index'))
    
    # Get all opportunities posted by this organization
    opportunities = Opportunity.query.filter_by(org_id=current_user.id).order_by(
        Opportunity.created_at.desc()
    ).all()
    
    # Calculate statistics
    total_applications = sum(len(opp.applications) for opp in opportunities)
    pending_applications = sum(
        len([app for app in opp.applications if app.status == 'pending'])
        for opp in opportunities
    )
    
    return render_template(
        'org_dashboard.html',
        opportunities=opportunities,
        total_applications=total_applications,
        pending_applications=pending_applications
    )


@app.route('/opportunity/create', methods=['GET', 'POST'])
@login_required
def create_opportunity():
    """Create a new volunteer opportunity"""
    if current_user.role != 'organization':
        flash('Only organizations can post opportunities.', 'danger')
        return redirect(url_for('index'))
    
    form = OpportunityForm()
    if form.validate_on_submit():
        opportunity = Opportunity(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            date=form.date.data,
            duration=form.duration.data,
            skills_required=form.skills_required.data,
            spots_available=form.spots_available.data,
            org_id=current_user.id,
            status='open'
        )
        
        db.session.add(opportunity)
        db.session.commit()
        
        flash('Opportunity posted successfully!', 'success')
        return redirect(url_for('org_dashboard'))
    
    return render_template('create_opportunity.html', form=form)


@app.route('/application/<int:app_id>/update', methods=['POST'])
@login_required
def update_application(app_id):
    """Accept or reject an application"""
    if current_user.role != 'organization':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    application = Application.query.get_or_404(app_id)
    
    # Verify the organization owns this opportunity
    if application.opportunity.org_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('org_dashboard'))
    
    action = request.form.get('action')
    
    if action == 'accept':
        application.status = 'accepted'
        flash('Application accepted!', 'success')
    elif action == 'reject':
        application.status = 'rejected'
        flash('Application rejected.', 'info')
    
    db.session.commit()
    return redirect(url_for('org_dashboard'))


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('base.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """500 error handler"""
    db.session.rollback()
    return render_template('base.html'), 500


# ========== DATABASE INITIALIZATION ==========

@app.cli.command()
def initdb():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


@app.cli.command()
def seeddb():
    """Seed the database with sample data."""
    # Create sample organization
    org = User(
        name='Community Food Bank',
        email='contact@foodbank.org',
        role='organization',
        phone='555-0100',
        location='New York, NY',
        bio='Dedicated to fighting hunger in our community.'
    )
    org.set_password('password123')
    db.session.add(org)
    db.session.commit()
    
    # Create sample volunteer
    volunteer = User(
        name='John Doe',
        email='john@example.com',
        role='volunteer',
        phone='555-0200',
        location='New York, NY'
    )
    volunteer.set_password('password123')
    db.session.add(volunteer)
    db.session.commit()
    
    # Create sample opportunity
    from datetime import date, timedelta
    opportunity = Opportunity(
        title='Food Distribution Volunteer',
        description='Help us distribute food to families in need. We need energetic volunteers to help pack and distribute food boxes.',
        location='123 Main St, New York, NY',
        date=date.today() + timedelta(days=7),
        duration='4 hours',
        skills_required='Physical fitness, Communication',
        spots_available=10,
        org_id=org.id,
        status='open'
    )
    db.session.add(opportunity)
    db.session.commit()
    
    print('Database seeded with sample data!')
    print('Organization: contact@foodbank.org / password123')
    print('Volunteer: john@example.com / password123')


# ========== RUN APPLICATION ==========

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)