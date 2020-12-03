from datetime import datetime
import json
import os
import time

from celery import Celery
from flask import Blueprint
from flask import abort
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from sqlalchemy.sql.elements import Null

from . import celery
from . import db
from .forms import FlickrSearch
from .model import Query
from .model import User
from .search_control import new_search
from .utilities import create_unique_id


RESULTS_PATH = ".\\response"

main = Blueprint("main", __name__)

main.secret_key = "SECRETKEY"
WTF_CSRF_SECRET_KEY = "CSRFSECRET"


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/search", methods=["GET", "POST"])
def search():

    form = FlickrSearch()

    if form.validate_on_submit():

        if form.validate() is False:

            flash("Failed Validation")
            return redirect(url_for("main.search"))

        else:

            data = request.form
            # user = current_user.id
            user = "test_user_2"  # for testing only
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
                min_taken=data.get("min_taken"),
                max_taken=data.get("max_taken"),
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
def status_landing():

    # TODO implement input page for manual status search w/ friendly id
    return render_template("status.html")


""" Gives of search task by id """


@main.route("/results/<task_id>")
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


""" url for returning map by id """


@main.route("/results/<task_id>/geojson")
def map(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH, str(task.user_id), str(task.execution_time)
    )

    try:
        return send_from_directory(path, filename='master.geojson', as_attachment=True)
    except FileNotFoundError:
        abort(404)
    

@main.route("/results/<task_id>/csv")
def csv(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH, str(task.user_id), str(task.execution_time)
    )

    try:
        return send_from_directory(path, filename='master.csv', as_attachment=True)
    except FileNotFoundError:
        abort(404)
    


""" endpoint for search task info """


@main.route("/info/<task_id>", methods=["GET"])
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
        # wrong
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),
        }
    return jsonify(response)


""" send geojson of results """


@main.route("/info/<task_id>/results", methods=["GET"])
def get_results(task_id):

    task = Query.query.filter_by(friendly_id=task_id).first()

    path = os.path.join(
        RESULTS_PATH, str(task.user_id), str(task.execution_time), "master.geojson"
    )
    print(path)
    try:
        with open(path, "r", encoding="utf8") as file:
            results = json.load(file)
    except FileNotFoundError:
        results = Null

    return results


# TODO adjust and implement
@main.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404")
