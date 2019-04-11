 
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

    $ cd ~
    $ mkdir GIT
    $ cd GIT

This will create the folder "GIT" in your user-directory and set the current path to that folder.

5) Get SAXSdog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use GIT to download a "clone-copy" of the latest SAXSdog version, by typing ::
    
    $ git clone https://github.com/maxburian/SAXS_py3.git

Once you have downloaded the repository, move to correpsonding folder ::

    $ cd SAXS_py3
    

6) Create the Python 3.5 Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SAXSdog is currently supported on Python 3.5 only and it requires very specific packet versions to work flawless. In order to create the corresponding environment and install all packages, type::

    $ conda env create -f environment.yml
    
This can now take a few minutes as all packages have to be downloaded and installed.

In case you want to integrate SAXSdog in your existing environment, use the detailed list of the required dependencies further bellow.
    
7) Activate the Python Environment 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You must now activate the Python environment such that you work with Python 3.5.5.::
    
    $ conda activate py3p5_qt4

    
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

This will generate a default configuration file with a random secret. The file must then be saved in ``$Home/.saxdognetwork``.

Dependencies
--------------------
In case you want to create your own environment, we provide a list of the required packages and versions for which SAXSdog has been tested. 

Install using ``$ conda install <module>=<version>=<build>`` :: 

    - python=3.5.5=h0c2934d_2
    - pyqt=4.11.4=py35_7
      
    - bitarray=0.8.1=py35hfa6e2cd_1
    - comtypes=1.1.4=py35_0
    - jsonschema=2.6.0=py35h27d56d3_0
    - matplotlib=1.5.1=np111py35_0
    - numpy=1.11.3=py35h4a99626_4
    - numpy-base=1.14.3=py35h5c71026_0
    - pandas=0.23.0=py35h830ac7b_0
    - pillow=3.4.2=py35_0
    - pyqt=4.11.4=py35_7
    - pytables=3.4.3=py35he6f6034_1
    - pywin32=223=py35hfa6e2cd_1
    - pyzmq=17.0.0=py35hfa6e2cd_1
    - scipy=1.1.0=py35h672f292_0
    - sphinx=1.7.9=py35_0
    - sphinx_rtd_theme=0.4.3=py_0
    - sphinxcontrib=1.0=py35_1
    - sphinxcontrib-websupport=1.0.1=py35ha3690eb_1
    - xlwt=1.3.0=py35hd04410a_0
    
    
Install using ``$ pip install <module>==<version>`` ::

    - sphinxcontrib-programoutput==0.13
    - sphinxcontrib-programscreenshot==0.0.0
    - watchdog==0.9.0
    - prettyplotlib==0.1.7
    - py2exe==0.9.2.2 


The code can be obtained on github: https://github.com/ChristianMeisenbichler/SAXS 