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

                         CLASS CREATE_PYLON
                        ----------------------

    Here the Pylon geometry is created.

   nac_type        --> nacelle type: (1)short / (2)long  [-] [integer]  
   croot           --> pylon root chord                  [m]    [real]  
   ctip            --> pylon tip chord                   [m]    [real]  
   len             --> pylon length                      [m]    [real]  
   sweep           --> pylon sweep angle               [deg]    [real]  
   tc              --> pylon relative thickness          [m]    [real]      



"""
from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                     NACELLE PYLON CLASS                              #
#----------------------------------------------------------------------#
class Create_Pylon(object, metaclass=AuxTools):
    """
        Nacelle component...
    """
        
    def __init__(self, geo,*args, **kwargs):
        super(Create_Pylon, self).__init__(geo,*args, **kwargs)

        if 'Fpylon' not in kwargs:
            raise ValueError("Cannot initiate Pylon...provide the \
                              argument Fnacelle = 'file_name'.")            
        self.file_name = kwargs['Fpylon'] 
        
# Data for the wing...some setup to avoid crashing

        self.geo['pylon']            = {}  
        self.geo['pylon']['type']    =   1
        self.geo['pylon']['croot']   =   5.3953
        self.geo['pylon']['ctip']    =   4.3090
        self.geo['pylon']['len']     =   0.5144
        self.geo['pylon']['sweep']   = -84.6000
        self.geo['pylon']['tc']      =   0.1020

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
            for key in (self.geo['pylon']):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.geo['pylon'][key] = float(vvals[i])
   

        pass
#------------------------------------------------------------------------------
    def Pylon(self):
        
        self.geo['pylon']['pyl_cma']  =  (self.geo['pylon']['croot']  +       \
                                         self.geo['pylon']['ctip']) * 0.50

        if self.geo['nacelle']['type'] == 1:
            self.geo['pylon']['swet'] = 2.0 * self.geo['pylon']['len'] *     \
                                         2.0 * self.geo['pylon']['pyl_cma']
        else:
            self.geo['pylon']['swet'] = self.geo['pylon']['len'] *           \
                                         2.0 * self.geo['pylon']['pyl_cma']                     


#------------------------------------------------------------------------------
    def Print_Pylon(self):
        print('  |-------------------------------------------------|')
        print('  |               Pylon Geometry                    |')
        print('  |-------------------------------------------------|')
        print('   Croot         [m]    --> ' + "{0:.3f}".format(          \
                                                   self.geo['pylon']['croot']))
        print('   Ctip          [m]    --> ' + "{0:.3f}".format(          \
                                                    self.geo['pylon']['ctip']))

        print('   Length        [m]    --> ' + "{0:.3f}".format(          \
                                                     self.geo['pylon']['len']))
        print('   Sweep       [deg]    --> ' + "{0:.3f}".format(          \
                                                   self.geo['pylon']['sweep']))
        print('   T/C           [-]    --> ' + "{0:.3f}".format(          \
                                                      self.geo['pylon']['tc']))
        print('   CMA           [m]    --> ' + "{0:.3f}".format(          \
                                                 self.geo['pylon']['pyl_cma']))
        print('   SWET         [m2]    --> ' + "{0:.3f}".format(          \
                                                   self.geo['pylon']['swet']))     
