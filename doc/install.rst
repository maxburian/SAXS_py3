 
Install
==========


The SAXS Package distributes as a Python package. So in order to use it, you need a Python system installed. The program was originally written in Python 2.7 and has been updated to Python 3.5. **In the future, the AustoSAXS beamline will only support the Python 3.5 version!**

SAXSDog has been developed and tested in a specific Python environment that requires precise control of the used libraries. *We hence suggest to create a dedicated environment as explained further below*.

For software "end-users" we suggest to use the step-by-step instructions below. For implementation in a beamline-network, we recommend contacting the authors as some adjustments in the core-code might have to be necessary, depending on the available hardware infrastructure.

Step-by-Step Instructions
-------------------------
The following is a step-by-step instruction to obtain and run SAXSDog on your machine. The instructions are given for Windows - MAC and Linux users might have to adjust them slightly. The SAXSdog code is based on the Anaconda framework, which is cross-platform compatible. In case of problems, please contact the authors.

1) Get Anaconda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download and install the latest Anaconda Package for Python 3.7 from: https://www.anaconda.com/distribution/#download-section 

2) Get GIT - version control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download and install the latest GIT distribution from https://git-scm.com

3) Start Anaconda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Start your Anacoda console, which can be found under the name *Anaconda promp* or *Anaconda Powershell Pronpt*.

4) Find your installation path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the command line in the Anaconda console to navigate to the desired SAXSdog installation directory. If you are not sure, we suggest the following commands::

    >> cd ~
    >> mkdir GIT
    >> cd GIT

This will create the folder "GIT" in your user-directory and set the current path to that folder.

5) Get SAXSdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use GIT to download a "clone-copy" of the latest SAXSdog version, by typing ::
    
    >> git clone https://github.com/maxburian/SAXS.git
    
6) Move to SAXS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Change your current directory to the SAXSdog folder by typing ::
    
    >> cd SAXS

7) Create the custom Python Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SAXSdog requires a very specific Python environment to work flawless. In order to install all required dependencies, including the correct Python version, type::

    >> conda create --name py3p5_qt5 --file conda-env.txt
    
This can now take a few minutes as all packages have to be downloaded and installed.

8) Activate the Python Environment 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to activate the Python environment you just created, type::
    
    >> activate py3p5_qt5
    
9) Install SAXSdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You are now ready to install SAXSdog using the following command::

    >> python setup.py install
    
10) Done!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You have now installed SAXSdog and the software is ready to be used. The installer has placed icons in the "Start Menu" as well as on your "Desktop". You can use either one to start "SAXSLeash": the graphical user interface to control your image integration. 


Dependencies
--------------------
In case you want to create your own environment, we provide a list of the required packages and versions for which SAXSdog has been tested. :: 

    **python == 3.5.5**
    **pyqt == 4.11.4**
    bitarray == 0.8.1
    hdf5 == 1.10.2
    jsonschema == 2.6.0
    matplotlib == 1.5.1
    numpy == 1.11.3
    pandas == 0.23.0
    pyzmq == 17.0.0
    scipy == 1.1.0
    setuptools == 39.1.0
    sphinx == 1.7.4
    sphinx_rtd_theme = 0.4.3
    sphinxcontrib == 1.0
    sphinxcontrib-programoutput == 0.13
    sphinxcontrib-programscreenshot == 0.0.0
    watchdog == 0.9.0
    
    prettyplotlib == 0.1.7 (only available over *pip*)



The code can be obtained on github: https://github.com/ChristianMeisenbichler/SAXS where you would also find a "Download Zip" button. After unpacking or cloning with git you end up with a directory called "SAXS" containing the files. Go there, and type into the command line:

.. code::

   python setup.py install
   
This installs the Python module to the environment, creates the command line tools and installs them on the system. Where that is, depends on the Python installation.  The setup script will also try to satisfy all the dependencies by downloading and installing the missing packages. 
