from datetime import datetime
import os
import time

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from . import db
from .forms import FlickrSearch
from .model import Query
from .search_control import new_search
from .utilities import create_unique_id


main = Blueprint("main", __name__)

main.secret_key = os.environ.get("MAIN_SECRET_KEY")
WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")
RESULTS_PATH = os.environ.get("RESULTS_PATH")


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


@main.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404")
