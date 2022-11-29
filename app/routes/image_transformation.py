import base64
import io
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
from ml.image_transformation_utils import color_transform, brightness_transform, contrast_transform, sharpness_transform
from ml.classification_utils import fetch_image
from config import Configuration

conf = Configuration()


@app.route('/image_transformation', methods=['GET', 'POST'])
def image_transformation():
    form = ImageTransformationForm()

    if form.validate_on_submit():
        image_id = form.image.data

        img_t = fetch_image(image_id)

        color = form.color.data
        brightness = form.brightness.data
        contrast = form.contrast.data
        sharpness = form.sharpness.data

        img_t = color_transform(img_t, color)
        img_t = brightness_transform(img_t, brightness)
        img_t = contrast_transform(img_t, contrast)
        img_t = sharpness_transform(img_t, sharpness)

        data = io.BytesIO()
        img_t.save(data, "PNG")
        encoded_img = base64.b64encode(data.getvalue())
        decoded_img = encoded_img.decode('utf-8')
        img_data = f"data:image/jpeg;base64,{decoded_img}"

        # image_name = image_save(img, image_id)

        return render_template('image_transformation_output.html', image_id=image_id, img_data=img_data)
    return render_template('image_transformation_select.html', form=form)
