from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateTimeField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class HomeworkForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    description = TextAreaField('Homework Description', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    deadline = DateTimeField('Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])  # Match format
    file = FileField('Upload File', validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg', 'gif'], 'Images and PDFs only!')])
    submit = SubmitField('Submit Homework')

class ContactAdminForm(FlaskForm):
    message = TextAreaField('Message to Admin', validators=[DataRequired()])
    submit = SubmitField('Contact Admin')

# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ContactAdminForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    message = TextAreaField('Message to Admin', validators=[DataRequired()])
    submit = SubmitField('Contact Admin')
