from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

from app.utils.list_images import list_images


class ImageTransformationForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    color = IntegerField('color', validators=[DataRequired()], default=0)
    brightness = IntegerField('brightness', validators=[DataRequired()], default=0)
    contrast = IntegerField('contrast', validators=[DataRequired()], default=0)
    sharpness = IntegerField('sharpness', validators=[DataRequired()], default=0)
    submit = SubmitField('Submit')
