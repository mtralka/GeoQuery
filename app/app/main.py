from datetime import datetime
import json
from logging import log
import os
import time

from flask import Blueprint
from flask import abort
from flask import flash
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for
from flask.wrappers import Response
from flask_login import current_user
from flask_login import login_required

from . import db
from .forms import FlickrSearch
from .model import Query
from .search_control import new_search
from .utilities import create_unique_id


main = Blueprint("main", __name__)

main.secret_key = "SECRETKEY"
WTF_CSRF_SECRET_KEY = "CSRFSECRET"
RESULTS_PATH =  "/app/response"


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/search", methods=["GET", "POST"])
@login_required
def search():

    form = FlickrSearch()

    if form.validate_on_submit():

        if form.validate() is False:

            flash("Failed Validation")
            return redirect(url_for("main.search"))

        else:

            data = request.form
            user = current_user.id
            #  user = "test_user" #  testing only
            task_time = str(time.time())
            friendly_id = create_unique_id()

            # Async Task Register
            task = new_search.delay(data, user, task_time, friendly_id)

            print(task.state)
            print(task.id)

            # Create and Submit DB Query Entry
            query = Query(
                id=str(task.id),
                user_id=user,
                friendly_id=friendly_id,
                execution_time=task_time,
                lat=data.get("lat"),
                lon=data.get("lon"),
                min_taken=data.get("min_taken_date"),
                max_taken=data.get("max_taken_date"),
                accuracy=data.get("accuracy"),
                radius=data.get("radius"),
                radius_units="KM",
                tags=data.get("tags"),
            )
            db.session.add(query)
            db.session.commit()
            return redirect(f"/results/{friendly_id}")

    return render_template("search.html", form=form, title="Search")


@main.route("/status", methods=["GET", "POST"])
@login_required
def status_landing():

    # TODO implement input page for manual status search w/ friendly id
    return render_template("status.html")


""" render results page """


@main.route("/results/<task_id>")
@login_required
def status_dash(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()
    started = datetime.fromtimestamp(task.execution_time).strftime("%Y-%m-%d %H:%M")

    return render_template(
        "results.html",
        task_id=task_id,
        task=task,
        started=started,
        title="Results",
    )


""" send geojson attatchment """


@main.route("/results/<task_id>/geojson")
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


@main.route("/results/<task_id>/csv")
@login_required
def csv(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH,
        str(task.user_id),
        str(task.execution_time),
        "master.csv",
    )
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


@main.route("/info/<task_id>", methods=["GET"])
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


@main.route("/info/<task_id>/results", methods=["GET"])
@login_required
def get_results(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH, str(task.user_id), str(task.execution_time), "master.geojson"
    )
    try:
        with open(path, "r", encoding="utf8") as file:
            results = json.load(file)
            print(results)
    except FileNotFoundError:
        abort(404)

    return results


@main.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404")