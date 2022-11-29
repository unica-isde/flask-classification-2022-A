# Add the “download results” button to the web interface.
# The button should allow the user to download the results (classification scores) as a JSON file
# and as a png file showing the top 5 scores in a plot (bar chart).
# All the functionalities must be preserved, this is just a new feature.
import os

import redis
from rq import Connection, Queue
from app import app
from config import Configuration
from matplotlib.pyplot import Figure
import time
from flask import send_from_directory, after_this_request

config = Configuration()

# path where the temporary file is saved
path = "/Users/maxrudat/PycharmProjects/flask-classification-2022-A/app/routes/"


@app.route('/classifications/<string:job_id>/result_plot', methods=['GET'])
def get_plot_for_download(job_id):
    """
    Connects to redis, gets the results and saves them as a .png file.
    """
    redis_url = config.REDIS_URL
    redis_conn = redis.from_url(redis_url)
    with Connection(redis_conn):
        q = Queue(name=Configuration.QUEUE)
        task = q.fetch_job(job_id)

    response = {
        'task_status': task.get_status(),
        'data': task.result,
    }

    data = dict(response["data"])

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.bar(list(data.keys()), list(data.values()), align='center')

    filename = f"temp_figure_{job_id}.png"

    fig.savefig(path + filename)

    @after_this_request
    def delete_img(response):
        """
        This removes the image file after the request has been sent.
        Prohibits taking space from (server) hard-drive.
        """
        os.remove(path + filename)
        return response

    return send_from_directory(path, filename, as_attachment=True)
