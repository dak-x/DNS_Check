from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import dns.rdatatype


class DNSForm(FlaskForm):
    myChoices = [
        ["ANY","ANY"],
        ["A", "A"],
        ["AAAA", "AAAA"],
        ["CNAME", "CNAME"],
        ["MX", "MX"],
        ["NS", "NS"],
        ["PTR", "PTR"],
        ["SRV", "SRV"],
        ["SOA", "SOA"],
        ["TXT", "TXT"],
        ["CAA", "CAA"]
    ]
    domain_name = StringField('Domain name', validators=[DataRequired()])
    type = SelectField("Record Type", choices=myChoices,
                       validators=[DataRequired()])
    default_dns = StringField('Default DNS', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RevForm(FlaskForm):
    domain_name = StringField('Domain name', validators=[DataRequired()])
    submit = SubmitField('Submit')
