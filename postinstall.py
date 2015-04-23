import sys
import os

 
 
desktop = get_special_folder_path("CSIDL_COMMON_DESKTOPDIRECTORY")
startmenu = get_special_folder_path("CSIDL_COMMON_STARTMENU")
 

pyw_executable =   os.path.join(sys.prefix,'pythonw.exe')
script_file =  '"'+os.path.join(sys.prefix,"Scripts","leash-script.pyw")+'"'
w_dir = os.path.expanduser('~')
desktop_path = get_special_folder_path("CSIDL_DESKTOPDIRECTORY")
startmenu_path = get_special_folder_path("CSIDL_STARTMENU")
iconpath= os.path.expanduser(
        os.path.join(
        sys.prefix,
        "Lib",
        "site-packages", 
        "SAXS",
        "icons",
        "program.ico"))
print(sys.argv)

if sys.argv[1] == '-install':
    print('Creating Shortcut')
    create_shortcut(
        pyw_executable,
        'SAXSDogLeash',
       os.path.join(startmenu_path,'SAXSLeash.lnk'),
        script_file,
        w_dir,
       iconpath,0)
 
    print('Creating Shortcut')
    create_shortcut(
        pyw_executable,
        'SAXSDogLeash',
        os.path.join(desktop_path,'SAXSLeash.lnk'),
        script_file,
        w_dir,
       iconpath,0)
    import _winreg as  wr
    wr.SetValue(wr.HKEY_CURRENT_USER,"Software\Classes\TUG.Leash\shell\open\command",wr.REG_SZ,pyw_executable+" \""+ script_file+ "\"  \"%1\"")
    wr.SetValue( wr.HKEY_CURRENT_USER,"Software\Classes\TUG.Leash\DefaultIcon",wr.REG_SZ,iconpath)
    wr.SetValue( wr.HKEY_CURRENT_USER,"Software\Classes\.saxsconf",wr.REG_SZ, "TUG.Leash");
    print "Update Registry:"
    from subprocess import call
    call(["conda","install","--yes","pip"])
    call(["pip","install","numpy",
                      "scipy", 
                      "matplotlib",
                      "jsonschema", 
                      "bitarray",
                      "watchdog",
                      "sphinxcontrib-programoutput",
                      "sphinxcontrib-programscreenshot",
                      "pyzmq",
                      "brewer2mpl","winshell"])      
elif sys.argv[1] == '-remove':
    pass