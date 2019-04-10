from .calibrationhelper import openmask
from PyQt4 import  QtGui
from PyQt4 import  QtCore
from scipy.misc.pilutil import toimage
from PIL.ImageQt import ImageQt
def nparrayToQPixmap(arrayImage):
    pilImage = toimage(arrayImage.astype('float'))
    qtImage = ImageQt(pilImage.convert("RGBA"))
    qImage =  QtGui.QImage(qtImage)
    qPixmap =  QtGui.QPixmap(qImage)
  
    return qPixmap
def getMaskPixMapFromFile(file):
    array=openmask(file)
    return nparrayToQPixmap(array)