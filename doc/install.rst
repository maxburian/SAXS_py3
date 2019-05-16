 
Install
==========


The SAXS Package distributes as a Python package. So in order to use it, you need a Python system installed. The program was originally written in Python 2.7 and has been updated to Python 3.5. **In the future, the AustoSAXS beamline will only support the Python 3.5 version!**

SAXSDog has been developed and tested in a specific Python environment that requires precise control of the used libraries. *We hence suggest to create a dedicated environment as explained further below*.

For software "end-users" we suggest to use the step-by-step instructions below. For implementation in a beamline-network, we recommend contacting the authors as some adjustments in the core-code might have to be necessary, depending on the available hardware infrastructure.

Sources
-------------------------
The source-code of SAXSDog is available from Github. Originally, SAXSdog was implemented in 2014 for Python 2.7. *This version will not be supported/updated by the AustroSAXS beamline!* The original repository can nevertheless be found at::

    https://github.com/ChristianMeisenbichler/SAXS 
    
After several program-extensions and optimizations, the code was updated to be compatible with Python 3.5.5 (last version supporting Qt4). **The latest version of SAXSdog can be obtained from**::

    https://github.com/maxburian/SAXS_py3

Step-by-Step Instructions
-------------------------
The following is a step-by-step instruction to obtain and run SAXSDog on your machine. The instructions are given for Windows - MAC and Linux users might have to adjust them slightly. The SAXSdog code is based on the Anaconda framework, which is cross-platform compatible. In case of problems, please contact the authors.

1) Get Anaconda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download and install the latest Anaconda Package for Python 3.7 from: https://www.anaconda.com/distribution/#download-section 

If you already have a working version of Anaconda, we recommend to use it. However, make sure to **update conda** and **pip**  before creating the environment - see :ref:`createEnv`.

2) Get GIT - version control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download and install the latest GIT distribution from https://git-scm.com

3) Start Anaconda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Start your Anacoda console, by opening the program called **Anaconda prompt** or **Anaconda Powershell Pronpt**.

4) Find your installation path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the command line in the Anaconda console to navigate to the desired SAXSdog installation directory. If you are not sure, we suggest the following commands::

    $ cd ~
    $ mkdir GIT
    $ cd GIT

This will create the folder "GIT" in your user-directory and set the current path to that folder.

5) Get SAXSdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use GIT to download a "clone-copy" of the latest SAXSdog version, by typing ::
    
    $ git clone https://github.com/maxburian/SAXS_py3.git

Once you have downloaded the repository, move to corresponding folder ::

    $ cd SAXS_py3
    
.. _createEnv:

6) Create the Python 3.5 Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SAXSdog is currently supported on Python 3.5 only and it requires very specific packet versions to work flawless. 
In order to create the corresponding environment and install all packages, type:

For Windows::
    
    $ conda env create -f environment_win.yml

    
For Linux/Mac::
    
    $ conda env create -f environment.yml
    
This can now take a few minutes as all packages have to be downloaded and installed.

In case you already have a working Anaconda distribution, you can still use the command above. However, make sure that you 
have **updated conda** using ``$ conda update conda`` and **updated pip** using ``$ conda update pip``. 

In case you want to integrate SAXSdog in your existing environment, use the detailed list of the required dependencies further bellow. 
    
7) Activate the Python Environment 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You must now activate the Python environment such that you work with Python 3.5.5.:
    
For Windows::
    
    $ conda activate py3p5_qt4      
    
For Linux/Mac::
    
    $ source activate py3p5_qt4
    
Make sure that the environment has really been changed! In your command window, you should see something similar to

.. figure:: install_active_env.png
    
8) Install SAXSdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You are now ready to install SAXSdog using the following command::

    $ python setup.py install
    
    

9) Done!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You have now installed SAXSdog and the software is ready to be used. The installer has placed icons in the "Start Menu" as well as on your "Desktop". You can use either one to start "SAXSLeash": the graphical user interface to control your image integration. 


(Optional) Create your Default Network Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SAXSDog is a network-based program. If you want to use it in a feeder-based environment or such that it operates on a remote server, you will have to setup your network configuration. For more information, please read :ref:`saxsdognetwork` and use ::

    % saxsnetconf

This will generate a default configuration file with a random secret. The file must then be saved in ``$User-Home$/.saxdognetwork``.

Dependencies
--------------------
In case you want to create your own environment, we provide a list of the required packages and versions for which SAXSdog has been tested. 

Install using ``$ conda install <module>=<version>=<build>`` :: 

    - python=3.5.5
    - pyqt=4.11.4
      
    - bitarray=0.8.1
    - comtypes=1.1.4        # windows only
    - jsonschema=2.6.0
    - matplotlib=1.5.1
    - numpy=1.11.3
    - numpy-base=1.14.3
    - pandas=0.23.0
    - pillow=3.4.2
    - pip
    - pyqt=4.11.4
    - pytables=3.4.3
    - pywin32=223           # windows only
    - pyzmq=17.0.0
    - scipy=1.1.0
    - sphinx=1.7.9
    - sphinx_rtd_theme=0.4.3
    - sphinxcontrib=1.0
    - sphinxcontrib-websupport=1.0.1
    - xlwt=1.3.0
    
    
Install using ``$ pip install <module>==<version>`` ::

    - python-daemon==2.2.3  # linux only
    - sphinxcontrib-programoutput==0.13
    - sphinxcontrib-programscreenshot==0.0.0
    - watchdog==0.9.0
    - prettyplotlib==0.1.7
    - py2exe==0.9.2.2       # windows only

