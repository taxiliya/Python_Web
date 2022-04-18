from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired,FileAllowed
from wtforms.validators import DataRequired, Length
from wtforms import Form, FileField,StringField, PasswordField


class BaseLogin(FlaskForm):
    name = StringField('name',
                       validators=[DataRequired(message='用户名不能为空'),
                                   Length(6, 16, message='长度6~16位')],
                       render_kw={'placeholder': '输入用户名'}
                       )
    password = PasswordField('password',
                             validators=[DataRequired(message='密码不能为空'),
                                         Length(6, 16, message='长度6~16位')],
                             render_kw={'placeholder': '输入密码'}
                             )


class UploadForm(Form):
    file = FileField(validators=[FileRequired(),
                                 FileAllowed(['jpg','png','gif'])
                                 ]
                     )
