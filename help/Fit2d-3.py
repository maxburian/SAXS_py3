import SAXS
arg=["../doc/data/fit2d","../doc/data/saxsdog"]
o={}
o=SAXS.AttrDict(o)
o.yax='linear'
o.xax='linear'
o['compare']=False
o.log=False
o.title="From the middle"
o.legend=True
o.plotfile=""
o.skip=350
o.clip=480
SAXS.makeplot(o,arg)