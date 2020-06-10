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

                         CLASS CREATE_VERTICAL
                        ----------------------

    Here the Vertical tail geometry is created.

   sref           --> vertical area                          [m2]  [real]   
   ar             --> vertical aspec ratio                    [-]  [real]   
   sweep14        --> vertical sweep 1/4 chors              [deg]  [real]   
   taper          --> vertical Croot/Ctip                     [-]  [real]   
   th_root        --> root thickness                          [-]  [real]   
   th_tip         --> tip thickness                           [-]  [real]   
   appex_14croot  --> appex at 1/4 of the VT_Croot            [m]  [real]   

"""
import numpy as np
from Auxilliary.class_aux import AuxTools
from ..Parameterization.parameterization_2d_profile import Bezier

#----------------------------------------------------------------------#
#                         HORIZONTAL CLASS                             #
#----------------------------------------------------------------------#
class Create_Vertical(object, metaclass=AuxTools):
    """
        Aircraft Components:  Vertical Tail
    """
    
    def __init__(self, geo,*args, **kwargs):
        super(Create_Vertical, self).__init__(geo,*args, **kwargs)

        if 'Fvertical' not in kwargs:
            raise ValueError("Cannot initiate Vertical...provide the \
                              argument Fvertical = 'file_name'.")            
        self.file_name = kwargs['Fvertical'] 
        
# Data for the wing...some setup to avoid crashing

        self.geo['vert']                       = {}  
        self.geo['vert']['sref']               =  25.570
        self.geo['vert']['ar']                 =   5.580
        self.geo['vert']['sweep14']            =  30.200
        self.geo['vert']['taper']              =   0.260
        self.geo['vert']['th_root']            =   0.120
        self.geo['vert']['th_tip']             =   0.120
        self.geo['vert']['appex_14croot']      =  29.530   
        self.geo['vert']['profiles']           =  1
        self.geo['vert']['parameterization']   =  'bezier'   
        self.geo['vert']['bezier_cp']          =  '.\Input_Files\Bezier_VT.inp'   
        self.geo['vert']['output_profile']     =  '.\Output_Files\airfoil.dat'         
        
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
            for key in (self.geo['vert']):
                if str(vvars[i].strip()) == str(key.strip()):
                    if (key == 'parameterization' or key == 'bezier_cp'  or   \
                        key == 'output_profile'):
                        self.geo['vert'][key] = vvals[i]
                    else:
                        self.geo['vert'][key] = float(vvals[i])
                        
    pass

#----------------------------------------------------------------------#
#                    Computing the Reference Wing                      #
#----------------------------------------------------------------------#
    def Vert_Planform(self):
        """ The wing_ref method computes the reference wing given a certain
            geometrical input provided by the user. The method is available
            for objects from the class CREATE_VERTICAL. The method adds to 
            the object a set of dictionaries containing important gemetrical 
            values.
        """
        
        pi    = np.arccos(-1.0)
#
#---- Initial definitions...

        self.geo['vert']['span']  = np.sqrt(self.geo['vert']['sref'] *        \
                                            self.geo['vert']['ar'])
        
        self.geo['vert']['croot'] = 2.0 * self.geo['vert']['sref']   /        \
                                         (self.geo['vert']['span']   *        \
                                         (1.0+self.geo['vert']['taper']))
                                         
        self.geo['vert']['ctip']  = self.geo['vert']['croot'] *               \
                                    self.geo['vert']['taper']
                                    
        self.geo['vert']['appex'] = self.geo['vert']['appex_14croot'] -       \
                                    self.geo['vert']['croot']*0.25

#
#---- Definition of the Z stations along the span...

        self.geo['vert']['z']      = list()
        z                          = np.zeros(2)
        z[0]                       = 0.0
        z[1]                       = self.geo['vert']['span'] 

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,2):
            self.geo['vert']['z'].append(str(z[i]))

#
#---- Definition of the Chords along the span...

        self.geo['vert']['chords'] = list()
        chords                     = np.zeros(2)
        chords[0]                  = self.geo['vert']['croot']
        chords[1]                  = self.geo['vert']['ctip']

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,2):
            self.geo['vert']['chords'].append(str(chords[i]))

#
#---- Definition of the X along the span...
        self.geo['vert']['x']      = list()
        x                          = np.zeros(2)
        x[0]                       = 0.0
        x[1]                       = x[0] + self.geo['vert']['span']    *     \
                                     np.tan(self.geo['vert']['sweep14'] *     \
                                     pi/180.0) + (self.geo['vert']['croot'] / \
                                     4.0) - (self.geo['vert']['ctip']/4.0)
#
#---- Adding the XAPPEX...
        x[0]                       = x[0] + self.geo['vert']['appex_14croot']
        x[1]                       = x[1] + self.geo['vert']['appex_14croot']
        
#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,2):
            self.geo['vert']['x'].append(str(x[i]))

#
#---- Definition of the XTE along the span...
        self.geo['vert']['xte']    = list()
        xte                        = np.zeros(2)
        xte[0]                     = x[0] + chords[0]
        xte[1]                     = x[1] + chords[1]

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,2):
            self.geo['vert']['xte'].append(str(xte[i]))

#
#---- Definition of the t/c along the span...
        self.geo['vert']['tc']      = list()
        self.geo['vert']['t']       = list()        
        tc                          = np.zeros(2)
        t                           = np.zeros(2)        

        tc[0]                       = self.geo['vert']['th_root']
        tc[1]                       = self.geo['vert']['th_tip'] 

        t[0]                        = chords[0] * tc[0]
        t[1]                        = chords[1] * tc[1] 

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,2):
            self.geo['vert']['tc'].append(str(tc[i]))
            self.geo['vert']['t'].append(str(t[i]))                    
        
#--- CMA, ZMA, SweepLE
        self.geo['vert']['cma']     = self.geo['vert']['croot'] * (2.0/3.0) * \
                                      (np.power(self.geo['vert']['taper'],2)+ \
                                       self.geo['vert']['taper']+1.0) /       \
                                      (self.geo['vert']['taper']+1.0)

        self.geo['vert']['zcma']    = z[0] + (self.geo['vert']['cma']  -      \
                                      chords[0])/(chords[1]-chords[0]) *      \
                                       (z[1]-z[0])
                                       
        self.geo['vert']['xcma']    = self.geo['vert']['appex']      +        \
                                     (self.geo['vert']['zcma']-z[0]) /        \
                                     (z[1]-z[0]) * (x[1]-x[0])

        self.geo['vert']['sweeple'] = np.arctan((x[1]-x[0])/(z[1]-z[0]))*     \
                                      180.0/pi
                                      
        self.geo['vert']['sweepte'] = np.arctan((xte[1]-xte[0]) /             \
                                      (z[1]-z[0]))*180.0/pi   
                
        self.geo['vert']['swet'] = (self.geo['vert']['span']/2.0)*            \
                                   chords[0]*((1.0+self.geo['vert']['taper'])*\
                          (2.0+9.0*np.power(self.geo['vert']['th_tip'],2.0)) +\
                          (6.0*np.power(self.geo['vert']['th_tip'],2.0))     *\
                          (self.geo['vert']['th_root'] /                      \
                           self.geo['vert']['th_tip']-1.0) *                  \
                          (1.0+2.0*self.geo['vert']['taper']))
#
#---- Average t/c ....

        self.geo['vert']['tcave'] = tc[1] - ((z[1]-self.geo['vert']['zcma'])/ \
                                    (z[1]-z[0]))*(tc[1]-tc[0])
#
#---- Printing data
        if self.screen_flag == True:
            print('  |-------------------------------------------------|')
            print('  |           Reference Vertical Tail               |')
            print('  |-------------------------------------------------|')
            print('   Sref          [m2]   --> ' + "{0:.3f}".format(          \
                                                     self.geo['vert']['sref']))
            
            print('   AR            [-]    --> ' + "{0:.3f}".format(          \
                                                       self.geo['vert']['ar']))
            
            print('   Vert_CMA      [m]    --> ' + "{0:.3f}".format(          \
                                                      self.geo['vert']['cma']))
            
            print('   Vert_XCMA     [m]    --> ' + "{0:.3f}".format(          \
                                                     self.geo['vert']['xcma']))
            
            print('   Vert_ZCMA     [m]    --> ' + "{0:.3f}".format(          \
                                                     self.geo['vert']['zcma']))        
            
            print('   Sweep1/4      [deg]  --> ' + "{0:.3f}".format(          \
                                                  self.geo['vert']['sweep14']))
            
            print('   Sweep_LE      [deg]  --> ' + "{0:.3f}".format(          \
                                                  self.geo['vert']['sweeple']))
            
            print('   Sweep_TE      [deg]  --> ' + "{0:.3f}".format(          \
                                                  self.geo['vert']['sweepte']))
            
            print('   Swet          [deg]  --> ' + "{0:.3f}".format(          \
                                                     self.geo['vert']['swet']))        
            
            print('   Taper         [-]    --> ' + "{0:.3f}".format(          \
                                                    self.geo['vert']['taper']))
            
            print('   t/c_Root      [-]    --> ' + "{0:.3f}".format(          \
                                                  self.geo['vert']['th_root']))
            
            print('   t/c_Tip       [-]    --> ' + "{0:.3f}".format(          \
                                                   self.geo['vert']['th_tip']))
            
            print('   Span          [m]    --> ' + "{0:.3f}".format(          \
                                                     self.geo['vert']['span']))
            
            print('   Croot         [m]    --> ' + "{0:.3f}".format(          \
                                                    self.geo['vert']['croot']))
            
            print('   Ctip          [m]    --> ' + "{0:.3f}".format(          \
                                                     self.geo['vert']['ctip']))
            
            print('                                                          ')    

#---
#
#       BEZIER (INPUT_FILE, OUTPUT_FILE, NO_STATIONS)
#       Generating the Vertical Tail Profile...
#
#---        
        Bezier(self.geo['vert']['bezier_cp'].strip(),                         \
               self.geo['vert']['output_profile'].strip(),                    \
               self.geo['vert']['profiles'])

    pass

      
