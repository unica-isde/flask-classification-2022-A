"""
This module is responsible to be able to download the results in json format.
It makes the results available through an API.
"""

import json
from app import app
from config import Configuration
from app.routes.classifications_id import classifications_id
from flask import Response

config = Configuration()


@app.route('/classifications/<string:job_id>/results', methods=['GET'])
def get_results_json_for_download(job_id):
    """
    Gets the result from redis and returns a json file.

    Parameters
    ----------
    job_id: id of the job

    Returns
    -------
    The json file as a download, using flask's object Response.
    """
    # get response
    response = classifications_id(job_id=job_id)

    # error handling: if the response is still none, we do again until we have something
    while response["data"] is None:
        response = classifications_id(job_id=job_id)

    # cast into json
    js = json.dumps(dict(response["data"]))

    # return for download
    return Response(js,
                    mimetype='application/json',
                    headers={f'Content-Disposition': f'attachment;filename=classification_results_job_{job_id}.json'})
