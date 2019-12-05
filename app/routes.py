from functools import wraps
from app import app, db
from flask import render_template, flash, redirect, url_for, request, session, logging
from app.forms import LoginForm, PatientForm, UserRegForm, DoctorForm, SearchForm, AppointmentForm, Billing
from passlib.hash import sha256_crypt
from app.MyTables import PatientTable, DoctorTable


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


# this is the login page
# methods args tells flask that the view fn accepts GET and POST req overriding default (only GET)
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = ''
    # here GET is false and POST is true.ie. only if the submit button is pressed the if stmts are checked.
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        c = db.connection.cursor()
        data = c.execute('SELECT * FROM user WHERE username =%s', [username])
        data = c.fetchone()[2]
        if sha256_crypt.verify(password, data):
            session['logged_in'] = True
            session['username'] = request.form['username']
            data = c.execute('SELECT id from user where username=%s', [username])
            data = c.fetchone()[0]
            session['user_id'] = data
            flash('You are now logged in')
            return redirect(url_for('home'))
        else:
            msg = "Invalid username or password "
        c.close()
    return render_template('login.html', title='Sign In', form=form, msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegForm()
    msg = ''
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        password = sha256_crypt.encrypt((str(form.password.data)))
        c = db.connection.cursor()

        x = c.execute("SELECT * FROM user WHERE username = %s",
                      [username])
        if int(x) > 0:
            flash("That username is already taken, please choose another")
            return redirect(url_for('register'))
        else:
            c.execute("INSERT INTO user (username, password) values(%s, %s);", (username, password))
            db.connection.insert_id()
            id = c.lastrowid
            c.execute("INSERT INTO employee(email, first_name, last_name, address, phone_no, user_id_ref) "
                      "VALUES (%s, %s, %s, %s, %s, %s);",
                      (email, form.first_name.data, form.last_name.data, form.address.data,
                       form.phone_no.data, id))
            flash("user registered!!")
            db.connection.commit()
            c.close()
            return redirect(url_for('home'))
    return render_template('register.html', title='Register User', form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    msg = ''
    posts = [
        {
            'author': {'username': 'Admin'},
            'body': 'The new database version fixing minor bugs'
        },
        {
            'author': {'username': 'Manager'},
            'body': 'Dr. Prasad has applied for a leave for 5days. No appointments to be booked under his name.\n'
                    'All existing appointments to be given over to Dr. Ramesh '
        }]
    return render_template('home.html', title='Home', msg=msg, posts=posts)


@app.route('/patient_form', methods=['GET', 'POST'])
@login_required
def patient_form():
    form = PatientForm()
    if form.validate_on_submit():
        c = db.connection.cursor()
        data = c.execute("INSERT INTO patient (first_name, last_name, email, address, phone_no, occuptation, added_by) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                         (form.first_name.data, form.last_name.data, form.email.data, form.address.data,
                          form.phone_no.data, form.occupation.data, int(session['user_id'])))
        db.connection.commit()
        #db.connection.close()
        flash("Patient created with name {}".format(form.first_name.data))
        return redirect(url_for('home'))
    return render_template('patient_form.html', title='New Patient', form=form)


@app.route('/view_patient', methods=['GET', 'POST'])
@login_required
def view_patient():
    form = SearchForm()
    data = ''
    c = db.connection.cursor()
    if form.validate_on_submit() or request.method == 'POST':
        search = form.search.data
        if search.isnumeric():
            data = c.execute("call searchp({},'');".format(int(search)))
        else:
            data = c.execute("call searchp(1,'{}');".format(search))
        data = c.fetchall()
    else:
        data = c.execute("select * from patient;")
        data = c.fetchall()
    c.close()
    return render_template('patient_table.html', data=data, form=form)


@app.route('/edit_patient_form/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient_form(id):
    c = db.connection.cursor()
    data = c.execute("select * from patient where id={}".format(id))
    data = c.fetchone()
    form = PatientForm(formdata=request.form, obj=data)
    if data:
        if form.validate_on_submit():
            c.execute("update patient set first_name=%s, last_name=%s, email=%s, address=%s, phone_no=%s,"
                      " occuptation=%s where id={}".format(int(id)), (form.first_name.data, form.last_name.data,
                                                                      form.email.data, form.address.data,
                                                                      form.phone_no.data, form.occupation.data))
            db.connection.commit()
            c.close()
            flash("edit successful for patient {}".format(id))
            return redirect(url_for('view_patient'))
    return render_template('edit_patient_form.html', title="edit patient", form=form, data=data)


@app.route('/delete_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_patient(id):
    c = db.connection.cursor()
    data = c.execute("delete from patient where id={}".format(id))
    flash("Patient id={} deleted".format(id))
    db.connection.commit()
    c.close()
    return redirect(url_for('view_doctor'))


@app.route('/doctor_form', methods=['GET', 'POST'])
@login_required
def doctor_form():
    form = DoctorForm()
    if request.method == 'POST':
        c = db.connection.cursor()
        data = c.execute("INSERT INTO doctor (first_name, last_name, email, address, phone_no, specialization, "
                         "department) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                         (form.first_name.data, form.last_name.data, form.email.data, form.address.data,
                          form.phone_no.data, form.specialization.data, form.dept.data))
        db.connection.commit()
        flash("Doctor created with name {}", format(form.first_name.data,))
        c.close()
        return redirect(url_for('home'))
    return render_template('doctor_form.html', title='New Doctor', form=form)


@app.route('/view_doctor', methods=['GET', 'POST'])
@login_required
def view_doctor():
    form = SearchForm()
    c = db.connection.cursor()
    if form.validate_on_submit() or request.method == 'POST':
        search = form.search.data
        if search.isnumeric():
            data = c.execute("call searchd({},'');".format(int(search)))
        else:
            data = c.execute("call searchd(1,'{}');".format(search))
        data = c.fetchall()
    else:
        data = c.execute("select * from doctor")
        data = c.fetchall()
    return render_template('doctor_table.html', data=data, form=form)


@app.route('/edit_doctor_form/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_doctor_form(id):
    c = db.connection.cursor()
    data = c.execute("select first_name, last_name, address, email, specialization, phone_no, department from doctor "
                     "where id={}".format(id))
    data = c.fetchone()
    form = DoctorForm(obj=data)
    if data:
        if form.validate_on_submit():
            c.execute("update doctor set first_name=%s, last_name=%s, email=%s, address=%s, phone_no=%s,"
                      "specialization=%s, department={} where id={}".format(int(form.dept.data), int(id)),
                      ([form.first_name.data], [form.last_name.data], [form.email.data], [form.address.data],
                       [form.phone_no.data], [form.specialization.data]))
            db.connection.commit()
            c.close()
            flash("edit successful for doctor {}".format(id))
            return redirect(url_for('view_doctor'))
    return render_template('edit_doctor_form.html', title="edit doctor", form=form, data=data)


@app.route('/delete_doctor/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_doctor(id):
    c = db.connection.cursor()
    data = c.execute("delete from doctor where id={}".format(id))
    data = c.fetchall
    flash("Doctor id={} deleted".format(id))
    db.connection.commit()
    c.close()
    return redirect(url_for('view_doctor'))


@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    return render_template('appointment.html', title='Appointments')


@app.route('/appointment1/<int:d>', methods=['GET', 'POST'])
@app.route('/appointment1/<int:d>/<int:d_id>/<int:t>', methods=['GET', 'POST'])
@app.route('/appointment1/<int:d_id>/<int:t>', methods=['GET', 'POST'])
@login_required
def appointment1(d='', d_id='', t=''):
    c = db.connection.cursor()
    data = c.execute("select * from doctor;")
    data = c.fetchall()
    dataa = c.execute("select doc_id,time_slot,pat_id from appointment where date={}".format(int(d)))
    dataa = c.fetchall()
    form = AppointmentForm()
    if form.validate_on_submit() or (request.method == 'POST'):
        c.execute("select * from patient where id={};".format(form.p_id.data))
        pdata = c.fetchall()
        if d_id == '' or t == '':
            flash('Please click the appropriate column')
            c.close()
            return redirect(url_for('appointment1', d=d))
        elif form.p_id.data == '' or len(pdata)<=0:
            flash('Please enter a valid patient id')
            c.close()
            return redirect(url_for('appointment1', d=d, d_id=d_id, t=t))
        else:
            data = c.execute("INSERT INTO appointment(doc_id, pat_id, date, time_slot) values({}, {}, {}, {})".format(
                              int(d_id), int(form.p_id.data), int(d), int(t)))
            db.connection.commit()
            c.close()
            flash('Appointment booked for {}'.format(form.p_id.data))
            return redirect(url_for('home'))
    return render_template('appointment1.html', title='Appointments1', data=data, dataa=dataa, form=form, d=d)


@app.route('/billing', methods=['GET', 'POST'])
@login_required
def billing():
    form = Billing()
    if request.method == 'POST' or form.validate_on_submit():
        c = db.connection.cursor()
        data = c.execute("INSERT INTO bill(app_id, doc_id, pat_id, consultation, health_check, test_set1, test_set2) "
                         "values({}, {}, {}, {}, {}, {}, {});".format(int(form.app_id.data), int(form.doc_id.data),
                                                                      int(form.pat_id.data),
                                                                      int(form.consultation.data),
                                                                      int(form.health_check.data),
                                                                      int(form.test_set1.data),
                                                                      int(form.test_set2.data)))
        db.connection.insert_id()
        b_id = c.lastrowid
        c.execute("call calc_total({})".format(b_id))
        c.close()
        db.connection.commit()
        return redirect(url_for('bill', id=b_id))
    return render_template('billing.html', form=form, title="Billing")


@app.route('/bill/<int:id>', methods=['GET', 'POST'])
@login_required
def bill(id):
    c = db.connection.cursor()
    data = c.execute("select b.bill_id, b.app_id, b.doc_id, d.first_name, b.pat_id, p.first_name, b.total_cost "
                     "from bill b, doctor d, patient p "
                     "where b.doc_id=d.id and b.pat_id=p.id and b.bill_id={};".format(id))
    data = c.fetchone()
    c.close()
    return render_template('bill.html', data=data, title='Bill')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('login'))


