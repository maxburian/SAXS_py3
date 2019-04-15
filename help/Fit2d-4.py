import SAXS
arg=["../doc/data/fit2d","../doc/data/saxsdog"]
o={}
o=SAXS.AttrDict(o)
o['compare']=False
o.log=False
o.yax='linear'
o.xax='linear'
o.title="Tail Region"
o.legend=True
o.plotfile=""
o.skip=850
o.clip=40
SAXS.makeplot(o,arg)