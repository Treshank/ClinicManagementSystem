from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField,\
    SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


class SearchForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Search')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[Email(), DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    phone_no = StringField('Phone Number', validators=[
        Length(min=10, max=10, message="Invalid Phone number"), DataRequired()])
    submit = SubmitField('Add Patient')


class UserRegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[Email(), DataRequired()])
    first_name = StringField('First_Name', validators=[DataRequired()])
    last_name = StringField('Last_Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    phone_no = StringField('Phone Number', validators=[
        Length(min=10, max=10, message="Invalid Phone number"), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register User')

    # def validate_username(self, username):
     #   user = User.query.filter_by(email=username.data).first()
     #   if user is not None:
      #      raise ValidationError('Please use a different username')

    # def validate_email(self, email):
      #   email = User.query.filter_by(email=email.data).first()
     #    if email is not None:
     #       raise ValidationError('Please use a different username')


class DoctorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[Email(), DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    phone_no = StringField('Phone Number', validators=[
        Length(min=10, max=10, message="Invalid Phone number"), DataRequired()])
    dept = SelectField('Department', choices=[('0', 'General Physician'), ('1', 'ENT'), ('2', 'Optician'),
                                              ('3', 'Radiology')])
    submit = SubmitField('Add New Doctor')


class EmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    email = EmailField('E-Mail', validators=[Email()])
    user_id_ref = StringField('Reference id')
    phone_no = StringField('Phone Number', validators=[
        Length(min=10, max=10, message="Invalid Phone number"), DataRequired()])
    dept = SelectField('Work', choices=[('4', 'Front Desk'), ('6', 'Management'), ('5', 'Nurse'),
                                        ('7', 'Support Staff')])
    submit = SubmitField('Add New Employee')


class AppointmentForm(FlaskForm):
    p_id = StringField('Patient ID', validators=[DataRequired()])
    submit = SubmitField('Book')


class Billing(FlaskForm):
    app_id = StringField('Appointment ID', validators=[DataRequired()])
    pat_id = StringField('Patient ID', validators=[DataRequired()])
    doc_id = StringField('Doctor ID', validators=[DataRequired()])
    consultation = BooleanField('Consultation')
    health_check = BooleanField('Heath Check')
    test_set1 = BooleanField('Clinical test set 1')
    test_set2 = BooleanField('Clinical test set 2')
    submit = SubmitField('Bill')
