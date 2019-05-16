# coding: utf8
'''
Created on 22.04.2014

@author: chm
'''
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
#from numba import jit
 
from jsonschema import validate
from .calibrationhelper import *
"""
Module ...
"""
class calibration:
    """
    This class represents a calibration for SAXS diffraction. 
    After initialization, the :py:meth:`integrate` method can compute the radial intensity very fast.
    
    :param dict config: the calibration json object as dictionary :ref:`root`:
    :param dict mask: The mask of the list to use for this instance
    :param dict attachment: If mask is not to be read from filesystem it must be provided as attachment
    """
    
    def __init__(self,config,mask=None,attachment=None):
        
        if isinstance(config, str):
            #open config and check schema
            caldict=json.load(open(config))
        elif  isinstance(config, dict):
            caldict=config
           
        else:
            print("calibrarion takes a config object as path or dictionary")
            raise TypeError (config)
        schemapath=os.path.dirname(__file__)+'/schema.json'
       
        schema=(json.load(open(schemapath)))
        validate(caldict, schema)
        #calculate a hash for all configdata
  
        self.config=caldict
        if not mask:
            mask=caldict["Masks"][0]
        self.maskconfig=mask
    
        self._setupcalibration(mask, attachment)
        self.kind="Radial"
 
    def __complexCoordinatesOfPicture(self, oversampling):
        """
        Generates array containing coordinates relative to beam center as complex numbers. 
        This is used to calculate the angles
        
        :param obj config:
        :param int oversampling:
        """
        imagesize=self.config["Geometry"]['Imagesize']
        beamcenter=self.config["Geometry"]['BeamCenter']
        return cplwcener(imagesize, beamcenter, oversampling)
        
    def polcorr(self, Pfrac, rot):
        """
        Polarization Correction
        """
        complexp=self.__complexCoordinatesOfPicture(1)
        pixelsize=self.config["Geometry"]['PixelSizeMicroM'][0]*1e-3 #
        r=(np.absolute(complexp))*pixelsize
        phi=np.angle(complexp)
        
        d=self.config["Geometry"]['DedectorDistanceMM']
        tilt=self.config["Geometry"]['Tilt']['TiltAngleDeg']/180.0*np.pi
        tiltdir=self.config["Geometry"]['Tilt']['TiltRotDeg']/180.0*np.pi
        
        theta=calc_theta(r, phi, d, tilt, tiltdir)
        corr=(Pfrac*(1.0 -np.square(np.sin(phi-rot)*np.sin(theta)))+
            (1.0-Pfrac)*(1.0-np.square(np.cos(phi-rot)*np.sin(theta))))
       
        return corr

    def _setupcalibration(self, mask, attachment):
        """
        Pre-calculate the data for the integration. This is done at initialization.
        """
        
       
        # Calculate array of size img with the distance from center as entries
        pixelsize=self.config["Geometry"]['PixelSizeMicroM'][0]*1e-3 #all length in millimeters
        oversampling=mask['Oversampling']
        complexp=self.__complexCoordinatesOfPicture(oversampling)
        r=np.absolute(complexp)*pixelsize
        phi=np.angle(complexp)

        d=self.config["Geometry"]['DedectorDistanceMM']
        tilt=self.config["Geometry"]['Tilt']['TiltAngleDeg']/180.0*np.pi
        tiltdir=self.config["Geometry"]['Tilt']['TiltRotDeg']/180.0*np.pi
        theta=calc_theta(r, phi, d, tilt, tiltdir)
        self.corr=np.ones((self.config["Geometry"]['Imagesize'][0], self.config["Geometry"]['Imagesize'][1]))
        if 'PolarizationCorrection' in self.config:
            frac = self.config["PolarizationCorrection"]
             #Nanometer
            self.corr=np.divide(self.corr, self.polcorr(frac['Fraction'], frac['Angle']/180.0*np.pi-np.pi/2))
        # rescale the theta that the radial regions connected to a label are about 1 pixel wide
        Angstrom=1.00001495e-1
        qpix =4*np.pi*np.sin(theta/2)/self.config['Wavelength']/Angstrom
        if 'PixelPerRadialElement' in mask:
            self.scale=1/np.max(qpix)*np.max(r)/pixelsize/mask['PixelPerRadialElement']
        else:
            pixelper=1.0
            self.scale=1/np.max(qpix)*np.max(r)/pixelsize
        
        # Check if Phimode is active
        if self.maskconfig["Phi-mode"]:
            self.scale=1/np.max(phi)*np.max(r)/mask['PixelPerRadialElement']
            labels=np.array((phi+np.pi)*self.scale, dtype=int)
        else:
            labels=np.array(qpix*self.scale, dtype=int)
        
        # print("Let's see if we can create a calibration")    
        self.maxlabel=np.max(labels)
        mask=openmask(mask["MaskFile"], attachment)
            
        
        if self.maskconfig["Phi-mode"]:
            complexp_q=self.__complexCoordinatesOfPicture(1)
            r_q=np.absolute(complexp_q)*pixelsize
            phi_q=np.angle(complexp_q)
            theta_q=calc_theta(r_q, phi_q, d, tilt, tiltdir)
            Angstrom=1.00001495e-1
            nqpix =4*np.pi*np.sin(theta_q/2)/self.config['Wavelength']/Angstrom
            masky = np.ones((self.config["Geometry"]['Imagesize'][0], self.config["Geometry"]['Imagesize'][1]), dtype=bool)
            masky[np.logical_not(mask)]=0
            masky[(nqpix<self.maskconfig["qStart"])]=0
            masky[(nqpix>self.maskconfig["qStop"])]=0
            mask = masky
            
        self.A=labelstosparse(labels, mask, oversampling)
        self.ITransposed =self.A
        self.I, self.Areas, self.oneoverA=rescaleI(self.A, self.corr)
        
        if self.maskconfig["Phi-mode"]:
            self.qgrid=(np.arange(self.maxlabel+1)+0.5)/self.scale-np.pi  
        else:
            self.qgrid=(np.arange(self.maxlabel+1)+0.5)/self.scale   
       
    
    def integrate(self, image):
        """
        Integrate a picture.
        
        :param numpy.array(dim=2) image: Sensor image to integrate as 2d `NumPy` array 
        :returns: Returns Angle and intensity vector as a tuple (angle,intensity)
        """
        return  (self.qgrid, self.I.dot(image.flatten() ))
    def integratechi(self, image, path, picture):
        """
        Integrate and save to file in "chi" format.
        
        :param np.array() image: Image to integrate as numpy array
        :param string path: Path to save the file to
        :returns: Scattering curve data as numpy array 
        """
        r= self.I.dot(image.flatten() )
     
        data=np.array([self.qgrid[len (self.qgrid)-len(r):],
                        r, 
                        np.sqrt(r*self.Areas) *self.oneoverA] # Poisson Error sclaed
                      ).transpose()
        
        if self.maskconfig["Phi-mode"]:
            I0=0
            I1=0
            I2=0
            collabels=[
                        "Phi Angle [rad]",
                        "Intensity (Count/Pixel)",
                        "Error Margin"]
            integparam={"I0":I0, "I1":I1, "I2":I2}
            headerstr= json.dumps(self.config)+"\n"
            headerstr+=json.dumps(integparam)+"\n"
            headerstr+=json.dumps(collabels)+"\n"
            headerstr+="   "+str(data.shape[0])+""
        else:
            I0, I1, I2 = self.integParameters(r)
            collabels=[
                        "Scattering Vector  q [$nm^{-1}$]",
                        "Intensity (Count/Pixel)",
                        "Error Margin"]
            integparam={"I0":I0, "I1":I1, "I2":I2}
            headerstr= json.dumps(self.config)+"\n"
            headerstr+=json.dumps(integparam)+"\n"
            headerstr+=json.dumps(collabels)+"\n"
            headerstr+="   "+str(data.shape[0])+""
        
        
        if path != "xxx":#if working in GISAXSmode, the data is not saved
            np.savetxt(path, data, fmt='%.18e', delimiter=' ', newline='\n ', header=headerstr, footer='', comments='')
        
       
        return {"array":data.transpose().tolist(),
                    "columnLabels":collabels,
                    "kind":"Radial",
                    "conf":self.config,
                    "mask":self.maskconfig,
                    "Integparam":integparam
        }
         
   
    def integrateerror(self, image):
        """
        Integrates an image and computes error estimates.
        
        :param np.array() image: Image to integrate as numpy array
        :returns: The intensity the standard deviation and the Poisson statistics error in a numpy array.
        """
        radial=self.I.dot(image.flatten()) 
        means=self.ITransposed.dot(radial*self.Areas)
        dev=np.square(image.flatten()-means)
        stddev=np.sqrt(self.I.dot(dev))
        poissonerr=np.sqrt(radial*self.Areas)*self.oneoverA
        rsq=(2*np.sin(self.qgrid)*self.config["Geometry"]['DedectorDistanceMM']
             *np.pi*self.config["Geometry"]['PixelSizeMicroM'][0]*1e-3**2)
        return  np.array([radial, stddev, poissonerr])
    
    def plot(self,image,outputfile="",startplotat=0 ,fig=None):
        """
        Plot integrated function for image in argument.
        
        :param numpy.array(dim=2) image: Sensor image to integrate as 2d `NumPy` array
        :param string outputfile: File to write plot to. Might be any image format supported by matplotlib.
        :param integer startplotat: radial point from which to start the plot
        """
        ## Do not use that in a multithread environment!!
        #if active_count()>0:
       
            
                    
        fun=self.integrateerror(image)
       
        nonzero=fun[0]>0
        #print "error:" ,np.sum(fun[1][nonzero])
        if not fig:fig=plt.figure()
        fig.clf()
        
        ax = fig.add_subplot(111)
        ax.fill_between( self.qgrid[nonzero], np.clip(fun[0][nonzero]-fun[1][nonzero], 1, 1.0e300), fun[0][nonzero]+fun[1][nonzero], facecolor='yellow', linewidth=0, alpha=0.5)
        ax.fill_between( self.qgrid[nonzero], np.clip(fun[0][nonzero]-fun[2][nonzero], 1, 1.0e300), fun[0][nonzero]+fun[2][nonzero], facecolor='blue', alpha=0.2, linewidth=0)
        ax.plot(self.qgrid[nonzero], fun[0][nonzero])
      
        
        plt.ylabel('Intensity [counts/pixel]')
        plt.xlabel('q [1/nm]')
        plt.yscale('log')
        plt.title(outputfile)
        
       
      
        if outputfile=="":   
               #.show()
               pass
        else:
               fig.savefig(outputfile)
         
        return fig
         
    def integParameters(self, Intensity):
        """
        function to calculate the integral parameters between qStart and qStop
        returns I0, I1, I2
        
        """        
        self.qgrid #numpy array
        qStop = self.maskconfig["qStop"]
        qStart = self.maskconfig["qStart"]
        if np.max(self.qgrid)<qStop:
            qStop=np.max(self.qgrid)
        qStopIndex = np.where(self.qgrid >= qStop)[0][0]
        if qStopIndex>np.size(Intensity):
            qStopIndex=np.size(Intensity)
        qStartIndex = np.where(self.qgrid >= qStart)[0][0]
        qDelta = self.qgrid[1]-self.qgrid[0]
        I0 = np.nansum(Intensity[qStartIndex:qStopIndex]) * qDelta
        I1 = np.nansum((Intensity[qStartIndex:qStopIndex] * self.qgrid[qStartIndex:qStopIndex])) * qDelta
        I2 = np.nansum((Intensity[qStartIndex:qStopIndex] 
              * self.qgrid[qStartIndex:qStopIndex] 
              * self.qgrid[qStartIndex:qStopIndex])) * qDelta
        return I0, I1, I2
