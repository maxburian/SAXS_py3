import SAXS
arg=["../doc/data/fit2d","../doc/data/saxsdog"]
o={}
o=SAXS.AttrDict(o)
o['compare']=False
o.log=True
o.yax='linear'
o.xax='linear'
o.title="Close to Beam"
o.legend=True
o.plotfile=""
o.skip=13
o.clip=960
SAXS.makeplot(o,arg)