from flask import render_template
from app import app
from app.forms.histogram_form import HistogramForm
from config import Configuration
import os
from skimage import io
import matplotlib.pyplot as plt
import base64
import io as IO

config = Configuration()


@app.route('/histograms', methods=['GET', 'POST'])
def histograms():
    """
    API for creating the histogram of a selected image:
    If the user clicks on the submit button the function will calculate the histogram of the image and pass it
    to the render_template function that will show the histogram_output html page.
    Otherwise, the select_histogram html page.
    """
    form = HistogramForm()
    if form.validate_on_submit():
        image_id = form.image.data

        # This code loads the selected image, calculates the histogram and passes the new image to the html file.
        image_path = os.path.join(config.image_folder_path, image_id)
        image = io.imread(image_path)
        fig = plt.figure()
        ax1 = fig.add_subplot(121)
        _ = plt.hist(image.ravel(), bins=256, color='orange', )
        _ = plt.hist(image[:, :, 0].ravel(), bins=256, color='red', alpha=0.5)
        _ = plt.hist(image[:, :, 1].ravel(), bins=256, color='Green', alpha=0.5)
        _ = plt.hist(image[:, :, 2].ravel(), bins=256, color='Blue', alpha=0.5)
        _ = plt.xlabel('Intensity Value')
        _ = plt.ylabel('Count')
        _ = plt.legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])

        s = IO.BytesIO()
        plt.savefig(s, format='JPEG')
        # The base64 library allows us to create the histogram image in memory without actually saving it to a file.
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        img_data = f"data:image/jpeg;base64,{s}"

        return render_template('histogram_output.html', image_id=image_id, hist=img_data)
    return render_template('histogram_select.html', form=form)

