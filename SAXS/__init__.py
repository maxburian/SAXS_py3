
from saxsdoglib import saxsdog
from ImageQueueLib import imagequeue
from Server import  saxsdogserver
from Leash import saxsleash
from Feeder import startfeeder as saxsfeeder
from converter  import convert
from plotchi import plotchi,makeplot
from calibration import calibration,calc_theta, scalemat, openmask
 
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self