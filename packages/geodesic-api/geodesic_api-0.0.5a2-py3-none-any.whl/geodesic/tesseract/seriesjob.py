from typing import Union, List
from geodesic import Dataset
from dateutil.parser import parse
from numpy import dtype as npdtype
from shapely.geometry import shape
from geodesic.stac import Item
from geodesic.client import get_client
from datetime import datetime as dt
from geodesic.tesseract.job import Job
import re

HOST = "http://localhost:8080"
# HOST = TESSERACT_HOST


class FeatureAggrigation(dict):
    def __init__(self, spec: dict = None):
        self._value = None
        self._aggregation_rules = None
        self._groups = None

        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("FeatureAggrigation must be initialised with a dict")

    @property
    def value(self):
        if self._value is not None:
            return self._value
        self._value = self.get('value', None)
        return self._value

    @value.setter
    def value(self, v: Union[str, float, int]):
        assert isinstance(v, (str, float, int))
        self['value'] = v

    @property
    def aggregation_rules(self):
        if self._aggregation_rules is not None:
            return self._aggregation_rules
        self._aggregation_rules = self.get('aggregation_rules', None)
        return self._aggregation_rules

    @aggregation_rules.setter
    def aggregation_rules(self, v: List[str]):
        assert isinstance(v, list)
        self['aggregation_rules'] = v

    @property
    def groups(self):
        if self._groups is not None:
            return self._groups
        self._groups = self.get('groups', None)
        return self._groups

    @groups.setter
    def groups(self, v: List[dict]):
        for i in v:
            if not ('field' in i and 'values' in i):
                raise ValueError("each group must have keys ['field', 'values']")
        self['groups'] = v


class GlobalProperties(dict):
    """These are the global properties specific to the series job type.

    Args:
        spec(dict): A dictionary representing the GlobalProperties portion of the request
    """
    def __init__(self, spec: dict = None):
        self._dtype = None
        self._compression = None
        self._datetime = None
        self._temporal_binning = None

        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("GlobalProperties must be initialised with a dict")

    @property
    def dtype(self, v):
        if self._dtype is not None:
            return self._dtype
        self._dtype = npdtype(self.get('dtype', 'float32'))
        return self._dtype

    @dtype.setter
    def dtype(self, d: dtype):
        self['dtype'] = str(d)

    @property
    def compression(self):
        if self._compression is not None:
            return self._compression
        self._compression = self.get('compression', 'zlib')
        return self._compression

    @compression.setter
    def compression(self, c: str):
        assert isinstance(c, str)
        if not (c in ["zlib", "blosc", "none"]):
            raise ValueError("invalid resample type, must be in ['zlib', 'blosc', 'none']")
        self['compression'] = c

    @property
    def datetime(self):
        if self._datetime is not None:
            return self._datetime
        d = self.get('datetime', None)
        if d is None:
            return None
        dates = d.split('/')
        try:
            return [d for d in map(parse, dates)]
        except Exception as e:
            raise e

    @datetime.setter
    def datetime(self, v: Union[List, tuple]):
        assert isinstance(v, (list, tuple))
        assert len(v) == 2
        if isinstance(v[0], str):
            self['datetime'] = f'{v[0]}/{v[1]}'
        elif isinstance(v[0], dt):
            self['datetime'] = f'{v[0].isoformat()}/{v[1].isoformat()}'
        else:
            raise ValueError("not a recognized datetime format. must be either python datetime or string")

    @property
    def temporal_binning(self):
        if self._temporal_binning is not None:
            return self._temporal_binning
        p = self.get("temporal_binning", {})
        self._temporal_binning = TemporalBinning(p)
        return self._temporal_binning

    @temporal_binning.setter
    def temporal_binning(self, v):
        self['temporal_binning'] = v


#########################################################################################
#  Temporal Binning Classes
#########################################################################################

class Equal(dict):
    def __init__(self, spec: dict = None):
        self._bin_size = None
        self._bin_count = None
        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("TemporalBinning must be initialized with a dict")

    @property
    def bin_size(self):
        if self._bin_size is not None:
            return self._bin_size
        d = self.get('bin_size', None)
        if d is None:
            return None
        dates = d.split('/')
        try:
            return [d for d in map(parse, dates)]
        except Exception as e:
            raise e

    @bin_size.setter
    def bin_size(self, v: Union[List, tuple]):
        assert isinstance(v, (list, tuple))
        assert len(v) == 2
        if isinstance(v[0], str):
            self['bin_size'] = f'{v[0]}/{v[1]}'
        elif isinstance(v[0], dt):
            self['bin_size'] = f'{v[0].isoformat()}/{v[1].isoformat()}'
        else:
            raise ValueError("not a recognized datetime format. must be either python datetime or string")

    @property
    def bin_count(self):
        if self._bin_count is not None:
            return self._bin_count
        self._bin_count = self.get('bin_count', None)
        return self._bin_count

    @bin_count.setter
    def bin_count(self, v: int):
        assert isinstance(v, int)
        self['bin_count'] = v


class User(dict):
    def __init__(self, spec: dict = None):
        self._bins = None
        self._omit_empty = None
        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("User must be initialized with a dict")

    @property
    def bins(self):
        if self._bin_size is not None:
            return self._bin_size
        b = self.get('bin_size', None)
        if not isinstance(b, list):
            raise ValueError("bins must be a list of list of datetimes")
        out = []
        for d in b:
            if d is None:
                return None
            dates = d.split('/')
            try:
                out.append([d for d in map(parse, dates)])
            except Exception as e:
                raise e
        return out

    @bins.setter
    def bin_size(self, v: List[List[str]]):
        assert isinstance(v, (list, tuple))
        bins = []
        for d in v:
            if isinstance(d[0], str):
                bins.append(f'{v[0]}/{v[1]}')
            elif isinstance(v[0], dt):
                bins.append(f'{v[0].isoformat()}/{v[1].isoformat()}')
            else:
                raise ValueError("not a recognized datetime format. must be either python datetime or string")
        self['bins'] = bins

    @property
    def omit_empty(self):
        if self._omit_empty is not None:
            return self._omit_empty
        self._omit_empty = self.get('bin_count', None)
        return self._omit_empty

    @omit_empty.setter
    def omit_empty(self, v: bool):
        assert isinstance(v, bool)
        self['omit_empty'] = v


class Cluster(dict):
    """Cluster spec for temporal binning"""
    def __init__(self, spec: dict = None):
        self._threshold = None
        self._max_cluster_width = None
        self._direction = None

        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("Cluster must be initialized with a dict")

    @property
    def threshold(self):
        if self._threshold is not None:
            return self._threshold
        self._threshold = self.get('threshold', None)
        return self._threshold

    @threshold.setter
    def threshold(self, v: str):
        if not isinstance(v, str):
            raise ValueError("threshold must be of type str")
        r = re.match(r'^\d+[YmdHMS]{1}', v)
        if r:
            self['threshold'] = v
        else:
            raise ValueError(r"threshold must have pattern: '^\d+[YmdHMS]{1}' example: '15H'")

    @property
    def max_cluster_width(self):
        if self._max_cluster_width is not None:
            return self._max_cluster_width
        self._max_cluster_width = self.get('max_cluster_width', None)
        return self._max_cluster_width

    @max_cluster_width.setter
    def max_cluster_width(self, v: str):
        if not isinstance(v, str):
            raise ValueError("max_cluster_width must be of type str")
        r = re.match(r'^\d+[YmdHMS]{1}', v)
        if r:
            self['max_cluster_width'] = v
        else:
            raise ValueError(r"max_cluster_width must have pattern: '^\d+[YmdHMS]{1}' example: '15H'")

    @property
    def direction(self):
        if self._direction is not None:
            return self._direction
        self._direction = self.get('direction', None)
        return self._direction

    @direction.setter
    def direction(self, v: str):
        if not isinstance(v, str):
            raise ValueError("direction must be type str")
        if v not in ['forward', 'backward']:
            raise ValueError("direction must be one of ['forward', 'backward']")
        self['direction'] = v


class TemporalBinning(dict):
    """Temporal binning is a class to represent the temporal binning in a series request.

    Args:
        spec(dict): The dict to initialize the class with.
    """
    def __init__(self, spec: dict = None):
        self._equal = None
        self._user = None
        self._cluster = None
        self._reference = None
        self._aggregation_rules = None

        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("TemporalBinning must be initialized with a dict")

    @property
    def equal(self):
        if self._equal is not None:
            return self._equal
        self._equal = self.get('equal', {})
        return self._equal

    @equal.setter
    def equal(self, v: dict):
        self['equal'] = v

    @property
    def user(self):
        if self._user is not None:
            return self._user
        self._user = User(self.get('user', {}))
        return self._user

    @user.setter
    def user(self, v: dict):
        self['user'] = v

    @property
    def reference(self):
        if self._reference is not None:
            return self._reference
        self._reference = self.get('reference', None)
        return self._reference

    @reference.setter
    def reference(self, v: str):
        if not isinstance(v, str):
            raise ValueError("reference must be a string")
        self['reference'] = v

    @property
    def aggregation_rules(self):
        if self._aggregation_rules is not None:
            return self._aggregation_rules
        self._aggregation_rules = self.get('aggregation_rules', None)
        return self._aggregation_rules

    @aggregation_rules.setter
    def aggregation_rules(self, v: List[str]):
        if not isinstance(v, list):
            raise ValueError("aggregation_rules must be a list of strings")
        for s in v:
            if not (s in ['mean', 'sum', 'first', 'last']):
                raise ValueError("aggregation_rule must be one of ['mean', 'sum', 'first', 'last']")
        self['aggregation_rules'] = v


######################################################################################
# Asset Spec Classes
######################################################################################

class AssetSpec(dict):
    """AssetSpec is a class to represent the requested output assets in a tesseract job.

    Args:
        spec(dict): A dictionary that can be used to initialize the object. Optional.

    """
    def __init__(self, spec: dict = None):
        self._name = None
        self._dataset = None
        self._bands = None
        self._dtype = None
        self._compression = None
        self._input_no_data = None
        self._ids = None
        self._datetime = None
        self._query = None
        self._feature_aggrigation = None
        self._item = None
        self._temporal_binning = None
        self._fill_value = None

        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("AssetSpec must be initialized with a dict")

    @property
    def name(self):
        if self._name is not None:
            return self._name
        self._name = self.get('name', None)
        return self._name

    @name.setter
    def name(self, name: str):
        assert isinstance(name, str)
        self['name'] = name

    @property
    def bands(self):
        if self._bands is not None:
            return self._bands
        self._bands = self.get('bands', None)
        return self._bands

    @bands.setter
    def bands(self, bands: List[str]):
        self['bands'] = bands

    @property
    def dtype(self):
        if self._dtype is not None:
            return self._dtype
        self._dtype = npdtype(self.get('dtype', 'float32'))
        return self._dtype

    @dtype.setter
    def dtype(self, d: npdtype):
        if not isinstance(d, npdtype):
            raise ValueError("dtype must be a numpy dtype")
        self['dtype'] = str(d)

    @property
    def compression(self):
        if self._compression is not None:
            return self._compression
        self._compression = self.get('compression', 'zlib')
        return self._compression

    @compression.setter
    def compression(self, c: str):
        assert isinstance(c, str)
        if not (c in ["zlib", "blosc", "none"]):
            raise ValueError("invalid resample type, must be in ['zlib', 'blosc', 'none']")
        self['compression'] = c

    @property
    def input_no_data(self):
        if self._input_no_data is not None:
            return self._input_no_data
        self._input_no_data = self.get("input_no_data", None)
        return self._input_no_data

    @input_no_data.setter
    def input_no_data(self, v: Union[List[float], float]):
        assert (isinstance(v, List) or isinstance(v, float))
        self['input_no_data'] = v

    @property
    def ids(self):
        if self._ids is not None:
            return self._ids
        self._ids = self.get('ids', None)
        return self._ids

    @ids.setter
    def ids(self, v: List[str]):
        self['ids'] = v

    @property
    def datetime(self):
        if self._datetime is not None:
            return self._datetime
        d = self.get('datetime', None)
        if d is None:
            return None
        dates = d.split('/')
        try:
            return [d for d in map(parse, dates)]
        except Exception as e:
            raise e

    @datetime.setter
    def datetime(self, v: Union[List, tuple]):
        assert isinstance(v, (list, tuple))
        assert len(v) == 2
        if isinstance(v[0], str):
            self['datetime'] = f'{v[0]}/{v[1]}'
        elif isinstance(v[0], dt):
            self['datetime'] = f'{v[0].isoformat()}/{v[1].isoformat()}'
        else:
            raise ValueError("not a recognized datetime format. must be either python datetime or string")

    @property
    def query(self):
        if self._query is not None:
            return self._query
        self._query = self.get("query", None)
        return self._query

    @query.setter
    def query(self, q: dict):
        self['query'] = q

    @property
    def feature_aggrigation(self):
        if self._feature_aggrigation is not None:
            return self._feature_aggrigation
        self._feature_aggrigation = FeatureAggrigation(self.get('feature_aggrigation', {}))
        self._feature_aggrigation

    @feature_aggrigation.setter
    def feature_aggrigation(self, f):
        self['feature_aggrigation'] = f

    @property
    def items(self):
        if self._item is not None:
            return self._item
        self._item = [Item(i) for i in self.get('items', [])]
        return self._item

    @items.setter
    def items(self, v: List[dict]):
        self['items'] = v

    @property
    def fill_value(self):
        if self._fill_value is not None:
            return self._fill_value
        self._fill_value = self.get('fill_value', None)
        return self._fill_value

    @fill_value.setter
    def fill_value(self, v: float):
        self['fill_value'] = v

    @property
    def temporal_binning(self):
        if self._temporal_binning is not None:
            return self._temporal_binning
        p = self.get("temporal_binning", {})
        self._temporal_binning = TemporalBinning(p)
        return self._temporal_binning

    @temporal_binning.setter
    def temporal_binning(self, v):
        self['temporal_binning'] = v


#############################################################################
# Series Job Root Class
#############################################################################

class SeriesJob(Job):
    """SeriesJob represents a tesseract process that produces time series.

    Args:
        desc(dict): A dictionary representing the job request.
        jobID(str): The job ID of a previously submitted job. This will reinitialize this object by querying tesseract.

    """
    def __init__(self, spec: dict = None, jobID: str = None):
        self._geometries = None
        self._geometry_epsg = None
        self._series_format = None
        self._global_properties = None
        self._asset_specs = None
        super().__init__(spec, jobID)

    def submit(self):
        """Submits a job to be processed by tesseract

        This function will take the job defined by this class and submit it to the tesserct api for processing.
        Once submitted the dataset and items fields will be populated containing the SeerAI dataset and STAC items
        respectively. Keep in mind that even though the links to files in the STAC item will be populated, the job
        may not yet be completed and so some of the chunks may not be finished.
        """
        if self._submitted:
            raise Exception("this job has already been submitted. \
                            Create a new SeriesJob if you would like to submit a new job")

        client = get_client()

        res = client.post(f'{HOST}/api/v1/series', **self)

        self._jobID = res.get("jobID", None)
        if self._jobID is None:
            raise ValueError("no jobID was returned, something went wrong")

        ds = res.get('dataset', None)
        if ds is not None:
            self._dataset = Dataset(**ds)

        si = res.get('item', None)
        print(si)
        if si is not None:
            self._item = Item(obj=si, dataset=self._dataset)

        self.status(returnQuarkGeoms=True)
        self._submitted = True
        return f"created job: {self._jobID}"

    @property
    def geometries(self):
        if self._geometries is not None:
            return self._geometries
        gj = self.get("geometries", [])
        self._geometries = [shape(g) for g in gj]

        return self._geometries

    @geometries.setter
    def geometries(self, v: list):
        if isinstance(v, list):
            # If its a dict of geojson then store it internally
            if isinstance(v[0], dict):
                self['geometries'] = v
                return

            geoms = []
            for g in v:
                try:
                    geoms.append(g.__geo_interface__)
                except AttributeError:
                    raise ValueError("input does not appear to be a geometry")
            self._geometries = geoms
        else:
            raise ValueError("input must be a list of geometries")

    @property
    def series_format(self) -> str:
        if self._series_format is not None:
            return self._series_format
        self._series_format = self.get("series_format", None)
        return self._series_format

    @series_format.setter
    def series_format(self, v: str):
        if not isinstance(v, str):
            raise ValueError("series format must be a string and one of ['netcdf', 'json']")
        if v not in ['netcdf', 'json']:
            raise ValueError("series_format must be one of ['netcdf', 'json']")
        self["series_format"] = v

    @property
    def geometry_epsg(self):
        if self._geometry_epsg is not None:
            return self._geometry_epsg

        self._geometry_epsg = self.get("geometry_epsg", None)
        return self._geometry_epsg

    @geometry_epsg.setter
    def geometry_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self["geometry_epsg"] = epsg

    @property
    def global_properties(self):
        if self._global_properties is not None:
            return self._global_properties
        p = self.get("global_properties", {})
        self._global_properties = GlobalProperties(p)
        return self._global_properties

    @global_properties.setter
    def global_properties(self, v):
        self['global_properties'] = v

    @property
    def asset_specs(self):
        if self._asset_specs is not None:
            return self._asset_specs
        a = self.get("asset_specs", {})
        self._asset_specs = AssetSpec(a)
        return self._asset_specs

    @asset_specs.setter
    def asset_specs(self, specs: List[dict]):
        self['asset_specs'] = specs
