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

                         CLASS CREATE_FUSELAGE
                        ----------------------

    Here the some basic infomration for the Fuselage geometry is created.
 
"""

import numpy as np
from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                         FUSELAGE CLASS                               #
#----------------------------------------------------------------------#
class Create_Fuselage(object, metaclass=AuxTools):
    """
        Aircraft Components:  FUSELAGE
    """
    
    def __init__(self, geo,*args, **kwargs):
        super(Create_Fuselage, self).__init__(geo,*args, **kwargs)

        if 'Fhorz' not in kwargs:
            raise ValueError("Cannot initiate Create_Fuselage...provide the   \
                              argument Fhorz = 'file_name'.")            
        self.file_name = kwargs['Fus']
        
# Data for the wing...some setup to avoid crashing

        self.geo['fus']                        = {}  
        self.geo['fus']['abreast']             =   4
        self.geo['fus']['nose']                =  12.000
        self.geo['fus']['pitch']               =  0.700
        self.geo['fus']['cone']                =  9.000
        self.geo['fus']['diameter']            =  3.500
        self.geo['fus']['seat_cushion_width']  =  0.470  
        self.geo['fus']['seat_arm_width']      =  0.050  
        self.geo['fus']['aisle_width']         =  0.400  
        self.geo['fus']['dlength']             =  2.000  
        self.geo['fus']['lnose_dfus_min']      =  1.50   
        self.geo['fus']['lnose_dfus_max']      =  2.20   
        self.geo['fus']['ltail_dfus_min']      =  2.50   
        self.geo['fus']['ltail_dfus_max']      =  3.20   
        
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
            for key in (self.geo['fus']):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.geo['fus'][key] = float(vvals[i])

    pass

#----------------------------------------------------------------------#
#                 Computing Fuselage Component                         #
#----------------------------------------------------------------------#
    def Fus_Torenbeek(self):

        pi    = np.arccos(-1.0)

        self.geo['fus']['fus_dia'] = self.geo['fus']['abreast']             * \
                                    (2*self.geo['fus']['seat_arm_width']    + \
                                    self.geo['fus']['seat_cushion_width'])  + \
                                     self.geo['fus']['aisle_width']
                                     
        self.geo['fus']['diameter'] = self.geo['fus']['fus_dia']
#        
        self.geo['fus']['lnose_min'] = self.geo['fus']['lnose_dfus_min']    * \
                                       self.geo['fus']['diameter']
#                                       
        self.geo['fus']['lnose_max'] = self.geo['fus']['lnose_dfus_max']    * \
                                       self.geo['fus']['diameter']
#                                       
        self.geo['fus']['ltail_min'] = self.geo['fus']['ltail_dfus_min']    * \
                                       self.geo['fus']['diameter']
#                                       
        self.geo['fus']['ltail_max'] = self.geo['fus']['ltail_dfus_max']    * \
                                        self.geo['fus']['diameter']
#                                        
        self.geo['fus']['fus_length_min'] = (self.operating['no_pass']      / \
                                             self.geo['fus']['abreast'])    * \
                                             self.geo['fus']['pitch']       + \
                                             self.geo['fus']['lnose_min']   + \
                                             self.geo['fus']['ltail_min']   + \
                                             self.geo['fus']['dlength']
                                             
#ap        self.geo['fus']['fus_length_max'] = (self.geo['fus']['no_pass']    /  \
#ap                                             self.geo['fus']['abreast'])   *  \
#ap                                             self.geo['fus']['pitch']      +  \
#ap                                             self.geo['fus']['lnose_max']  +  \
#ap                                             self.geo['fus']['ltail_max']  +  \
#ap                                             self.geo['fus']['dlength'] 

        self.geo['fus']['fus_length_max']   = (self.operating['no_pass']    / \
                                               self.geo['fus']['abreast'])  * \
                                               self.geo['fus']['pitch']     + \
                                               self.geo['fus']['lnose_max'] + \
                                               self.geo['fus']['ltail_max'] + \
                                               self.geo['fus']['dlength'] 
#
        self.geo['fus']['fus_length']=0.5*(self.geo['fus']['fus_length_min']+ \
                                           self.geo['fus']['fus_length_max'])
#        
        self.geo['fus']['esb'] = self.geo['fus']['fus_length']              / \
                                 self.geo['fus']['diameter']
#
        self.geo['fus']['swet'] = pi * self.geo['fus']['diameter']          * \
                                       self.geo['fus']['fus_length']        * \
                              ((1.0-2.0/self.geo['fus']['esb'])**(2.0/3.0)) * \
                              (1.0+1.0/(self.geo['fus']['esb']              * \
                                        self.geo['fus']['esb']))

#ap        self.geo['fus']['central'] = int(self.geo['fus']['no_pass']    /      \
#ap                                         self.geo['fus']['abreast'])   *      \
#ap                                         self.geo['fus']['pitch']      +      \
#ap                                         self.geo['fus']['dlength']

        self.geo['fus']['central'] = int(self.operating['no_pass']         /  \
                                         self.geo['fus']['abreast'])       *  \
                                         self.geo['fus']['pitch']          +  \
                                         self.geo['fus']['dlength']
                                         
        self.geo['fus']['vol'] = pi* 0.25 *                                   \
                                     (self.geo['fus']['diameter'])**2.0    *  \
                                      self.geo['fus']['fus_length']        *  \
                                      (1.0 - (2.0/self.geo['fus']['esb']))
#
#---- Printing data
        if self.screen_flag == True:
            print('  |-------------------------------------------------|')
            print('  |          Fuselage Geometric Parameters          |')
            print('  |-------------------------------------------------|')
            print('   Fuselage Nose         [m]   --> ' + "{0:.3f}".          \
                                               format(self.geo['fus']['nose']))
            
            print('   Fuselage Pitch        [-]   --> ' + "{0:.3f}".          \
                                              format(self.geo['fus']['pitch']))
            
            print('   Fuselage Cone         [-]   --> ' + "{0:.3f}".          \
                                               format(self.geo['fus']['cone']))
            
            print('   Fuselage Diameter     [m]   --> ' + "{0:.3f}".          \
                                           format(self.geo['fus']['diameter']))
            
            print('   Fuselage Abreast      [-]   --> ' + "{0:.3f}".          \
                                            format(self.geo['fus']['abreast']))
            
            print('   Fuselage Length       [m]   --> ' + "{0:.3f}".          \
                                         format(self.geo['fus']['fus_length']))
            
            print('   Fuselage Slenderness  [-]   --> ' + "{0:.3f}".          \
                                                format(self.geo['fus']['esb']))
            
            print('   Fuselage Swet         [m2]  --> ' + "{0:.3f}".          \
                                               format(self.geo['fus']['swet']))
            
            print('   Fuselage Volume       [m3]  --> ' + "{0:.3f}".          \
                                                format(self.geo['fus']['vol']))           
            
            print('                                                          ')
        
        pass
