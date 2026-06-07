from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class MetadataForm(Form):
    access_decision = StringField('Recommended access level', [validators.DataRequired()])
    cultural_notes = StringField('Cultural notes')
    access_conditions = StringField('Access conditions')
    public_description = StringField('Approved public description')
