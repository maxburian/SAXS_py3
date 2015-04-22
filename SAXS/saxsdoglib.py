
 
import json
from optparse import OptionParser
import os,sys
import time
import calibration
import imagequeuelib
def saxsdogparseopt():
    """
    handles commandline options for "saxsdog"
    """
    parser = OptionParser()
    usage = "usage: %prog [options] directory/to/watch"
    parser = OptionParser(usage,add_help_option=False)
    parser.add_option("-h", "--help", action="help", help="Show this help message and exit.")
    parser.add_option("-c", "--calibration", dest="calfilename",
                      help="Path to calibration file (JSON).", metavar="FILE",default="cal.json")
    parser.add_option("-t", "--threads",type="int", dest="threads",
                      help="Number of concurrent threads.",default=1)
    parser.add_option("-m", "--plotmonitor", dest="plotwindow", default=False, action="store_true",
                      help="Show a live updating plot window.")
    parser.add_option("-w", "--watch", dest="watchdir", default=False,action="store_true",
                      help="Watch directory for changes, using file system events recursively for all sub directories.")
    parser.add_option("-r", "--resume", dest="resume", default=False,action="store_true",
                      help="Skip files that are already converted.")
    parser.add_option("-o", "--out", dest="outdir", default="",
                      help="Specify output directory.")
    parser.add_option("-R", "--relpath", dest="relpath", default="../work",
                      help="Specify output directory as relative path to image file. Default: '../work'")
     
   
    parser.add_option("-s", "--svg", dest="writesvg",action="store_true",
                      help="Write plot to svg file.",default=False)
    parser.add_option("-p", "--png", dest="writepng",action="store_true",
                      help="Write png of original.",default=False)
    parser.add_option("-P","--profile",dest="profile",action="store_true",default=False,
                      help="Make a time Profile and print it.")
    parser.add_option("-S","--silent",dest="silent",default=False,action="store_true",
                      help="Less output.")
    parser.add_option("-n","--nowalk",dest="nowalk",default=False,action="store_true",
                      help="Don't scan for files already there, only watch file system if -w flag is given.")
    parser.add_option("-D","--walkdirinthreads",dest="walkdirinthreads",default=False,action="store_true",
                      help="Search all directories in parallel process.")
    parser.add_option("-V","--servermode",dest="servermode",default=False,action="store_true",
                      help="Servermode.")
        
     
    
    
    
    (options, args) = parser.parse_args(args=None, values=None)
     
    if len(args)!=1:
        parser.error("incorrect number of arguments")
        
    if options.watchdir:options.watch=True
    else: options.watch=False
    return (options, args)

 
def saxsdog():
    """
    This implements the functionality of :ref:`saxsdog`
    """
    (options, args)=saxsdogparseopt()
   
    if options.profile: 
        import cProfile, pstats, StringIO
        pr = cProfile.Profile()
    conf=json.load(open(options.calfilename,"r"))
    cals=[]
    directory=args[0]
    if "Masks" in conf:
        for mnumber,mask in enumerate(conf["Masks"]):
            cals.append(calibration.calibration(
                                           conf,
                                            mask,
                                             None))
    if "Slices" in   conf:
        for slice in conf["Slices"]:
            cals.append(GISAXSSlices.slice( conf,slice,None))
    imgq=imagequeuelib.imagequeue(cals,
                options,directory,None)
    if options.profile: 
        pr.enable()
    
    imgq.start()
    
    if options.profile:       
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print "#####################################"
        print '# Wrote profile to the file "prof". #'
        print '#####################################'
        open("prof","w").write(s.getvalue())
if __name__ == '__main__':
    saxsdog()
    