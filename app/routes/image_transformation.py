import base64
import os

from PIL import ImageEnhance

# enhancer = ImageEnhance.Color()
# enhancer = ImageEnhance.Brightness()
# enhancer = ImageEnhance.Contrast()
# enhancer = ImageEnhance.Sharpness()

# factor = 5 / 4.0
# enhancer.enhance(factor).show(f"Sharpness{factor:f}")

import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.image_transformation_form import ImageTransformationForm
from ml.image_transformation_utils import color_transform, image_save
from ml.classification_utils import classify_image
from config import Configuration

conf = Configuration()


@app.route('/image_transformation', methods=['GET', 'POST'])
def image_transformation():
    form = ImageTransformationForm()

    if form.validate_on_submit():
        image_id = form.image.data
        color = form.color.data
        brightness = form.brightness.data
        contrast = form.contrast.data
        sharpness = form.sharpness.data
        image_output = color_transform(image_id, color)

        image_name = image_save(image_output, image_id)

        return render_template('image_transformation_output.html', image_id=image_name)
    return render_template('image_transformation_select.html', form=form)
