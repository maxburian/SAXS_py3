def yDirSliceProjector(x,y,x1,x2,mask):
    a=np.repeat(np.arange(x),y).reshape((x,y))
    maskx=np.zeros((x,y),dtype=bool)
    maskx[mask]=1
    maskx[:,:x1]=1
    maskx[:,x2:]=1
    return SAXS.labelstosparse(a,np.logical_not(maskx),1)
def xDirSliceProjector(x,y,y1,y2,mask):
    a=np.tile(np.arange(y),x).reshape(x,y)
    masky=np.zeros((x,y),dtype=bool)
    masky[mask]=1
    masky[:y1]=1
    masky[y2:]=1
    return SAXS.labelstosparse(a,np.logical_not(masky),1)
class sclice():
    def __init__(self,x,y,sliceconf,mask):
        """ 
        sliceconf dictionary:
        Direction "x"|"y", Plane "InPlane'|'Vertical", CutPosition, CutMargin, IncidentAngle}
        """
        self.sliceconf=sliceconf
        start=scliceconf["CutPosition"]-cliceconf["CutMargin"]
        stop=scliceconf["CutPosition"]+cliceconf["CutMargin"]
        if scliceconf["Direction"]=="x":
            self.Projector=xDirSliceProjector(x,y,start,stop,mask).transpose()
        elif scliceconf["Direction"]=="y":
            self.Projector=yDirSliceProjector(x,y,start,stop,mask).transpose()
        else :
            raise Exception("Invalid Direction: "+ scliceconf["Direction"])
        self.areas=self.Projector.dot(np.ones((x,y)).flatten())
        areaswithoutzero=np.where(self.areas>0.0 ,self.areas,-1.0)
        self.oneoverA=np.where(areaswithoutzero>0,1.0/areaswithoutzero,0)
    def integrate(self,picture):
        return self.Projector.dot(picture.flatten())*self.oneoverA
    def getQscale(self,conf):
        pass
    
        