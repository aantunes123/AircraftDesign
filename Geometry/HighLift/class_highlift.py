# -*- coding: utf-8 -*-
"""
 
    Code   :  Aircraft Design (03/02/2017)                                              
    Created:  03/03/2017                                                        
    Licence:  GNU AGPLv3                                                        
                                                                             
    Permissions of this strongest copyleft license are conditioned             
    on making available complete source code of licensed works and             
    modifications, which include larger works using a licensed work,           
    under the same license. Copyright and license notices must be 
    preserved. Contributors provide an express grant of patent rights.
    When a modified version is used to provide a service over a 
    network, the complete source code of the modified version must 
    be made available.

                        SLATS/FLAPS INPUT 
                        ------------------
                                                                            
   slat_type           --> slat:  (0)no / (1)yes           [-] [integer]    
   flap_type           --> slat:  (1)single / (2)double    [-] [integer]    
   flap_yinb           --> flap inboard station            [%]    [real]    
   flap_yout           --> flap outboard station           [%]    [real]    
   flap_m_croot        --> chord main flap root            [%]    [real]    
   flap_a_croot        --> chord aft flap root             [%]    [real]    
   flap_m_ctip         --> chord main flap tip             [%]    [real]    
   flap_a_ctit         --> chord aft flap tit              [%]    [real]    
   flap_deflec         --> flap deflection               [deg]    [real]    

"""
import numpy as np
from scipy.optimize import fmin
from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                              HIGH LIFT                               #
#----------------------------------------------------------------------#
class Create_HighLift(object, metaclass=AuxTools):
    """
        Aircraft Components:  WING
    """
   
    def __init__(self, geo,*args, **kwargs):
        super(Create_HighLift, self).__init__(geo,*args, **kwargs)
        
        if 'Fhighlift' not in kwargs:
            raise ValueError("Cannot initiate Create_HighLift...provide the   \
                              argument Fhighlift = 'file_name'.")            
        self.file_name = kwargs['Fhighlift']     
        
# Data for the wing...some setup to avoid crashing

        self.geo['highlift']                 = {}
        self.geo['highlift']['flap']         = {}
        self.geo['highlift']['slat']         = {}

        self.geo['highlift']['slat_type']    =  1
        self.geo['highlift']['flap_type']    =  1
        self.geo['highlift']['flap_yinb']    = 0.120
        self.geo['highlift']['flap_yout']    = 0.750
        self.geo['highlift']['flap_m_croot'] = 0.180
        self.geo['highlift']['flap_a_croot'] = 0.080
        self.geo['highlift']['flap_m_ctip']  = 0.220
        self.geo['highlift']['flap_a_ctip']  = 0.080
        self.geo['highlift']['flap_takeoff'] = 15.0
        self.geo['highlift']['flap_landing'] = 38.0    

        vvars = list()
        vvals = list()
 
# Input file for the wing...
        f = open(self.file_name,'r')              
        for line in f:
            if(line[0] != '#' and line.isspace() == False):
                try:
                    vvars.append(line.strip().split('=')[0])
                    vvals.append(line.strip().split('=')[1])
                except:
                    pass
        f.close()
#
#--- Updating the variables...
        for i in range(0,len(vvars)):
            for key in (self.geo['highlift']):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.geo['highlift'][key] = float(vvals[i])

#------------------------------------------------------------------------------
    def Flaps_Slats(self):
        """
           Definition of the flap panels.
        
        
        """
# Defining the lists to store the flap geometrical data...
        self.geo['highlift']['flap']['y']     = []
        self.geo['highlift']['flap']['xte']   = []
        self.geo['highlift']['flap']['xle']   = []
        self.geo['highlift']['flap']['chord'] = []                

# Auxiliary vectors....        
        xte   = np.zeros(3)
        xle   = np.zeros(3)        
        chord = np.zeros(3)

# Auxiliary vectors for interpolation purpose...
        wing_y     = [float(item) for item in self.geo['Kink_wing']['y']]
        wing_xte   = [float(item) for item in self.geo['Kink_wing']['xte']]
        wing_chord = [float(item) for item in self.geo['Kink_wing']['chords']]        

#
# Wing Inboard panel        
        yinb = self.geo['highlift']['flap_yinb'] * self.geo['wing']['span']/ \
               2.0

# checking if the defined flap station is inside the fuselage...        
        if yinb < float(self.geo['Kink_wing']['y'][1]):
            yinb = float(self.geo['Kink_wing']['y'][1])
            print('Flap inboard definition inside the fuselage!')
            print('A new station was defined.')

        self.geo['highlift']['flap']['y'].append(yinb)
        
# Inboard flap station...
        if yinb >= float(self.geo['Kink_wing']['y'][1]) and \
           yinb < float(self.geo['Kink_wing']['y'][2]):
               xte[0]   = np.interp(yinb,wing_y,wing_xte)
               wchord   = np.interp(yinb,wing_y,wing_chord)

# Flap Single....               
               if self.geo['highlift']['flap_type'] == 1:
                   xle[0] = xte[0] - wchord *                                 \
                            self.geo['highlift']['flap_m_croot']
               else:
                   xle[0] = xte[0] - wchord *                                 \
                            (self.geo['highlift']['flap_m_croot']   +         \
                             self.geo['highlift']['flap_a_croot'])
# Flap chord..
               chord[0] = xte[0]-xle[0]
           
#
# Kink station
#
# I am assuming that the percentage of flap chord in the kink station is the 
# average of the root and tip percentage.
        ykink = float(self.geo['Kink_wing']['y'][2])

# Storing the flap Kink station...
        self.geo['highlift']['flap']['y'].append(ykink)
        
        if self.geo['highlift']['flap_type'] == 1:
               chord[1] = float(self.geo['Kink_wing']['chords'][2]) * 0.5 *   \
                          (self.geo['highlift']['flap_m_croot']           +   \
                           self.geo['highlift']['flap_m_ctip'])
        else:
               chord[1] = float(self.geo['Kink_wing']['chords'][2]) * 0.5 *   \
                          (self.geo['highlift']['flap_m_croot']           +   \
                           self.geo['highlift']['flap_a_croot']           +   \
                           self.geo['highlift']['flap_m_ctip']            +   \
                           self.geo['highlift']['flap_a_ctip'])

        xte[1] = float(self.geo['Kink_wing']['xte'][2])
        xle[1] = xte[1] - chord[1] 

#
# Wing Outboard panel
        yout = self.geo['highlift']['flap_yout'] * self.geo['wing']['span']/ \
               2.0
               
# HERE SHOULD COME THE AILERON STATION BASED ON THE AILERON VOLUME COMPUTATION
# THIS SHOULD BE IMPLEMENTED AS SOON AS POSSIBLE.....
# ALEXANDRE 18/07/2020...               
        if yout > (0.75* self.geo['wing']['span']/2.0):
            yout = 0.75* self.geo['wing']['span']/2.0
            print('Flap outboard definition is beyond the aileron station!')
            print('A new station was defined.')

# Storing the flap Kink station...
        self.geo['highlift']['flap']['y'].append(yout)
        
        xte[2]   = np.interp(yout,wing_y,wing_xte)
        wchord    = np.interp(yout,wing_y,wing_chord)               
               
# Flap Single....               
        if self.geo['highlift']['flap_type'] == 1:
            xle[2] = xte[2] - wchord *                                      \
                     self.geo['highlift']['flap_m_croot']
        else:
            xle[2] = xte[2] - wchord *                                      \
                     (self.geo['highlift']['flap_m_croot']   +                \
                      self.geo['highlift']['flap_a_croot'])

        chord[2] = xte[2] - xle[2]
                   
        for i in range(0,3):
            self.geo['highlift']['flap']['xte'].append(xte[i])
            self.geo['highlift']['flap']['xle'].append(xle[i])
            self.geo['highlift']['flap']['chord'].append(chord[i])
            
# Computing the flap area          

        self.geo['highlift']['flap']['area_inb'] =                            \
                          (float(self.geo['highlift']['flap']['y'][1])      - \
                           float(self.geo['highlift']['flap']['y'][0]))     * \
                          (float(self.geo['highlift']['flap']['chord'][0])  + \
                           float(self.geo['highlift']['flap']['chord'][1])) * \
                           0.5
                           
        self.geo['highlift']['flap']['area_out'] =                            \
                          (float(self.geo['highlift']['flap']['y'][2])      - \
                           float(self.geo['highlift']['flap']['y'][1]))     * \
                          (float(self.geo['highlift']['flap']['chord'][2])  + \
                           float(self.geo['highlift']['flap']['chord'][1])) * \
                           0.5
                         
                           