"""
Run script for Socio+ application
This script initializes the database and starts the Flask server
"""

from app import app, db

def init_database():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("✓ Database initialized successfully!")
        print("✓ Tables created: users, opportunities, applications")

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Socio+ Application")
    print("=" * 50)
    
    # Initialize database
    init_database()
    
    print("\n" + "=" * 50)
    print("Server is running!")
    print("Open your browser and visit: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 50 + "\n")
    
    # Run the Flask development server
    app.run(debug=True, host='127.0.0.1', port=5000)