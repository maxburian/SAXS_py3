import numpy as np
from calibration import openmask,labelstosparse
 
def yDirSliceProjector(x,y,x1,x2,mask):
    a=np.repeat(np.arange(x),y).reshape((x,y))
    maskx=np.ones((x,y),dtype=bool)
    maskx[np.logical_not(mask)]=0
    maskx[:,:x1]=0
    maskx[:,x2:]=0
    return labelstosparse(a, maskx,1)
def xDirSliceProjector(x,y,y1,y2,mask):
    a=np.tile(np.arange(y),x).reshape(x,y)
    masky=np.ones((x,y),dtype=bool)
    masky[np.logical_not(mask)]=0
    masky[:y1]=0
    masky[y2:]=0
    return labelstosparse(a, masky,1)
 
class slice():
    def __init__(self,conf,sliceconf,attachments):
        """ 
        sliceconf dictionary:
        Direction "x"|"y", Plane "InPlane'|'Vertical", CutPosition, CutMargin, IncidentAngle}
        """
        x=conf["Geometry"]["Imagesize"][0]
        y=conf["Geometry"]["Imagesize"][1]
        self.conf=conf
        self.sliceconf=sliceconf
        start=sliceconf["CutPosition"]-sliceconf["CutMargin"]
        stop=sliceconf["CutPosition"]+sliceconf["CutMargin"]
        if len (conf["Masks"])>0 and sliceconf['MaskRef']>=0:
            self.mask=openmask(conf["Masks"][sliceconf['MaskRef']]["MaskFile"],
                               attachments[sliceconf['MaskRef']])
        else:
            self.mask=np.zeros((x,y))
        if sliceconf["Direction"]=="x":
            self.Projector=xDirSliceProjector(x,y,start,stop,self.mask).transpose()
            self.grid=np.arange(y,dtype=np.float)
        elif sliceconf["Direction"]=="y":
            self.Projector=yDirSliceProjector(x,y,start,stop,self.mask).transpose()
            self.grid=np.arange(x,dtype=np.float)
        else :
            raise Exception("Invalid Direction: "+ sliceconf["Direction"])
        self.areas=self.Projector.dot(np.ones((x,y)).flatten())
        #areaswithoutzero=np.where(self.areas>0.0 ,self.areas,-1.0)
        self.oneoverA=np.where(self.areas>0.0,1.0/self.areas ,np.NAN)
        
    def integrate(self,picture):
        return self.Projector.dot(picture.flatten())*self.oneoverA
   
    def integratechi(self,image,path):
        """
        Integrate and save to file in "chi" format.
        
        :param np.array() image: Image to integrate as numpy array
        :param string path: Path to save the file to
        :returns: Scattering curve data as numpy array 
        """
        r= self.Projector.dot(image.flatten() ) 
        print len(r)
        print len(self.grid)
        data=np.array([self.grid,
                        r *self.oneoverA, 
                        np.sqrt(r ) *self.oneoverA # Poisson Error scaled
                      ]).transpose()
        print data
        
        headerstr=path+" GISAXS Slice\n"
        headerstr+="Pixel"
        headerstr+="Intensity\n"
        headerstr+="   "+str(data.shape[0])+""
        
        np.savetxt(path, data, fmt='%.18e', delimiter=' ', newline='\n ', header=headerstr, footer='', comments='')
        
        
        return {"array":data.transpose().tolist(),
                    "columnLabels":[
                    "Pixel Index",
                    "Intensity (Count/Pixel)",
                    "Error Margin"],
                    "kind":"Slice",
                    "conf":self.sliceconf}
    def plot(self,image,outputfile="",startplotat=0 ,fig=None):
        """
        dummy function in order to not trip up image queue
        """
        pass
        