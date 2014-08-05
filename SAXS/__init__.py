from Leash import saxsleash,initcommand,validateResponse
import Leash
from saxsdoglib import saxsdog
from ImageQueueLib import imagequeue
from Server import  saxsdogserver
from Server import Server
from Feeder import startfeeder as saxsfeeder
from converter  import convert
from plotchi import plotchi,makeplot
from calibration import calibration,calc_theta, scalemat, openmask
from NetConf import createsaxdogconf as gennetconf
from LeashGui import LeashGUI
try:
    from datamerge import merge
except Error as e:
    print e
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self