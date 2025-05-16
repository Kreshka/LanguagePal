from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField


class GForm(FlaskForm):
    r1 = RadioField()
    r2 = RadioField()
    r3 = RadioField()
    r4 = RadioField()
    submit = SubmitField('Ответить')
