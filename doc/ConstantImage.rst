

Integrating a Constant Image With Masked Values
-----------------------------------------------

This test shows that nothing wrong happens at mask borders. 
For those we want to integrate an image that is one everywhere except for the masked regions

We use the following calibration without Polarization correction and mask:

.. literalinclude:: cal.json

The image we are going to integrate is exactly the array the :py:func:`SAXS.openmask` returns:

.. plot::
   
    import SAXS,json
    from scipy import misc
    import matplotlib.pyplot as plt
    import numpy as np
    conf=json.load(open('cal.json'))
    img =SAXS.openmask(conf["Masks"][0]["MaskFile"])
    img=img.astype(int)
    plt.imshow(img,cmap='Greys')
    plt.colorbar() 
    misc.imsave("mask.tif",img)
   
The result is constant 1 (where the intensity is not 0), save 2e-12.

.. plot::

    import SAXS,json
    from scipy import misc
    import matplotlib.pyplot as plt
    import numpy as np 
    conf=json.load(open('cal.json'))
    img =SAXS.openmask(conf["Masks"][0]["MaskFile"]) 
    img=img.astype(float)
    cal=SAXS.calibration(conf)
    r=cal.integrate(img)
    nonzero=(r[1]!=0)
    plt.plot(r[0][nonzero],r[1][nonzero])
   
