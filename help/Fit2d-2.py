import SAXS
arg=["../doc/data/fit2d","../doc/data/saxsdog"]
o={}
o=SAXS.AttrDict(o)
o['compare']=True
o.log=False
o.yax='linear'
o.xax='linear'
o.title="Difference"
o.legend=True
o.plotfile=""
SAXS.makeplot(o,arg)