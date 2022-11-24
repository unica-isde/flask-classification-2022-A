from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

from config import Configuration

conf = Configuration()


class ClassificationFormWithUpload(FlaskForm):
    model = SelectField('model', choices=conf.models, validators=[DataRequired()])
    image = FileField('image', validators=[FileRequired()])
    submit = SubmitField('Submit')
