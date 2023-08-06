from geodesic.client import get_client
from geodesic import Dataset
from geodesic.stac import FeatureCollection, Item
import time

try:
    import ipywidgets as widgets
    from ipywidgets import VBox, HBox
    from IPython.display import display
    OUTPUT_TYPE = "widget"
except ImportError:
    print("could not import ipywidgets, text output will be used instead")
    OUTPUT_TYPE = "text"

try:
    from ipyleaflet import Map, basemaps, GeoJSON
    USE_MAP = True
except ImportError:
    print("could not load ipyleaflet")
    USE_MAP = False

HOST = "http://localhost:8080"


class Job(dict):
    """Base class for all job types in tesseract.

    This base class has all of the core functionality needed for tesseract jobs except for the submit() funtion.
    Submit should be implemented individually on the different sub-classes since the underlying sub-classes can
    be a bit different and how they are submitted can vary. The class can be initialized either with a dictionary
    that represents the request for the particular type, or can be given an job ID. If a job ID is provided it
    will query for that job on the tesseract service and then update this class with the specifics of that job.

    Args:
        spec(dict): A dictionary representing the job request.
        jobID(str): The jobID string. If provided the job will be initialized
                    with info by making a request to tesseract.
    """
    def __init__(self, spec: dict = None, jobID: str = None):
        self._submitted = False
        self._dataset = None
        self._item = None

        # status values
        self._state = None
        self._nQuarks = None
        self._nCompleted = None

        # geometries
        self._queryGeom = None
        self._quarkGeoms = None

        if isinstance(spec, dict):
            self.update(spec)
            self["f"] = self.get("f", "JSON")  # Always json for now. May add http later
            self["async"] = True

        if jobID is not None:
            self._jobID = jobID
            client = get_client()
            ds = client.get(f'{HOST}/api/v1/job/{self._jobID}')
            self._dataset = Dataset(**ds)
            si = client.get(f'{HOST}/api/v1/job/{self._jobID}/items/1')
            self._item = Item(obj=si, dataset=self._dataset)
            self._queryGeom = self._item.geometry

            st = self.status(returnQuarkGeoms=True)
            qgeoms = st.get('features', None)
            if qgeoms is None:
                raise Exception("job status returned no geometries")
            self._quarkGeoms = FeatureCollection(obj=qgeoms, dataset=self._dataset)

    def status(self, returnQuarkGeoms: bool = False, returnQuarkStatus: bool = False):
        """Status queries the tesseract service for the jobs status.

        Args:
            returnQuarkGeoms(bool): Should the query to the service ask for all of the quarks geometries.
                                    If True it will populate the geometry in this class.
            returnQuarkStatus(bool): If True will query for the status of each individual quark associated with the job.

        returns:
            A dictionary with the response from the Tesseract service

        """
        if not self._jobID:
            raise Exception("jobID not set, cannot get status")
        client = get_client()
        q = {
            "returnQuarkGeoms": returnQuarkGeoms,
            "returnQuarkStatus": returnQuarkStatus
            }
        res = client.get(f'{HOST}/api/v1/job/{self._jobID}/status', **q)
        status = res.get('jobStatus', None)
        if status is None:
            raise Exception("status: could not get job status")

        self._nQuarks = status.get('nQuarks', None)
        self._nCompleted = status.get('nQuarksCompleted', 0)
        self._state = status.get('state', None)

        if returnQuarkGeoms:
            qgeoms = status.get('features', None)
            if qgeoms is None:
                raise Exception("job status returned no geometries")
            self._quarkGeoms = FeatureCollection(obj=qgeoms, dataset=self._dataset)

        return status

    def delete(self):
        """Delete marks a job for deletion in the Tesseract service.

        When delete is called it marks the job to be deleted. This wont immediately delete the job
        from the service. Instead it will just set its state as 'deleted' and it will stop processing
        quarks. If the job is re-submitted it will completely delete the previous job from the service and
        recreate it. Once the job is in the 'deleted' state it will be fully deleted from the service after
        24 hours at which point it is not recoverable.
        """
        if not self._jobID:
            raise Exception("jobID not set, cannot delete")
        client = get_client()
        res = client.delete(f'{HOST}/api/v1/job/{self._jobID}/delete')
        js = res.get('jobStatus', None)
        if js is None:
            raise Exception("could not get confirmation of delete")
        state = js.get('state', None)
        if state is None:
            raise Exception("could not get confirmation of delete")
        self._state = state
        self._submitted = False

    def watch(self):
        """Monitor the tesseract job with the SeerAI widget.

        Will create a jupyter widget that will watch the progress of this tesseract job.
        """
        if not self._jobID:
            raise Exception("jobID not set, nothing to watch")

        self.status()
        if OUTPUT_TYPE == "widget":
            self._prog = widgets.IntProgress(
                value=self._nCompleted,
                min=0,
                max=self._nQuarks,
                step=1,
                description="Running: ",
                bar_style='',
                orientation='horizontal'
            )
            self._title = widgets.HTML(
                value=self._get_title()
            )
            self._ratio = widgets.HTML(
                value=self._get_ratio()
            )

            c = self._item['bbox']
            # bounds = [[c[1], c[0]], [c[3], c[2]]]
            center = (c[2]-c[0], c[3] - c[1])

            map = Map(
                basemap=basemaps.CartoDB.DarkMatter,
                center=center,
                zoom=10,
            )

            vb = VBox([self._title, self._ratio, self._prog])
            w = HBox([vb, map])

            if self._quarkGeoms:
                fc = {
                    'type': 'FeatureCollection',
                    'features': self._quarkGeoms.features
                }
                quarkLayer = GeoJSON(
                    data=fc,
                    style={
                        "opacity": 1,
                        'fillOpacity': 0.1,
                        'color': 'red',
                    },
                    hover_style={
                        'fillOpacity': 0.75,
                    },
                    style_callback=self._quark_color
                )
                map.add_layer(quarkLayer)

            if self._item:
                fci = {
                    'type': 'FeatureCollection',
                    'features': [
                        self._item.__geo_interface__
                    ]
                }
                queryLayer = GeoJSON(
                    data=fci,
                    style={
                        "opacity": 0.5, "color": "red", "fillColor": "yellow", 'weight': 5,
                    },
                    hover_style={
                        'fillOpacity': 0.75
                    }
                )
                # map.fit_bounds(bounds=bounds)
                map.add_layer(queryLayer)
                # rectangle = Rectangle(bounds=bounds)
                # map.add_layer(rectangle)

            display(w)

            keep_watching = True
            while keep_watching:
                time.sleep(5)
                if self._nCompleted == self._nQuarks:
                    self._update_widget()
                    break
                self._update_widget()

    def _update_widget(self):
        self.status()
        # set numerics
        self._prog.value = self._nCompleted
        self._title.value = self._get_title()
        self._ratio.value = self._get_ratio()

        # set geoms

    def _get_title(self):
        return f"<h2>Job ID: {self._jobID} - {self._state}</h2>"

    def _get_ratio(self):
        return f"<h2>{self._nCompleted} / {self._nQuarks}</h2>"

    @staticmethod
    def _quark_color(feature):
        return {
            'color': 'red',
            'fillColor': None,
        }

    @property
    def state(self):
        return self._state
