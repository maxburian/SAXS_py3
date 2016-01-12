 

======================
SAXSDog Documentation!
======================


.. image::  tugwhite.png
   :width: 200 px
 
The SAXS Python package implements analysis tools for Small Angle X-Ray Scattering (SAXS) data. The first and most important one is to efficiently integrate 2d sensor data to an angle dependent diffraction curve.



.. plot:: 
 
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
   
The SAXS module consists of a Python library and 3 command line tools: :ref:`saxsdog`, :ref:`plotchi` and :ref:`converter` and the :ref:`saxsdognetwork` that integrates all of it and provides a GUI, :ref:`saxsleash`.
 


.. toctree::
   :maxdepth: 2
   
   install
   TheTools
   Server
   SAXSSchemaDoc
   TheTechnology
   LeashDeveloperDoc
   SAXSapi
 

`Get this guide as PDF <SAXS.pdf>`_.

.. image::  tugwhite.png
   :width: 200 px