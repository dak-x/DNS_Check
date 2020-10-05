from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import dns.rdatatype


class DNSForm(FlaskForm):
    myChoices = [
        [dns.rdatatype.A, "A"],
        [dns.rdatatype.AAAA, "AAAA"],
        [dns.rdatatype.CNAME, "CNAME"],
        [dns.rdatatype.MX, "MX"],
        [dns.rdatatype.NS, "NS"],
        [dns.rdatatype.PTR, "PTR"],
        [dns.rdatatype.SRV, "SRV"],
        [dns.rdatatype.SOA, "SOA"],
        [dns.rdatatype.TXT, "TXT"],
        [dns.rdatatype.CAA, "CAA"]
    ]
    domain_name = StringField('Domain name', validators=[DataRequired()])
    type = SelectField("Record Type", choices=myChoices,
                       validators=[DataRequired()])
    default_dns = StringField('Default DNS', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RevForm(FlaskForm):
    domain_name = StringField('Domain name', validators=[DataRequired()])
    submit = SubmitField('Submit')
