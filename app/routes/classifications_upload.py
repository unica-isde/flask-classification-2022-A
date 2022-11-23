import os

import redis
from flask import render_template, request, flash, redirect
from rq import Connection, Queue
from rq.job import Job
from werkzeug.utils import secure_filename

from app import app
from app.forms.classification_form_with_upload import ClassificationFormWithUpload
from ml.classification_utils import classify_image
from config import Configuration

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
    The functions below are necessary to transform the
    upload image filename to a valid one.
    When an image filename containing brackets and spaces is uploaded,
    it is saved in the "uploads" folder without round brackets and 
    with underscores replacing the spaces.
"""
def rm_string_spaces(string):
    """
    It replaces every space in the string with an underscore.

    """
    list_splits = string.split(" ")
    new_string = ""
    for i in range(len(list_splits)):
        """if list_splits[i] == '(' or list_splits[i] == ')':
            continue"""
        if i == len(list_splits) - 1:
            new_string += list_splits[i]
        else:
            new_string += list_splits[i] + '_'
    return new_string

def rm_string_round_brackets(string):
    """l_string = list(string)
    list_occurrences = [l_string.count('(')
    for i in range(occurrence):
        l_string.remove('(')"""
    new_string = ""
    list_splits = (new_string.join(string.split('('))).split(')')
    return new_string.join(list_splits)

def validate_filename(string):
    tmp_string = rm_string_spaces(string)
    return rm_string_round_brackets(tmp_string)


config = Configuration()
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """API for selecting a model and an image and running a
    classification job. Returns the output scores from the
    model."""
    form = ClassificationFormWithUpload()
    if form.validate_on_submit():
        file = form.image.data #that's still a type "FileStorage", not an image ID
        image_id = validate_filename(file.filename)

        if image_id == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(image_id):
            filename = secure_filename(image_id)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            model_id = form.model.data
            clf_output = classify_image(model_id=model_id,  img_id=image_id)
            result = dict(data=clf_output)
            return render_template('classification_output.html', results=result, image_id=image_id,
                                   caller_page='classifications_upload', image_folder='uploads')

    return render_template('classification_upload.html', form=form)
