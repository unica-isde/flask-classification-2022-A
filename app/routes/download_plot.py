"""
This module implements the following functions:
- Create a plot of the results with pyplot.
- Provide the plot in a downloadable format as a route.
"""


import os
from app import app
from config import Configuration, project_root
from matplotlib.pyplot import Figure
from flask import send_from_directory, after_this_request
from app.routes.classifications_id import classifications_id

config = Configuration()

# path where the temporary file is saved
path = project_root + "/app/routes/"


def create_plot(data: dict, filename: str):
    """
    Creates a figure and saves it.

    Parameters
    ----------
    data: dictionary with keys and values that represent the x and y data.
    filename: name of the png file
    """

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.bar(list(data.keys()), list(data.values()), align='center')

    fig.savefig(path + filename)


@app.route('/classifications/<string:job_id>/result_plot', methods=['GET'])
def get_plot_for_download(job_id):
    """
    Connects to redis, gets the results and saves them as a .png file.

    Parameters
    ----------
    job_id: id of the redis job in the queue

    Returns
    -------
    The file of the plot.
    """
    response = classifications_id(job_id=job_id)

    # error handling: if the response is still none, we do again until we have something
    while response["data"] is None:
        response = classifications_id(job_id=job_id)

    data = dict(response["data"])

    filename = f"temp_figure_{job_id}.png"

    create_plot(data=data, filename=filename)

    @after_this_request
    def delete_img(response):
        """
        This removes the image file after the request has been sent.
        Prohibits taking space from (server) hard-drive.

        Parameters
        ----------
        response: Mandatory for flask.

        Returns
        -------
        Response of the request.
        """

        os.remove(path + filename)
        return response

    return send_from_directory(path, filename, as_attachment=True)
