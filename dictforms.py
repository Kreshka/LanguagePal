from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import DataRequired


def cdf_test(questions):
    class DynamicForm(FlaskForm):
        pass

    for question in questions:
        setattr(DynamicForm, question['id'],
                RadioField(question['text'],
                           choices=question['choices']))

    setattr(DynamicForm, 'submit', SubmitField('Проверить тест'))

    return DynamicForm