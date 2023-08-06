from typing import Union, List
from geodesic import Dataset
from dateutil.parser import parse
from numpy import dtype
from shapely.geometry import box
from geodesic.stac import Item
from geodesic.client import get_client
from datetime import datetime as dt
from geodesic.tesseract.job import Job

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
    def __init__(self, spec: dict = None):
        self._shape = None
        self._pixel_size = None
        self._pixel_dtype = None
        self._compression = None
        self._datetime = None
        self._merge_assets = None

        if isinstance(spec, dict):
            self.update(spec)
        else:
            raise ValueError("GlobalProperties must be initialised with a dict")

    @property
    def shape(self):
        if self._shape is not None:
            return self._shape
        self._shape = self.get('shape', None)
        return self._shape

    @shape.setter
    def shape(self, v: List[int]):
        assert isinstance(v, list)
        assert isinstance(v[0], int)
        assert len(v) == 2
        self['shape'] = v

    @property
    def pixel_size(self):
        if self._pixel_size is not None:
            return self._pixel_size
        self._pixel_size = self.get('pixel_size', None)
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, v: List[float]):
        assert isinstance(v, list)
        assert isinstance(v[0], float)
        assert len(v) == 2
        self['pixel_size'] = v

    @property
    def pixel_dtype(self, v):
        if self._pixel_dtype is not None:
            return self._pixel_dtype
        self._pixel_dtype = dtype(self.get('pixel_dtype', 'float32'))
        return self._pixel_dtype

    @pixel_dtype.setter
    def pixel_dtype(self, d: dtype):
        self['pixel_dtype'] = str(d)

    @property
    def compression(self):
        if self._compression is not None:
            return self._compression
        self._compression = self.get('compression', 'lzw')
        return self._compression

    @compression.setter
    def compression(self, c: str):
        assert isinstance(c, str)
        if not (c in ["lzw", "deflate", "none"]):
            raise ValueError("invalid resample type, must be in ['lzw', 'deflate', 'none']")
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
    def merge_assets(self):
        if self._merge_assets is not None:
            return self._merge_assets
        self._merge_assets = self.get('merge_assets', False)
        return self._merge_assets

    @merge_assets.setter
    def merge_assets(self, v: bool):
        assert isinstance(v, bool)
        self['merge_assets'] = v


class AssetSpec(dict):
    """AssetSpec is a class to represent the requested output assets in a tesseract job.

    Args:
        spec(dict): A dictionary that can be used to initialize the object. Optional.

    """
    def __init__(self, spec: dict = None):
        self._name = None
        self._dataset = None
        self._bands = None
        self._resample = None
        self._processors = None
        self._shape = None
        self._pixel_size = None
        self._pixel_dtype = None
        self._compression = None
        self._input_no_data = None
        self._output_no_data = None
        self._ids = None
        self._datetime = None
        self._query = None
        self._feature_aggrigation = None
        self._item = None
        self._aggregation_rules = None
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
    def dataset(self):
        if self._dataset is not None:
            return self._dataset
        self._dataset = self.get('dataset', None)
        return self._dataset

    @dataset.setter
    def dataset(self, v):
        if not isinstance(v, str):
            raise ValueError("dataset must be a string")
        self['dataset'] = v

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
    def resample(self):
        if self._resample is not None:
            return self._resample
        self._resample = self.get('resample', 'nearest')
        return self._resample

    @resample.setter
    def resample(self, r: str):
        assert isinstance(r, str)
        if not (r in ["nearest", "bilinear", "mean"]):
            raise ValueError("invalid resample type, must be in ['nearest', 'bilinear', 'mean']")
        self['resample'] = r

    @property
    def processors(self):
        if self._processors is not None:
            return self._processors
        self._processors = self.get('processors', None)
        return self._processors

    @processors.setter
    def processors(self, p: List[str]):
        assert isinstance(p, list)
        # Could put some stuff in here to check that the processors are valid
        self['processors'] = p

    @property
    def shape(self):
        if self._shape is not None:
            return self._shape
        self._shape = self.get('shape', None)
        return self._shape

    @shape.setter
    def shape(self, s: List[int]):
        self['shape'] = s

    @property
    def pixel_size(self):
        if self._pixel_size is not None:
            return self._pixel_size
        self._pixel_size = self.get('pixel_size', None)
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, s: List[float]):
        self['pixel_size'] = s

    @property
    def pixel_dtype(self):
        if self._pixel_dtype is not None:
            return self._pixel_dtype
        self._pixel_dtype = dtype(self.get('pixel_dtype', 'float32'))
        return self._pixel_dtype

    @pixel_dtype.setter
    def pixel_dtype(self, d: dtype):
        self['pixel_dtype'] = str(d)

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
    def output_no_data(self):
        if self._output_no_data is not None:
            return self._output_no_data
        self._output_no_data = self.get("output_no_data", None)
        return self._output_no_data

    @output_no_data.setter
    def output_no_data(self, v: Union[List[float], float]):
        assert (isinstance(v, List) or isinstance(v, float))
        self['output_no_data'] = v

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
    def aggregation_rules(self):
        if self._aggregation_rules is not None:
            return self._aggregation_rules
        self._aggregation_rules = self.get('aggregation_rules', None)
        return self._aggregation_rules

    @aggregation_rules.setter
    def aggregation_rules(self, r: dict):
        self['aggregation_rules'] = r

    @property
    def fill_value(self):
        if self._fill_value is not None:
            return self._fill_value
        self._fill_value = self.get('fill_value', None)
        return self._fill_value

    @fill_value.setter
    def fill_value(self, v: float):
        self['fill_value'] = v


class RasterJob(Job):
    """RasterJob represents a tesseract process that produces a raster.

    Args:
        desc(dict): A dictionary representing the job request.

    """
    def __init__(self, spec: dict = None, jobID: str = None):
        self._bbox = None
        self._bbox_epsg = None
        self._raster_format = None
        self._output_epsg = None
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
                            Create a new RasterJob if you would like to submit a new job")

        client = get_client()

        res = client.post(f'{HOST}/api/v1/raster', **self)

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
    def bbox(self):
        if self._bbox is not None:
            return self._bbox
        bb = self.get("bbox", [])
        if len(bb) >= 4:
            self._bbox = box(bb[0], bb[1], bb[2], bb[3])
        return self._bbox

    @bbox.setter
    def bbox(self, b):
        if isinstance(b, list):
            self['bbox'] = b
            return
        try:
            self['bbox'] = b.__geo_interface__
            try:
                self['bbox'] = b.bounds
            except AttributeError:
                try:
                    self['bbox'] = b.extent
                except Exception:
                    pass
            return
        except AttributeError:
            raise ValueError("unknown bbox or geometry type")

    @property
    def raster_format(self) -> str:
        if self._raster_format is not None:
            return self._raster_format
        self._raster_format = self.get("raster_format", None)
        return self._raster_format

    @raster_format.setter
    def raster_format(self, f: str):
        assert isinstance(f, str)
        self["raster_format"] = f

    @property
    def bbox_epsg(self):
        if self._bbox_epsg is not None:
            return self._bbox_epsg

        self._bbox_epsg = self.get("bbox_epsg", None)
        return self._bbox_epsg

    @bbox_epsg.setter
    def bbox_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self["bbox_epsg"] = epsg

    @property
    def output_epsg(self):
        if self._output_epsg is not None:
            return self._output_epsg

        self._output_epsg = self.get("output_epsg", None)
        return self._output_epsg

    @output_epsg.setter
    def output_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self["output_epsg"] = epsg

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
