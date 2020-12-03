import os

import geopandas as gpd

from ..model import Query


class Generic:
    def __init__(self, user, start_time, friendly_id, task):

        self.friendly_id = friendly_id
        self.start_time = start_time
        self.user = user
        self.task = task

    def find_celery_id(self, friendly_id):
        return Query.query.filter_by(friendly_id=friendly_id).first().id

    def make_files(self, csv=True, geojson=True, pickle=False):

        file_path = os.path.join("./response", self.user, self.start_time)

        self.task.update_state(
            state="IN PROGRESS", meta={"status": "saving results..."}
        )

        if csv:
            self.df.to_csv(file_path + "/master.csv", index=False)

        if geojson:
            gdf = gpd.GeoDataFrame(
                self.df,
                geometry=gpd.points_from_xy(self.df.longitude, self.df.latitude),
            )
            gdf.to_file(file_path + "/master.geojson", driver="GeoJSON")

        if pickle:
            self.df.to_pickle(file_path + "master.pkl")

        self.task.update_state(
            state="IN PROGRESS", meta={"status": "results saved"}
        )

        print("file save complete")
