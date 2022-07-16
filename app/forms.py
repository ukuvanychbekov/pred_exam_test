from flask_wtf import FlaskForm
import wtforms as wf
from wtforms import validators



class UserForm(FlaskForm):
    username = wf.StringField('Пользователь', validators=[wf.validators.DataRequired()])
    password = wf.PasswordField('Пароль', validators=[wf.validators.DataRequired(), validators.Length(min=4, max=10)])
    submit = wf.SubmitField('OK')


class CustomerForm(FlaskForm):
    name = wf.StringField('ФИО', validators=[wf.validators.DataRequired()])
    phone_number = wf.StringField('Номер телефона', validators=[wf.validators.DataRequired()])
    item = wf.StringField('Товар', validators=[wf.validators.DataRequired()])
    quantity = wf.IntegerField('Количество', validators=[wf.validators.DataRequired()])
    price = wf.IntegerField('Цена', validators=[wf.validators.DataRequired()])
    submit = wf.SubmitField('OK')

