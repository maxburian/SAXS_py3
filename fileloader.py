from optparse import OptionParser
import sys
import numpy as np
import os

def main(argv):
    srcdir = ''
    outputfile = ''
    
    parser = OptionParser("usage: %prog <-d> srcdir <-o> outputfile")
    
    parser.add_option("-d", "--srcdir", dest="srcdir",
                  help="Path to directory for fileload")
    parser.add_option("-o", "--outfile", dest="outfile", default="fileloader_out",
                  help="Filename for output in numpy format")

    (opts, args) = parser.parse_args(args=None, values=None)
    
    #print opts
    
    if len(args)==0:
        args=["."]
    if opts.srcdir==None :
        print("No directory specified. Run -h flag!")
        sys.exit()
    
    srcdir = opts.srcdir
    outputfile = opts.outfile + ".txt"
    
    print(('The source directory is  "'+ srcdir+'"'))
    print(('The output filename is"'+ outputfile+'"'))


    '''Now, generate a list of all files'''
    filelist = np.empty([0, 1], dtype='string')
    for root, dirs, files in os.walk(srcdir):
        #..\\.\\110413_lechner\\
        dirs[:]=''
        for file in files:
            if file.endswith(".chi"):# and file.startswith("bi_cp_s"):
                filelist=np.vstack((filelist, os.path.join(root, file)))
                #print(os.path.join(root, file))
    
    phi = np.genfromtxt(filelist[0][0], usecols=(0), skip_header=4, dtype='float32')
    phi_oldsize=phi.size
    print(('Filelist was generated! Loading a total of ', filelist.size, 'files.'))
    
    '''Now read in the actual data'''
    imported_data = np.empty([filelist.size, phi.size])
    for i in range(filelist.size):
        try:
            imported_data[i,:]=np.genfromtxt(filelist[i][0], usecols=(1), skip_header=4, dtype='float32')
        except:
            print(("something went wrong in ", filelist[i][0]))
        if (i%(filelist.size/10)==0):
            print(("Loaded %d %%" % (float(i)/filelist.size *100.)))
            
    print(("We now imported a total of ", imported_data.shape[0], " files."))
    
    outfile =os.path.join(srcdir, outputfile)
    #outfile = srcdir + outputfile
    print(('The data is saved in "'+ outfile+'"'))
    np.savetxt(outfile, imported_data)
    print("Done!")
    

if __name__ == "__main__":
   main(sys.argv[1:])