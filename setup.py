from setuptools import setup

print("####################################################")
print("       Starting Installation of SaxsDog")
print("####################################################")


versionstring="3.0"
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
    install_requires=["numpy",
                      "scipy", 
                      "matplotlib",
                      "jsonschema", 
                      "bitarray",
                      "watchdog", 
                      "sphinxcontrib-programoutput",
                      "sphinxcontrib-programscreenshot",
                      "pyzmq", "prettyplotlib",
                      "pandas",
                      'winshell;platform_system=="Windows"'],
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
    print("No py2exe here")
 
def get_reg(name,path):
    # Read variable from Windows Registry
    # From https://stackoverflow.com/a/35286642
    try:
        registry_key = wr.OpenKey(wr.HKEY_CURRENT_USER, path, 0,
                                       wr.KEY_READ)
        value, regtype = wr.QueryValueEx(registry_key, name)
        wr.CloseKey(registry_key)
        return value
    except WindowsError:
        return None 
 
from subprocess import call
import sys, os
if sys.argv[1] == 'install':
    if os.name == "nt":
        
        import winreg as  wr
      
        pyw_executable =   os.path.join(sys.prefix, 'pythonw.exe')
        script_file =  '"'+os.path.join(sys.prefix, "Scripts", "leash-script.pyw")+'"'
        iconpath= os.path.expanduser(
            os.path.join(
            sys.prefix,
            "Lib",
            "site-packages", 
            "SAXS",
            "icons",
            "program.ico"))
        wr.SetValue(wr.HKEY_CURRENT_USER, "Software\Classes\TUG.Leash\shell\open\command", wr.REG_SZ, pyw_executable+" \""+ script_file+ "\"  \"%1\"")
        wr.SetValue( wr.HKEY_CURRENT_USER, "Software\Classes\TUG.Leash\DefaultIcon", wr.REG_SZ, iconpath)
        wr.SetValue( wr.HKEY_CURRENT_USER, "Software\Classes\.saxsconf", wr.REG_SZ, "TUG.Leash");
        
        print("added registry values for extensions")
         
        #import winshell
        import win32com.client
        
        w_dir = os.path.expanduser('~')
        regName = 'Desktop'
        regPath = r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
        desktop_path = os.path.normpath(get_reg(regName,regPath))
        #desktop_path = os.path.expanduser("~/Desktop")
        #startmenu_path =win32com.shell.shell.SHGetSpecialFolderPath(0, win32com.shell.shellcon.CSIDL_STARTMENU)
        regName = 'Start Menu'
        startmenu_path = os.path.normpath(get_reg(regName,regPath))
        
        print("  ")
        print("  ")
        print("####################################################")
        print("  ")
        print("Shortcuts for SAXSleash created at:")
        
        '''Startmenu Shortcut'''
        shell = win32com.client.Dispatch("WScript.Shell")
        startmenu_path = startmenu_path.replace("%USERPROFILE%",os.environ['USERPROFILE'])
        linklocation = os.path.join(startmenu_path, 'SAXSLeash.lnk')
        link = shell.CreateShortCut(linklocation)
        link.TargetPath = pyw_executable
        link.Description =  "Control panel for SAXSdog Server"
        link.Arguments =  script_file
        link.IconLocation =iconpath
        link.save()
        print("   -) Start Menu: "+linklocation)
        

        '''Startmenu Shortcut'''
        desktop_path = desktop_path.replace("%USERPROFILE%",os.environ['USERPROFILE'])
        linklocation = os.path.join(desktop_path, 'SAXSLeash.lnk')
        link = shell.CreateShortCut(linklocation)
        link.TargetPath = pyw_executable
        link.Description =  "Control panel for SAXSdog Server"
        link.Arguments =  script_file
        link.IconLocation =iconpath
        link.save()
        print("   -) Dektop:  "+linklocation)
        print("   ")
        
        call(["ie4uinit.exe", "-ClearIconCache"])
    elif os.name == "posix":
        print(os.name)
       
        call(["bash", "addmime.sh"])
        
print("####################################################")
print("        SaxsDog Installation done!")
print("####################################################")