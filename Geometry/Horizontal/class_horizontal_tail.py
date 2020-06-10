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

                         CLASS Create_Horizontal
                        ------------------------

    Here the Horizontal tail geometry is created.

   sref           --> horizontal area                 [m2]    [real]   
   ar             --> horizontal aspec ratio           [-]    [real]   
   sweep14        --> horizontal sweep 1/4 chors     [deg]    [real]   
   taper          --> horizontal Croot/Ctip            [-]    [real]   
   dihedral       --> self explanatory               [deg]    [real]   
   th_root        --> root thickness                   [-]    [real]   
   th_tip         --> tip thickness                    [-]    [real]   
   width_fus      --> fuselage width @ 1/4 Croot       [m]    [real]   
   appex_14croot  --> appex at 1/4 of the HT_Croot     [m]    [real]   

"""
import numpy as np
from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                         HORIZONTAL CLASS                             #
#----------------------------------------------------------------------#
class Create_Horizontal(object, metaclass=AuxTools):
    """
        Aircraft Components:  Horizontal Tail
    """
    
    def __init__(self, geo,*args, **kwargs):
        super(Create_Horizontal, self).__init__(geo,*args, **kwargs)

        if 'Fhorz' not in kwargs:
            raise ValueError("Cannot initiate Create_Horizontal...provide the \
                              argument Fhorz = 'file_name'.")            
        self.file_name = kwargs['Fhorz'] 
        
# Data for the wing...some setup to avoid crashing

        self.geo['horz']                    = {}  
        self.geo['horz']['sref']            =  25.570
        self.geo['horz']['ar']              =   5.580
        self.geo['horz']['sweep14']         =  30.200
        self.geo['horz']['taper']           =   0.260
        self.geo['horz']['dihedral']        =   8.000
        self.geo['horz']['th_root']         =   0.120
        self.geo['horz']['th_tip']          =   0.120
        self.geo['horz']['width_fus']       =   1.260
        self.geo['horz']['appex_14croot']   =  29.530   
        
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
            for key in (self.geo['horz']):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.geo['horz'][key] = float(vvals[i])
   
        pass

#----------------------------------------------------------------------#
#                    Computing the Reference Wing                      #
#----------------------------------------------------------------------#
    def Horz_Planform(self):
        """ The wing_ref method computes the reference wing given a certain
            geometrical input provided by the user. The method is available
            for objects from the class CREATE_HORIZONTAL. The method adds to 
            the object a set of dictionaries containing important gemetrical 
            values.
        """
#
#---- Initial definitions...

        self.geo['horz']['span']  = np.sqrt(self.geo['horz']['sref']   *      \
                                            self.geo['horz']['ar'])
        
        self.geo['horz']['croot'] = 2.0 * self.geo['horz']['sref']     /      \
                                         (self.geo['horz']['span']     *      \
                                         (1.0+self.geo['horz']['taper']))
                                         
        self.geo['horz']['ctip']  = self.geo['horz']['croot']          *      \
                                    self.geo['horz']['taper']
                                    
        self.geo['horz']['appex'] = self.geo['horz']['appex_14croot']  -      \
                                    self.geo['horz']['croot']*0.25

#
#---- Definition of the Y stations along the span...

        self.geo['horz']['y']      = list()
        y                          = np.zeros(3)
        y[0]                       = 0.0
        y[1]                       = self.geo['horz']['width_fus'] / 2.0
        y[2]                       = self.geo['horz']['span'] / 2.0

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,3):
            self.geo['horz']['y'].append(str(y[i]))

#
#---- Definition of the Chords along the span...

        self.geo['horz']['chords'] = list()
        chords                     = np.zeros(3)
        chords[0]                  = self.geo['horz']['croot']
        chords[2]                  = self.geo['horz']['ctip']
        chords[1]                  = chords[0] + (chords[2]-chords[0])  *     \
                                     ((y[1]-y[0])/(y[2]-y[0]))

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,3):
            self.geo['horz']['chords'].append(str(chords[i]))

#
#---- Definition of the X along the span...
        self.geo['horz']['x']      = list()
        x                          = np.zeros(3)
        
        x[0] = 0.0
        
        x[2] = x[0] - (self.geo['horz']['croot']/4.0) - (y[2]-y[0])        *  \
                     np.tan(self.geo['horz']['sweep14']*np.pi/180.0)       +  \
                           (self.geo['horz']['ctip']/4.0)
                           
        x[1] = x[0] + (x[2]-x[0])*((y[1]-y[0])/(y[2]-y[0]))

#
#---- Adding the XAPPEX...
        x[0]                       = -x[0] + self.geo['horz']['appex_14croot']
        x[1]                       = -x[1] + self.geo['horz']['appex_14croot']
        x[2]                       = -x[2] + self.geo['horz']['appex_14croot']
        
#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,3):
            self.geo['horz']['x'].append(str(x[i]))

#
#---- Definition of the XTE along the span...
        self.geo['horz']['xte']    = list()
        xte                        = np.zeros(3)
        xte[0]                     = x[0] + chords[0]
        xte[1]                     = x[1] + chords[1]
        xte[2]                     = x[2] + chords[2]

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,3):
            self.geo['horz']['xte'].append(str(xte[i]))

#
#---- Definition of the t/c along the span...
        self.geo['horz']['tc']      = list()
        self.geo['horz']['t']       = list()        
        tc                          = np.zeros(3)
        t                           = np.zeros(3)        

        tc[0]                       = self.geo['horz']['th_root']
        tc[2]                       = self.geo['horz']['th_tip'] 

        t[0]                        = chords[0] * tc[0]
        t[2]                        = chords[2] * tc[2] 

        t[1]                        = t[0] + (t[2]-t[0])*                     \
                                      ((y[1]-y[0])/(y[2]-y[0]))
        tc[1]                       = t[1]/chords[1]

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,3):
            self.geo['horz']['tc'].append(str(tc[i]))
            self.geo['horz']['t'].append(str(t[i]))                    
        
#
#---- Definition of the t/c along the span...
        self.geo['horz']['zu']      = list()
        self.geo['horz']['zl']      = list()        
        zu                          = np.zeros(3)
        zl                          = np.zeros(3)        

        zu[0]                       = 0.0
        zu[2]                       = zu[0] - self.geo['horz']['span']     *  \
                                      np.tan(-self.geo['horz']['dihedral'] *  \
                                      np.pi/180.0) + (t[2]/4.0 - t[0]/4.0)
                                      
        zu[1]                       = zu[0] + (zu[2]-zu[0]) *                 \
                                      ((y[1]-y[0])/(y[2]-y[0]))

        zl[0]                       = zu[0]-t[0]
        zl[2]                       = zu[2]-t[2]
        zl[1]                       = zl[0] + (zl[2]-zl[0]) *                 \
                                      ((y[1]-y[0])/(y[2]-y[0]))

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,3):
            self.geo['horz']['zu'].append(str(zu[i]))
            self.geo['horz']['zl'].append(str(zl[i])) 

        self.geo['horz']['cma']  = self.geo['horz']['croot'] * (2.0/3.0)  *   \
                                   (np.power(self.geo['horz']['taper'],2) +   \
                                    self.geo['horz']['taper']+1.0)        /   \
                                   (self.geo['horz']['taper']+1.0)

        self.geo['horz']['ycma'] = y[0] + (self.geo['horz']['cma']-chords[0])/\
                                   (chords[2]-chords[0]) * (y[2]-y[0]) 
                                   
        self.geo['horz']['xcma'] = self.geo['horz']['appex'] + (x[2]-x[0])*\
                                  ((self.geo['horz']['ycma']-y[0])/(y[2]-y[0]))

        self.geo['horz']['xcma14'] = self.geo['horz']['xcma'] +               \
                                     0.25*self.geo['horz']['cma']

        self.geo['horz']['sweeple'] = np.arctan((x[2]-x[0])/(y[2]-y[0])) *    \
                                      180.0/np.pi
                                      
        self.geo['horz']['sweepte'] = np.arctan((xte[2]-xte[1]) /             \
                                      (y[2]-y[1]))*180.0/np.pi   

# Notice that I have upper and lower sides and two horizontal tails...
        self.geo['horz']['swet']    = 4.0*((chords[1]+chords[2])/2.0) *       \
                                      (y[2]-y[1])                     
#
#---- Average t/c ....

        self.geo['horz']['tcave'] = tc[2] - ((y[2]-self.geo['horz']['ycma'])/ \
                                    (y[2]-y[0]))*(tc[2]-tc[0])
            
#
#---- Printing data
        if self.screen_flag == True:
            print('  |-------------------------------------------------|')
            print('  |           Reference Horizontal Tail             |')
            print('  |-------------------------------------------------|')
            print('   Sref          [m2]   --> ' + "{0:.3f}".                 \
                                              format(self.geo['horz']['sref']))
            
            print('   AR            [-]    --> ' + "{0:.3f}".                 \
                                                format(self.geo['horz']['ar']))
            
            print('   Taper         [-]    --> ' + "{0:.3f}".                 \
                                             format(self.geo['horz']['taper']))
            
            print('   Dihedral      [deg]  --> ' + "{0:.3f}".                 \
                                          format(self.geo['horz']['dihedral']))
            
            print('   Sweep1/4      [deg]  --> ' + "{0:.3f}".                 \
                                           format(self.geo['horz']['sweep14']))
            
            print('   X_Appex       [m]    --> ' + "{0:.3f}".                 \
                                     format(self.geo['horz']['appex_14croot']))
            
            print('   Horz_CMA      [m]    --> ' + "{0:.3f}".                 \
                                               format(self.geo['horz']['cma']))
            
            print('   Horz_YCMA     [m]    --> ' + "{0:.3f}".                 \
                                              format(self.geo['horz']['ycma']))
            
            print('   Horz_XCMA     [m]    --> ' + "{0:.3f}".                 \
                                              format(self.geo['horz']['xcma']))        
            
            print('   Sweep_LE      [deg]  --> ' + "{0:.3f}".                 \
                                           format(self.geo['horz']['sweeple']))
            
            print('   Sweep_TE      [deg]  --> ' + "{0:.3f}".                 \
                                           format(self.geo['horz']['sweepte']))
            
            print('   Swet          [m2]   --> ' + "{0:.3f}".                 \
                                              format(self.geo['horz']['swet']))        
            
            print('   t/c_Root      [-]    --> ' + "{0:.3f}".                 \
                                           format(self.geo['horz']['th_root']))
            
            print('   t/c_Tip       [-]    --> ' + "{0:.3f}".                 \
                                            format(self.geo['horz']['th_tip']))
            
            print('   Width Fus     [m]    --> ' + "{0:.3f}".                 \
                                         format(self.geo['horz']['width_fus']))
            
            print('   Span          [m]    --> ' + "{0:.3f}".                 \
                                              format(self.geo['horz']['span']))
            
            print('   Croot         [m]    --> ' + "{0:.3f}".                 \
                                             format(self.geo['horz']['croot']))
            
            print('   Ctip          [m]    --> ' + "{0:.3f}".                 \
                                              format(self.geo['horz']['ctip']))
            
            print('                                                          ')            

        pass
      
