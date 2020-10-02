from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class DNSForm(FlaskForm):
    myChoices = [["A", "A"], ["AAAA", "AAAA"], [
        "MX", "MX"], ["CA", "CA"], ["TXT", "TXT"]]
    domain_name = StringField('Domain name', validators=[DataRequired()])
    type = SelectField("Record Type", choices=myChoices,
                       validators=[DataRequired()])
    default_dns = StringField('Default DNS', validators=[DataRequired()])
    submit = SubmitField('Submit')
