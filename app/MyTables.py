from flask_table import Table, Col, LinkCol


class PatientTable(Table):
    id = Col('id')
    first_name = Col('First Name')
    last_name = Col('Last Name')
    phone_no = Col('Phone Number')
    email = Col('Email')
    address = Col('Address')
    occupation = Col('Occupation')
    added_by_user = Col('Created By')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id', table="patient"))
    Table.border = True


class DoctorTable(Table):
    id = Col('id')
    first_name = Col('First Name')
    last_name = Col('Last Name')
    phone_no = Col('Phone Number')
    email = Col('Email')
    address = Col('Address')
    specialization = Col('Specialization')
    Table.border = True
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id', table="doctor"))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))
