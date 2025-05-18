from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import DataRequired


class GForm(FlaskForm):
    def generate_fields(num_t: int):
        fields = {}
        for i in range(num_t):
            fields[f'r{i}_1'] = RadioField()
            fields[f'r{i}_2'] = RadioField()
            fields[f'r{i}_3'] = RadioField()
            fields[f'r{i}_4'] = RadioField()
            fields[f'submit'] = SubmitField('Ответить')
            return fields


def cdf_test(questions):
    class DynamicForm(FlaskForm):
        pass

    for question in questions:
        setattr(DynamicForm, question['id'],
                RadioField(question['text'],
                           choices=question['choices'], validators=[DataRequired()]))

    setattr(DynamicForm, 'submit', SubmitField('Проверить тест'))

    return DynamicForm


def cdf_write(questions):
    class DynamicForm(FlaskForm):
        pass

    for question in questions:
        setattr(DynamicForm, question['id'],
                StringField(question['text'], validators=[DataRequired()]))

    setattr(DynamicForm, 'submit', SubmitField('Проверить ответы'))

    return DynamicForm


def cdf_list(questions):
    class DynamicForm(FlaskForm):
        pass

    for question in questions:
        setattr(DynamicForm, question['id'],
                StringField(question['text']))

    setattr(DynamicForm, 'submit', SubmitField('Проверить ответы'))

    return DynamicForm