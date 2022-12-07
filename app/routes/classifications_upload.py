import os

import redis
from flask import render_template, request, flash, redirect
from rq import Connection, Queue
from rq.job import Job
from werkzeug.utils import secure_filename

from app import app
from app.forms.classification_form_with_upload import ClassificationFormWithUpload
# from app.utils.filename_validation import validate_filename
from ml.classification_utils import classify_image
from config import Configuration

from app.utils import filename_validation as fv

config = Configuration()
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER


@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """API for selecting a model and uploading an image from the
    user computer and running classification job. Returns the output scores from the
    model."""
    form = ClassificationFormWithUpload()
    if form.validate_on_submit():
        file = form.image.data
        image_id = fv.validate_filename(file.filename)

        if image_id == '':
            flash('No selected file')
            return redirect(request.url)
        if file and fv.allowed_file(image_id):
            filename = secure_filename(image_id)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            model_id = form.model.data

            redis_url = Configuration.REDIS_URL
            redis_conn = redis.from_url(redis_url)
            with Connection(redis_conn):
                q = Queue(name=Configuration.QUEUE)
                job = Job.create(classify_image, kwargs={
                    "model_id": model_id,
                    "img_id": image_id
                })
                task = q.enqueue_job(job)

            return render_template("classification_output_queue.html", image_id=image_id, image_folder="uploads",
                                   caller_page="classifications_upload", jobID=task.get_id())

    return render_template('classification_upload.html', form=form)
