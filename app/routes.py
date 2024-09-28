import os
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, session
from app import app, db
from app.models import ContactMessage, Homework
from app.forms import HomeworkForm, ContactAdminForm, AdminLoginForm
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_homework_ajax', methods=['GET', 'POST'])
def submit_homework():
    form = HomeworkForm()

    if form.validate_on_submit():
        app.logger.info(f"Form data: {request.form}")  # Log incoming form data

        try:
            filename = None
            if form.file.data:
                file = form.file.data
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    app.logger.info(f"File saved to {file_path}")
                else:
                    return jsonify({'success': False, 'message': 'Invalid file type'})

            homework = Homework(
                name=form.name.data,
                description=form.description.data,
                cost=form.cost.data,
                deadline=form.deadline.data,
                file_path=filename
            )
            db.session.add(homework)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Homework submitted successfully'})
        except Exception as e:
            app.logger.error(f"Error in file upload: {str(e)}")
            return jsonify({'success': False, 'message': 'An error occurred while uploading the file'})
    
    return render_template('submit_homework.html', form=form)

@app.route('/works')
def work_list():
    works = Homework.query.order_by(Homework.timestamp.desc()).all()
    return render_template('work_list.html', works=works)

@app.route('/contact_admin/<int:work_id>', methods=['GET', 'POST'])
def contact_admin(work_id):
    work = Homework.query.get_or_404(work_id)
    form = ContactAdminForm()
    
    if form.validate_on_submit():
        try:
            # Save the contact message to the database
            message = ContactMessage(
                name=form.name.data,  # Ensure this field exists in your form
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            
            flash(f'Message sent to admin regarding work: {work.name}', 'success')
            return redirect(url_for('work_list'))
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            flash(f'An error occurred while sending the message: {str(e)}', 'danger')
    
    return render_template('contact_admin.html', form=form, work=work)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin123':  # Replace with your actual logic
            session['admin_logged_in'] = True
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard after login
        else:
            flash('Invalid username or password', 'danger')
    return render_template('admin_login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        flash('You must be logged in as an admin to access this page', 'danger')
        return redirect(url_for('admin_login'))

    # Fetch all homework submissions and messages
    works = Homework.query.order_by(Homework.timestamp.desc()).all()
    messages = ContactMessage.query.order_by(ContactMessage.timestamp.desc()).all()

    return render_template('admin_dashboard.html', works=works, messages=messages)

@app.route('/admin/delete/<int:work_id>', methods=['POST'])
def delete_work(work_id):
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        flash('You must be logged in as an admin to perform this action', 'danger')
        return redirect(url_for('admin_login'))
    
    try:
        # Fetch the work to be deleted
        work = Homework.query.get_or_404(work_id)
        if work.file_path:
            # Delete the file if it exists
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], work.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete the homework entry
        db.session.delete(work)
        db.session.commit()
        flash('Homework entry deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting work: {str(e)}")
        flash('An error occurred while trying to delete the entry', 'danger')

    return redirect(url_for('admin_dashboard'))
