# Add the “download results” button to the web interface.
# The button should allow the user to download the results (classification scores) as a JSON file
# and as a png file showing the top 5 scores in a plot (bar chart).
# All the functionalities must be preserved, this is just a new feature.

import json
import redis
from rq import Connection, Queue

from app import app
from config import Configuration

from flask import Response

config = Configuration()


@app.route('/classifications/<string:job_id>/results', methods=['GET'])
def get_results_json_for_download(job_id):
    """Returns the status and the result of the job identified
    by the id specified in the path."""
    redis_url = config.REDIS_URL
    redis_conn = redis.from_url(redis_url)
    with Connection(redis_conn):
        q = Queue(name=Configuration.QUEUE)
        task = q.fetch_job(job_id)

    response = {
        'task_status': task.get_status(),
        'data': task.result,
    }

    js = json.dumps(dict(response["data"]))

    return Response(js,
                    mimetype='application/json',
                    headers={f'Content-Disposition': f'attachment;filename=classification_results_job_{job_id}.json'})
