import SAXS
arg=["../doc/data/powder.chi"]
o={}
o=SAXS.AttrDict(o)
o['compare']=False
o.log=False
o.yax='linear'
o.xax='linear'
o.title="Diffraction Curve"
o.legend=False
o.plotfile=""
o.skip=13
o.clip=40
SAXS.makeplot(o,arg)