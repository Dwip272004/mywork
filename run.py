from app import app, db
import os

# Set the secret key for session management
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    # Get the PORT environment variable or use 5000 as a default
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port, debug=False)  # Bind to all interfaces
