from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

from app.utils.list_images import list_images


class ImageTransformationForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    color = FloatField('color', default=1)
    brightness = FloatField('brightness', default=0)
    contrast = FloatField('contrast', default=0)
    sharpness = FloatField('sharpness', default=0)
    submit = SubmitField('Submit')
