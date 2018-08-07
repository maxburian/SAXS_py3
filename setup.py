from setuptools import setup

versionstring="2.0b1"
 

setup(
    name="SAXS",
    version=versionstring,
    packages=["SAXS"],
    package_data={"SAXS": ["icons/*",
                           "schema.json",
                           "schema_1.json",
                           "LeashRequestSchema.json",
                           "LeashResultSchema.json",
                           "NetworkSchema.json",
                           "LeashMW.ui",
                           "importdialog.ui",
                           "DataConsolidationConf.json",
                           "consolconftemplate.json"
                           ]},
    author="Christian Meisenbichler",
    author_email="chmberg@gmail.com",
    description="Tools for analysing SAXS Data",
    scripts =["postinstall.py"],
    install_requires=["numpy==1.13.1",
                      "scipy==0.16.0", 
                      "matplotlib==1.3.1",
                      "jsonschema==2.4.0", 
                      "bitarray==0.8.1",
                      "watchdog==0.8.2", 
                      "sphinxcontrib-programoutput==0.8",
                      "sphinxcontrib-programscreenshot==0.0.5",
                      "pyzmq==15.2.0","prettyplotlib==0.1.7",
                      "pandas==0.17.1"],
    license="Proprietary",
    entry_points = {
        'console_scripts': [
            'saxsconverter = SAXS:convert',
            'saxsdog = SAXS:saxsdog',
            'plotchi=SAXS:plotchi',
            'saxsdogserver = SAXS:launcher',
            'saxsleash =SAXS:saxsleash',
            'saxsfeeder=SAXS:saxsfeeder',
            "saxsnetconf=SAXS:gennetconf",
            "saxsdmerge=SAXS:merge"
            ],
        'gui_scripts':[
            'leash=SAXS:LeashGUI'
                       ]
        
        
    }
)
try:
    import py2exe
except:
    print "No py2exe here"
 
from subprocess import call
import sys,os
if sys.argv[1] == 'install':
    if os.name == "nt":
        import _winreg as  wr
      
        pyw_executable =   os.path.join(sys.prefix,'pythonw.exe')
        script_file =  '"'+os.path.join(sys.prefix,"Scripts","leash-script.pyw")+'"'
        iconpath= os.path.expanduser(
            os.path.join(
            sys.prefix,
            "Lib",
            "site-packages", 
            "SAXS",
            "icons",
            "program.ico"))
        wr.SetValue(wr.HKEY_CURRENT_USER,"Software\Classes\TUG.Leash\shell\open\command",wr.REG_SZ,pyw_executable+" \""+ script_file+ "\"  \"%1\"")
        wr.SetValue( wr.HKEY_CURRENT_USER,"Software\Classes\TUG.Leash\DefaultIcon",wr.REG_SZ,iconpath)
        wr.SetValue( wr.HKEY_CURRENT_USER,"Software\Classes\.saxsconf",wr.REG_SZ, "TUG.Leash");
        
        print "added registry values for extensions"
         
        import winshell
        import win32com 
        w_dir = os.path.expanduser('~')
        desktop_path = winshell.desktop()
        startmenu_path =win32com.shell.shell.SHGetSpecialFolderPath(0, win32com.shell.shellcon.CSIDL_STARTMENU)
        with winshell.shortcut( os.path.join(startmenu_path,'SAXSLeash.lnk')) as link:
            link.path= pyw_executable
            link.description =  "Control panel for SAXSdog Server"
            link.arguments =  script_file
            link.icon_location=(iconpath,0)
        with winshell.shortcut( os.path.join(desktop_path,'SAXSLeash.lnk')) as link:
            link.path= pyw_executable
            link.description = "Control panel for SAXSdog Server"
            link.arguments =  script_file
            link.icon_location=(iconpath,0)
        print startmenu_path
        call(["ie4uinit.exe" ,"-ClearIconCache"])
    elif os.name == "posix":
        print os.name
       
        call(["bash","addmime.sh"])