from app import app, db
# app.py
app.secret_key = 'your_secret_key_here'  # Replace with a secure key


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
