import time

import pandas as pd
import requests

from ..env import KEY
from .base import Base


class flickr(Base):

    DEFAULT_PARAM = {
        "per_page": "500",
        "format": "json",
        "nojsoncallback": "1",
        "has_geo": "1",
        "api_key": KEY,
        "extras": "description, license, date_upload, date_taken, owner_name, \
        icon_server, original_format, last_update, geo, tags, url_l",
    }

    POSSIBLE_PARAMS = (
        "radius",
        "radius_unit",
        "accuracy",
        "min_taken_date",
        "max_taken_date",
        "tags",
    )

    def _formatInput(self, data):

        _params = {"lat": data["lat"], "lon": data["lon"]}

        for term in self.POSSIBLE_PARAMS:
            if term in data and len(data[term]) > 0:
                _params[term] = data[term]

        return {**self.DEFAULT_PARAM, **_params}

    def __init__(self, user, start_time, friendly_id, task, data):

        super().__init__(user, start_time, friendly_id, task)
        self.params = self._formatInput(data)
        self.current_page = 1

    def search(self, first_run=True):

        URL = "https://api.flickr.com/services/rest/?method=flickr.photos.search"

        self.params["page"] = self.current_page

        r = requests.get(url=URL, params=self.params)
        response = r.json()
        print(f"Status: {r}")

        if first_run:
            self.df = pd.DataFrame.from_dict(
                response["photos"]["photo"], orient="columns"
            )
            self.total_page = response["photos"]["pages"]
        else:
            self.df = self.df.append(
                pd.DataFrame.from_dict(response["photos"]["photo"], orient="columns"),
                ignore_index=True,
            )

            try:
                # API timeout and reset
                if str(response["photos"]["pages"]) == "0":
                    print(response)

                    time.sleep(5)
                    self.search(first_run=False)
                else:
                    self.current_page = response["photos"]["page"]
            except ValueError:
                print("Value Error")
                print(response)

        print(f"Page {self.current_page} of {self.total_page}")
        self.current_page = self.current_page + 1

        self.task.update_state(
            state="IN PROGRESS",
            meta={
                "current": self.current_page,
                "total": self.total_page,
                "status": "searching flickr...",
            },
        )

        if self.current_page <= self.total_page:
            time.sleep(0.2)
            self.search(first_run=False)
