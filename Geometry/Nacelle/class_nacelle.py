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

                         CLASS CREATE_NACELLE
                        ----------------------

    Here the Nacelle geometry is created.

   type  --> nacelle type: (1) short / (2) long  [-]   [integer]      
   no    --> number of engines                   [-]   [integer]      
   dfan  --> nacelle fan diameter               [in]      [real]      
   lmax  --> nacelle length                     [in]      [real]      
   tc    --> nacelle rel. thickness              [-]      [real]       

"""
from Auxilliary.class_aux import AuxTools
from Auxilliary.UnitConvertions import Units
import numpy as np

#----------------------------------------------------------------------#
#                     NACELLE CREATE CLASS                             #
#----------------------------------------------------------------------#
class Create_Nacelle(object, metaclass=AuxTools):
    """
        Nacelle component...
    """
        
    def __init__(self, geo,*args, **kwargs):
        super(Create_Nacelle, self).__init__(geo,*args, **kwargs)

        if 'Fnacelle' not in kwargs:
            raise ValueError("Cannot initiate Nacelle...provide the \
                              argument Fnacelle = 'file_name'.")            
        self.file_name = kwargs['Fnacelle'] 
        
# Data for the wing...some setup to avoid crashing

        self.geo['nacelle']          = {}  
        self.geo['nacelle']['type']  =    1
        self.geo['nacelle']['no']    =    2
        self.geo['nacelle']['dfan']  =   69.800 * Units('inch','meters')
        self.geo['nacelle']['lmax']  =  136.000 * Units('inch','meters')
        self.geo['nacelle']['tc']    =    0.080

        vvars = list()
        vvals = list()

#    # Input file for the wing...
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
            for key in (self.geo['nacelle']):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.geo['nacelle'][key] = float(vvals[i])
   
#------------------------------------------------------------------------------
    def Nacelle(self):

# inches to meters...
        dfan  = self.geo['nacelle']['dfan'] * Units('inch','meters')
        lmax  = self.geo['nacelle']['lmax'] * Units('inch','meters')

        if self.geo['nacelle']['type'] == 1 :
            nac_dav = 1.30 * dfan
            self.geo['nacelle']['swet'] = np.pi * nac_dav * lmax * 1.10                
        else:
             nac_dav   = 1.35 * dfan
             self.geo['nacelle']['swet'] = np.pi * nac_dav * lmax * 1.10 

# I am doing this because in case I enter many times in this method I can keep
# scalling the nacelle many times...

        self.geo['nacelle']['dfan'] = dfan
        self.geo['nacelle']['lmax'] = lmax
#----------------------------------------------------------------------#
#                 Print the Nacelle Component                          #
#----------------------------------------------------------------------#    
    def Print_Nacelle(self):
        print(' ')
        print('  |-------------------------------------------------|')
        print('  |               Nacelle Geometry                  |')
        print('  |-------------------------------------------------|')
        print('   Type          [-]    --> ' + "{0:.3f}".format(          \
                                                  self.geo['nacelle']['type']))
        print('   Number        [-]    --> ' + "{0:.3f}".format(          \
                                                    self.geo['nacelle']['no']))

        print('   Diameter      [m]    --> ' + "{0:.3f}".format(          \
                                                  self.geo['nacelle']['dfan']))
        print('   Length        [m]    --> ' + "{0:.3f}".format(          \
                                                  self.geo['nacelle']['lmax']))
        print('   T/C           [-]    --> ' + "{0:.3f}".format(          \
                                                    self.geo['nacelle']['tc'])) 
                
        print('   Swet         [m2]    --> ' + "{0:.3f}".format(          \
                                                  self.geo['nacelle']['swet'])) 
        
