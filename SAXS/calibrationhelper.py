import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import scipy.sparse as sp
import json
import pickle
import hashlib, binascii
import os, sys
from threading import Thread, current_thread, active_count 
import io, base64    
"""
Necessary Helper Functions
"""
def cplwcener(imagesize, beamcenter, oversampling):
        return np.add.outer(
                         1j*(np.arange(0,
                                             imagesize[0],
                                             1./oversampling,
                                             dtype=np.float_)
                                   -imagesize[0]
                                   +beamcenter[0]+0.5/oversampling),
                        (np.arange(0,
                                             imagesize[1],
                                             1./oversampling,
                                             dtype=np.float_)
                                   - beamcenter[1]+0.5/oversampling)
                         )

def labelstosparse(labels, mask, oversampling):
        '''labels: numerates pixels of same radial distance'''
        ind=np.argsort(labels.flatten()).astype(int) #sorted indices to labeled pixels as array
        sortedl=labels.flatten()[ind] #labels as array sorted by indices
        '''at this point ind gives pixel number, sortedl the label for which integration ring the pixel is counted'''
        newcol=sortedl-np.roll(sortedl, 1)#0,1 matrix that is always zero and only one when the integration label is increased
        length=sortedl.shape[0]
        coli=np.array(np.where(newcol>0)[0])#gives the position in sortedl where the ring is changed
        coliptr= np.concatenate(([0], coli, [length])) #adds first and last point (0) and (length)
        m= sp.csc_matrix((np.ones(length), ind, coliptr))#sparse matrix representation of labels
        sc=scalemat(mask.shape[0], mask.shape[1], oversampling)
        
        A=sp.csc_matrix((sc.dot(m)))
        return sp.csc_matrix((A.data*mask.flatten()[A.indices], A.indices, A.indptr))

def rescaleI(sparse, corr):
        areas=sparse.transpose().dot(np.ones(sparse.shape[0]))
        #corect for sensor shape 
         
        oneoverA=np.where(areas>0, 1.0/areas, np.NAN)
        #calculate factors for area
        l=sparse.indptr
        b=np.roll(sparse.indptr, 1) # l-b is repeating count for each column
        #update sparse data
        data=sparse.data*np.repeat(oneoverA, (l-b)[1:])*corr.flatten()[sparse.indices] 
        sparse.data=data
        return sparse.transpose(), areas,  oneoverA
def calc_theta(r, phi, d, tilt, tiltdir):
        """
        Calculates the difraction angle from pixel coordinates. It does work when called with arrays. 
        See :ref:`geometry`
        
        :param float r: Distance to beamcenter.
        :param float phi: Angle[rad] from polar sensor plane coordinates.
        :param float d: distance to difraction center.
        :param float tilt: Angle[rad] of sensor plane tilt.
        :param float tiltdir: Angle[rad] of direction of tilt.
        :returns:  theta
        """
        alpha=np.arcsin(np.sin(tilt)*np.sin(phi+tiltdir+np.pi/2))
        lsquared=d**2 +r**2 -2*d*r*np.cos(np.pi/2+alpha)
        return np.arccos(-(r**2-lsquared-d**2)/(2*np.sqrt(lsquared)*d))
    
   
        
def scalemat(Xsize, Ysize, ov):
        """
        Computes a scaling projection for use in computing the pixel weights for integration
        
        :param int Xsize: Picture size in X direction.
        :param int Ysize: Picture size in Ydirection.
        :param int ov: Number of oversampling ticks in x ynd y direction
        :param array corr: Polarizationn an other correction factors
        :returns: sparce matrix doing the scaling
        """
    
        cell=np.add.outer(np.arange(ov)*Ysize*ov, np.arange(ov))
        grid=np.add.outer(np.arange(0, Xsize*Ysize*ov*ov, Ysize*ov*ov), np.arange(0, Ysize*ov, ov))
        cindices=np.add.outer(grid, cell).flatten().astype(int)
        return sp.csr_matrix((np.ones(len(cindices))/ov**2,
                     cindices,
                     np.arange(0, Ysize*Xsize*ov**2+1, ov*ov, dtype=int)),
                    dtype=np.float, shape=(Ysize*Xsize, Ysize*Xsize*ov**2))

def openmask(mfile,attachment=None):
        """
        Open the mask file especialy the \*.msk file. Unfortunately there is no library
        module for msk files available also no documentation. So, for the msk file, we have a very brittle hack
        it works for our sensor. Nevermind any other resolution or size.
        
        :param object config: Calibration config object.
        :returns: Mask as logical numpy array.
        """
        if attachment:
            #mfilestream=base64.b64decode(attachment['data']).decode('cp1252','ignore')
            mfilestream=attachment['data']
            fin=io.BytesIO(mfilestream.encode('latin-1','ignore'))
            #was 'cp1252' codec
            print("Now we open attached mask!")
        else:
            mfilestream=open(mfile,encoding='latin-1').read()
            fin=open(mfile, "rb")
            print("Now we open local mask!")
        if mfile.endswith('.msk'):
            import bitarray
            maskb=bitarray.bitarray(endian='little')
            maskb.frombytes(mfilestream.encode('latin-1','ignore')) 
            maskl=np.array(maskb.tolist())
            
            import struct
            fin.seek(0x10)
            (y,)= struct.unpack('i', fin.read(4))
            fin.seek(0x14)
            x,=struct.unpack('i', fin.read(4))
            word=32
            padding= word - y % word
            yb=y+padding
            off=np.size(maskl)-yb*x
            off=8192
            
            try:
                mask=maskl[off:x*yb+off].reshape(x,yb)
            except:
                mask=maskl[off:x*yb+off].reshape(x,y)
            #misc.imsave("mask.png",mask)
            cropedmask=np.flipud(mask[0:x, 0:y])
            # save the mask in order to check if it worked
            #misc.imsave("cropedmask.png",cropedmask)
            print("Success!")
            return np.logical_not(cropedmask)

        else:
            if attachment:
                mask= np.where(misc.imread(mfilestream)!=0, False, True)
            else:
                mask= np.where(misc.imread(mfile)!=0, False, True)
           
            return mask    
