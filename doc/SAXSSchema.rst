.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. _required:

 The ':red:`*`' signifies a required Field.

The SAXS configuration file specifies the parameters of a SAXS sensor calibration. It is written in the JSON format which governs the general syntax.


:Type:
  object
:Contains:
  :ref:`Title <Title>`, :ref:`Geometry <Geometry>`:red:`*`, :ref:`Masks <Masks>`:red:`*`, :ref:`Slices <Slices>`, :ref:`Wavelength <Wavelength>`:red:`*`, :ref:`PolarizationCorrection <PolarizationCorrection>`, :ref:`Directory <Directory>`:red:`*`, :ref:`Threads <Threads>`
:Required:
  True
:JSON Path:
  * :ref:`# <root>` 

Example JSON: 

.. code:: json

    {
      "Geometry": {
        "Tilt": {
          "TiltRotDeg": 0,
          "TiltAngleDeg": 0
        },
        "Imagesize": [
          1000,
          900
        ],
        "BeamCenter": [
          800.0,
          400.0
        ],
        "PixelSizeMicroM": [
          100.0
        ],
        "DedectorDistanceMM": 1000.0
      },
      "Wavelength": 1.54,
      "Directory": [],
      "Masks": []
    }

.. _Title:

Title
-------------------------

:Type:
  string
:Required:
  False
:JSON Path:
  * :ref:`# <root>` [':ref:`Title <Title>`']

Example JSON: 

.. code:: json

    {"Title": ""}

.. _Geometry:

Geometry
-------------------------

:Type:
  object
:Contains:
  :ref:`Tilt <Tilt>`:red:`*`, :ref:`BeamCenter <BeamCenter>`:red:`*`, :ref:`DedectorDistanceMM <DedectorDistanceMM>`:red:`*`, :ref:`PixelSizeMicroM <PixelSizeMicroM>`:red:`*`, :ref:`Imagesize <Imagesize>`:red:`*`
:Required:
  True
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`']

Example JSON: 

.. code:: json

    {
      "Geometry": {
        "Tilt": {
          "TiltRotDeg": 0,
          "TiltAngleDeg": 0
        },
        "Imagesize": [
          1000,
          900
        ],
        "BeamCenter": [
          800.0,
          400.0
        ],
        "PixelSizeMicroM": [
          100.0
        ],
        "DedectorDistanceMM": 1000.0
      }
    }

.. _Tilt:

Tilt
-------------------------

The sensor, usually is not perfectly perpenticular to the ray direction. The tilt angle can be specified by giving the following paramters.


:Type:
  object
:Contains:
  :ref:`TiltRotDeg <TiltRotDeg>`:red:`*`, :ref:`TiltAngleDeg <TiltAngleDeg>`:red:`*`
:Required:
  True
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`'][':ref:`Tilt <Tilt>`']

Example JSON: 

.. code:: json

    {"Tilt": {"TiltRotDeg": 0,"TiltAngleDeg": 0}}

.. _TiltRotDeg:

TiltRotDeg
-------------------------

This gives the angel of the tilt direction.


:Type:
  number in degree
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`'][':ref:`Tilt <Tilt>`'][':ref:`TiltRotDeg <TiltRotDeg>`']

Example JSON: 

.. code:: json

    {"TiltRotDeg": 0}

.. _TiltAngleDeg:

TiltAngleDeg
-------------------------

This gives the angle between the ray direction and the normal to the sensor plane.


:Type:
  number in degree
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`'][':ref:`Tilt <Tilt>`'][':ref:`TiltAngleDeg <TiltAngleDeg>`']

Example JSON: 

.. code:: json

    {"TiltAngleDeg": 0}

.. _BeamCenter:

BeamCenter
-------------------------

Gives the beam center in pixel coorinates.


:Type:
  array(2) items: number 
:Required:
  True
:Default:
  [800.0, 400.0]
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`'][':ref:`BeamCenter <BeamCenter>`']

Example JSON: 

.. code:: json

    {"BeamCenter": [800.0,400.0]}

.. _DedectorDistanceMM:

DedectorDistanceMM
-------------------------

Distance between diffraction center and sensor.


:Type:
  number in Millimeters
:Required:
  True
:Default:
  1000.0
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`'][':ref:`DedectorDistanceMM <DedectorDistanceMM>`']

Example JSON: 

.. code:: json

    {"DedectorDistanceMM": 1000.0}

.. _PixelSizeMicroM:

PixelSizeMicroM
-------------------------

The pixel size on the sensor.


:Type:
  array(2) items: number 
:Required:
  True
:Default:
  [100.0]
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`'][':ref:`PixelSizeMicroM <PixelSizeMicroM>`']

Example JSON: 

.. code:: json

    {"PixelSizeMicroM": [100.0]}

.. _Imagesize:

Imagesize
-------------------------

Size of sensor image in pixel.


:Type:
  array(2) items: integer 
:Required:
  True
:Default:
  [1000, 900]
:JSON Path:
  * :ref:`# <root>` [':ref:`Geometry <Geometry>`'][':ref:`Imagesize <Imagesize>`']

Example JSON: 

.. code:: json

    {"Imagesize": [1000,900]}

.. _Masks:

Masks
-------------------------

:Type:
  array() items: {:ref:`MaskFile`, :ref:`Oversampling`, :ref:`PixelPerRadialElement`, :ref:`Name`, :ref:`qStart`, :ref:`qStop`}
:Required:
  True
:JSON Path:
  * :ref:`# <root>` [':ref:`Masks <Masks>`']

Example JSON: 

.. code:: json

    {"Masks": []}

.. _MaskFile:

MaskFile
-------------------------

Path of Maskfile


:Type:
  string
:Required:
  True
:Default:
  AAA_integ.msk
:JSON Path:
  * :ref:`# <root>` [':ref:`Masks <Masks>`'][0][':ref:`MaskFile <MaskFile>`']

Example JSON: 

.. code:: json

    {"MaskFile": "AAA_integ.msk"}

.. _Oversampling:

Oversampling
-------------------------

Oversampling factor for radial integration. The higher, the longer the setup but the higher the accuracy. More then 3 is probably overkill. 


:Type:
  integer
:Required:
  True
:Default:
  3
:JSON Path:
  * :ref:`# <root>` [':ref:`Masks <Masks>`'][0][':ref:`Oversampling <Oversampling>`']

Example JSON: 

.. code:: json

    {"Oversampling": 3}

.. _PixelPerRadialElement:

PixelPerRadialElement
-------------------------

Expresses the width of a radial step in terms of pixels. '1' means :math:`\delta R\approx 1` :ref:`PixelSizeMicroM`.


:Type:
  number in Pixel
:Required:
  True
:Default:
  1
:JSON Path:
  * :ref:`# <root>` [':ref:`Masks <Masks>`'][0][':ref:`PixelPerRadialElement <PixelPerRadialElement>`']

Example JSON: 

.. code:: json

    {"PixelPerRadialElement": 1}

.. _Name:

Name
-------------------------

Name for mask configuration.


:Type:
  string
:Required:
  False
:JSON Path:
  * :ref:`# <root>` [':ref:`Masks <Masks>`'][0][':ref:`Name <Name>`']

Example JSON: 

.. code:: json

    {"Name": ""}

.. _qStart:

qStart
-------------------------

Starting q-value for Integral Parameters.


:Type:
  number in nm^-1
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <root>` [':ref:`Masks <Masks>`'][0][':ref:`qStart <qStart>`']

Example JSON: 

.. code:: json

    {"qStart": 0}

.. _qStop:

qStop
-------------------------

Ending q-value for Integral Parameters.


:Type:
  number in nm^-1
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <root>` [':ref:`Masks <Masks>`'][0][':ref:`qStop <qStop>`']

Example JSON: 

.. code:: json

    {"qStop": 0}

.. _Slices:

Slices
-------------------------

Slices are designed to analyse GISAXS data.It allows you to specify slices along the sensor axis and get intensity along :math:`q_x`, :math:`q_z` directions.


:Type:
  array() items: {:ref:`Direction`, :ref:`Plane`, :ref:`CutPosition`, :ref:`CutMargin`, :ref:`IncidentAngle`, :ref:`MaskRef`}
:Required:
  False
:JSON Path:
  * :ref:`# <root>` [':ref:`Slices <Slices>`']

Example JSON: 

.. code:: json

    {"Slices": []}

.. _Direction:

Direction
-------------------------

'x' or 'y' direction in sensor pixel coordinates.


:Type:
  string
:values:
  [x, y]

:Required:
  True
:Default:
  x
:JSON Path:
  * :ref:`# <root>` [':ref:`Slices <Slices>`'][0][':ref:`Direction <Direction>`']

Example JSON: 

.. code:: json

    {"Direction": "x"}

.. _Plane:

Plane
-------------------------

Whether the direction is in plane with scattering surface or vertical to it.


:Type:
  string
:values:
  [InPlane, Vertical]

:Required:
  True
:Default:
  InPlane
:JSON Path:
  * :ref:`# <root>` [':ref:`Slices <Slices>`'][0][':ref:`Plane <Plane>`']

Example JSON: 

.. code:: json

    {"Plane": "InPlane"}

.. _CutPosition:

CutPosition
-------------------------

Cut position in pixel coordinates in the other coodinate then specified in 'Direction'. Origin is top left Corner.


:Type:
  integer in Pixel
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <root>` [':ref:`Slices <Slices>`'][0][':ref:`CutPosition <CutPosition>`']

Example JSON: 

.. code:: json

    {"CutPosition": "0"}

.. _CutMargin:

CutMargin
-------------------------

Number of pixels left and right from  cut to include into the average .


:Type:
  integer in Pixel
:Required:
  True
:Default:
  1
:JSON Path:
  * :ref:`# <root>` [':ref:`Slices <Slices>`'][0][':ref:`CutMargin <CutMargin>`']

Example JSON: 

.. code:: json

    {"CutMargin": 1}

.. _IncidentAngle:

IncidentAngle
-------------------------

Angle of incidence in GISAXS setup.


:Type:
  number in degree
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <root>` [':ref:`Slices <Slices>`'][0][':ref:`IncidentAngle <IncidentAngle>`']

Example JSON: 

.. code:: json

    {"IncidentAngle": 0}

.. _MaskRef:

MaskRef
-------------------------

Chose which mask to use for the sclice. '-1' means don't use mask


:Type:
  integer
:Required:
  True
:Default:
  0
:JSON Path:
  * :ref:`# <root>` [':ref:`Slices <Slices>`'][0][':ref:`MaskRef <MaskRef>`']

Example JSON: 

.. code:: json

    {"MaskRef": 0}

.. _Wavelength:

Wavelength
-------------------------

Refined wavelength.


:Type:
  number in Angstrom
:Required:
  True
:Default:
  1.54
:JSON Path:
  * :ref:`# <root>` [':ref:`Wavelength <Wavelength>`']

Example JSON: 

.. code:: json

    {"Wavelength": 1.54}

.. _PolarizationCorrection:

PolarizationCorrection
-------------------------

The scattering direction id dependend on the light polarization. This may be acconted for with the polarization correction.


:Type:
  object
:Contains:
  :ref:`Fraction <Fraction>`:red:`*`, :ref:`Angle <Angle>`:red:`*`
:Required:
  False
:Default:
  OrderedDict([(u'Fraction', 0.95), (u'Angle', 0)])
:JSON Path:
  * :ref:`# <root>` [':ref:`PolarizationCorrection <PolarizationCorrection>`']

Example JSON: 

.. code:: json

    {"PolarizationCorrection": {"Angle": 0.0,"Fraction": 0.95}}

.. _Fraction:

Fraction
-------------------------

Fraction of light polarized in the given (:ref:`Angle`) direction.


:Type:
  number
:Required:
  True
:Default:
  0.95
:JSON Path:
  * :ref:`# <root>` [':ref:`PolarizationCorrection <PolarizationCorrection>`'][':ref:`Fraction <Fraction>`']

Example JSON: 

.. code:: json

    {"Fraction": 0.95}

.. _Angle:

Angle
-------------------------

Angle of the polarization plane.


:Type:
  number in degree
:Required:
  True
:Default:
  0.0
:JSON Path:
  * :ref:`# <root>` [':ref:`PolarizationCorrection <PolarizationCorrection>`'][':ref:`Angle <Angle>`']

Example JSON: 

.. code:: json

    {"Angle": 0.0}

.. _Directory:

Directory
-------------------------

Directory to take into acount for processing images. Given as a list of subdirectories.


:Type:
  array() items: string 
:Required:
  True
:JSON Path:
  * :ref:`# <root>` [':ref:`Directory <Directory>`']

Example JSON: 

.. code:: json

    {"Directory": []}

.. _Threads:

Threads
-------------------------

:Type:
  integer
:Required:
  False
:Default:
  2
:JSON Path:
  * :ref:`# <root>` [':ref:`Threads <Threads>`']

Example JSON: 

.. code:: json

    {"Threads": 2}

