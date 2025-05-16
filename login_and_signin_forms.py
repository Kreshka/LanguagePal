from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    mail = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    pre_password = PasswordField('Поддтверждение пароля', validators=[DataRequired(), EqualTo("password")])
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    patr = StringField("Отчество", validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class SigninForm(FlaskForm):
    mail = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')