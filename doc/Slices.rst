

GISAXS Slices
-------------

In grasing incidend SAXS looking at radial integration doesnt make much sence. 
In GISAXS you rather want to look at horizontal or vertical sclices. That is horizontal or vertical with
respect to the scattering surface.

The SAXSDog tools allow to specify :ref:`Slices` of pixels and allow to look at them at the :math:`q_y`, 
:math:`q_z` 
scale as they are used in GISAX analysis.

The :py:class:`slice` class implements this functionality very much the same as the radial 
integration except that 
the labels of the pixels simply are the integer x coordinate in pixels when we want a slice in x direction
and the y coordinate when we want the slice in y direction. 
Oversampling doesnt make any sense in this scenario but the rest is the same. 
The only subtile thing is to calulate the :math:`q_y` and :math:`q_z` scale. Because the dedector coorinatesystem 
may have the x or the y axis aligned with the scattering
suface the :ref:`Slices` allows to chose wether we are in plane or verical to the scattering surface.
If you want to get correct :math:`q_z` values you must also specify the incident angle :math:`\alpha_i`, (:ref:`incidentangle`)





