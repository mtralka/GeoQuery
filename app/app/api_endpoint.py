
import json
import os

from flask import Blueprint
from flask import abort
from flask import jsonify
from flask import send_file
from flask_login import login_required

from .model import Query
from .search_control import new_search


api_endpoint = Blueprint("api_endpoint", __name__)

api_endpoint.secret_key = os.environ.get("API_ENDPOINT_SECRET_KEY")
WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")
RESULTS_PATH = os.environ.get("RESULTS_PATH")


""" send geojson attatchment """


@api_endpoint.route("/results/<task_id>/geojson")
@login_required
def map(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH,
        str(task.user_id),
        str(task.execution_time),
        "master.geojson",
    )
    attachment_filename = f"results_{str(int(task.execution_time))}"

    try:
        return send_file(
            path,
            as_attachment=True,
            mimetype="json",
            attachment_filename=attachment_filename,
        )
    except FileNotFoundError:
        abort(404)


""" send csv attatchment """


@api_endpoint.route("/results/<task_id>/csv")
@login_required
def csv(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH,
        str(task.user_id),
        str(task.execution_time),
        "master.csv",
    )
    print(os.path.abspath(path))
    attachment_filename = f"results_{str(int(task.execution_time))}.csv"

    try:
        return send_file(
            path,
            as_attachment=True,
            attachment_filename=attachment_filename,
        )
    except FileNotFoundError:
        abort(404)


""" endpoint for task info """


@api_endpoint.route("/info/<task_id>", methods=["GET"])
@login_required
def status_endpoint(task_id):

    friendly = Query.query.filter_by(friendly_id=task_id).first()

    task = new_search.AsyncResult(friendly.id)

    if task.state == "PENDING":
        response = {
            "state": task.state,
            "current": "waiting",
            "total": "waiting",
            "status": "waiting",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current"),
            "total": task.info.get("total"),
            "status": task.info.get("status"),
        }
    else:
        # catch all
        response = {
            "state": task.state,
            "current": task.info.get("current"),
            "total": task.info.get("total"),
            "status": str(task.info),
        }
    return jsonify(response)


""" return geojson of results for leaflet """


@api_endpoint.route("/info/<task_id>/results", methods=["GET"])
@login_required
def get_results(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH, str(task.user_id), str(task.execution_time), "master.geojson"
    )
    try:
        with open(path, "r", encoding="utf8") as file:
            results = json.load(file)
            
    except FileNotFoundError:
        abort(404)

    return results
