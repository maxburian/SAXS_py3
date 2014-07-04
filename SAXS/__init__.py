
from saxsdoglib import saxsdog
from ImageQueueLib import imagequeue
from converter  import convert
from plotchi import plotchi,makeplot
from calibration import calibration,calc_theta, scalemat, openmask
import tifffile
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self