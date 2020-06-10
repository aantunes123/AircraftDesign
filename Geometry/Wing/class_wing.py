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

                         CLASS CREATE_WING
                        ------------------

    Here the Wing geometry is created.

   sref           --> self explanatory                    [m2]  [real]      
   ar             --> wing aspect ratio                    [-]  [real]      
   sweep14        --> wing sweep 1/4 chord               [deg]  [real]      
   taper          --> wing taper Croot/Ctip                [-]  [real]      
   dihedral       --> self explanatory                   [deg]  [real]      
   kink           --> wing Ykink / Ytip                    [-]  [real]      
   tcroot         --> relative thickness                   [-]  [real]      
   tckink         --> relative thickness                   [-]  [real]      
   tctip          --> relative thickness                   [-]  [real]      
   stubwidth      --> stub width (fuselage width)          [m]  [real]      
   xappex         --> wing location X                      [m]  [real]      
   yappex         --> wing location Y                      [m]  [real]      
   spar_LE        --> Front spar x/c position              [-]  [real]      
   spar_TE        --> Rear spar x/c position               [-]  [real]      
   tank_y         --> Fuel tank length/wing_semispan       [-]  [real]      
   sections       --> wing No. of stations                 [-]  [int.]         

"""
import numpy as np
from scipy.optimize import fmin
from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                               WING CLASS                             #
#----------------------------------------------------------------------#
class Create_Wing(object, metaclass=AuxTools):
    """
        Aircraft Components:  WING
    """
   
    def __init__(self, geo,*args, **kwargs):
        super(Create_Wing, self).__init__(geo,*args, **kwargs)
        
        if 'Fwing' not in kwargs:
            raise ValueError("Cannot initiate Create_Wing...provide the       \
                              argument Fwing = 'file_name'.")            
        self.file_name = kwargs['Fwing']     
        
# Data for the wing...some setup to avoid crashing

        self.geo['Kink_wing']          = {}     # Real Wing...

        self.geo['wing']               = {}
        self.geo['wing']['sref']       = 110.0
        self.geo['wing']['ar']         =  10.0
        self.geo['wing']['sweep14']    =  28.0
        self.geo['wing']['taper']      =  0.24
        self.geo['wing']['dihedral']   =  5.00
        self.geo['wing']['kink']       =  0.39
        self.geo['wing']['tcroot']     =  0.145
        self.geo['wing']['tckink']     =  0.120
        self.geo['wing']['tctip']      =  0.110
        self.geo['wing']['stubwidth']  =  3.500
        self.geo['wing']['xappex']     = 12.900
        self.geo['wing']['yappex']     = -1.230
        self.geo['wing']['spar_LE']    =  0.20
        self.geo['wing']['spar_TE']    =  0.70
        self.geo['wing']['tank_y']     =  0.70        
        self.geo['wing']['sections']   =  4

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
            for key in (self.geo['wing']):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.geo['wing'][key] = float(vvals[i])

        pass

#----------------------------------------------------------------------#
#                    Computing the Reference Wing                      #
#----------------------------------------------------------------------#
    def Wing_Reference_Planform(self):
        """ 
            The wing_ref method computes the reference wing given a certain
            geometrical input provided by the user. The method is available
            for objects from the class CREATE_WING. The method adds to the
            object a set of dictionaries containing important gemetrical 
            values.
        """
#
#---- Initial definitions...

        self.geo['wing']['span']  = np.sqrt(self.geo['wing']['sref']*self.geo['wing']['ar'])
        self.geo['wing']['croot'] = 2.0 * self.geo['wing']['sref'] /(self.geo['wing']['span']*(1.0+self.geo['wing']['taper']))
        self.geo['wing']['ctip']  = self.geo['wing']['croot'] * self.geo['wing']['taper']
#
#---- Definition of the Y stations along the span...

        self.geo['wing']['y']      = list()
        y                          = np.zeros(4)
        y[0]                       = 0.0
        y[1]                       = self.geo['wing']['stubwidth'] / 2.0
        y[2]                       = self.geo['wing']['span'] * self.geo['wing']['kink'] / 2.0
        y[3]                       = self.geo['wing']['span'] / 2.0

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,4):
            self.geo['wing']['y'].append(str(y[i]))
#
#---- Definition of the L.E. coordinate for each Y station...

        self.geo['wing']['x']      = list()
        x                          = np.zeros(4)
        x[0]                       = 0.0
        x[3]                       =  x[0] - (self.geo['wing']['croot']/4.0) - (y[3]-y[0]) * np.tan(self.geo['wing']['sweep14']*np.pi/180) \
                                           + (self.geo['wing']['ctip']/4.0)
        x[1]                       =  x[0] + (x[3]-x[0]) * ((y[1]-y[0])/(y[3]-y[0]))
        x[2]                       =  x[0] + (x[3]-x[0]) * ((y[2]-y[0])/(y[3]-y[0]))
#
#---- Adding the XAPPEX...
        x[0]                       = -x[0] + self.geo['wing']['xappex']
        x[1]                       = -x[1] + self.geo['wing']['xappex']
        x[2]                       = -x[2] + self.geo['wing']['xappex']
        x[3]                       = -x[3] + self.geo['wing']['xappex']

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,4):
            self.geo['wing']['x'].append(str(x[i]))
#
#---- Computation of the chords...

        self.geo['wing']['chords']    = list()
        chords                     = np.zeros(4)
        chords[0]                  = self.geo['wing']['croot']
        chords[1]                  = self.geo['wing']['croot'] + (self.geo['wing']['ctip'] - self.geo['wing']['croot']) * \
                                                                   ((y[1]-y[0])/(y[3]-y[0]))

        chords[2]                  = self.geo['wing']['croot'] + (self.geo['wing']['ctip'] - self.geo['wing']['croot']) * \
                                                                   ((y[2]-y[0])/(y[3]-y[0]))
        chords[3]                  = self.geo['wing']['ctip']

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,4):
            self.geo['wing']['chords'].append(str(chords[i]))

#
#---- Computation of the XTE...
        self.geo['wing']['xte'] = list()
        for i in range(0,4):
            self.geo['wing']['xte'].append(str(float(self.geo['wing']['x'][i])+float(self.geo['wing']['chords'][i])))

#
#---- Computation of the wing t/c

        self.geo['wing']['tc']     = list()
        self.geo['wing']['t']      = list()        
        tc                         = np.zeros(4)
        t                          = np.zeros(4)          
        tc[1]                      = self.geo['wing']['tcroot']
        tc[2]                      = self.geo['wing']['tckink']
        tc[3]                      = self.geo['wing']['tctip']
        
        t[1]                       =  tc[1] * chords[1]
        t[2]                       =  tc[2] * chords[2]
        t[3]                       =  tc[3] * chords[3]        

        tc[0]                      = ( t[1] + ((y[0]-y[1])/(y[1]-y[2])) * (t[1]-t[2]) ) / chords[0]
        t[0]                       =   t[1] + ((y[0]-y[1])/(y[1]-y[2])) * (t[1]-t[2])

#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,4):
            self.geo['wing']['tc'].append(str(tc[i]))
            self.geo['wing']['t'].append(str(t[i]))            

#
#---- Computation of the wing Z
        self.geo['wing']['zu']     = list()
        self.geo['wing']['zl']     = list()        
        zu                         = np.zeros(4)
        zl                         = np.zeros(4)

        zu[0]                      = 0.0
        zu[3]                      = zu[0] - y[3]*np.tan(-self.geo['wing']['dihedral']*np.pi/180.0)  \
                                           + (t[3]/2.0 - t[0]/2.0)
        zu[1]                      = zu[0] + (zu[3]-zu[0])*((y[1]-y[0])/(y[3]-y[0]))
        zu[2]                      = zu[0] + (zu[3]-zu[0])*((y[2]-y[0])/(y[3]-y[0]))
#
        zl[0]                      = zu[0] - t[0]
        zl[1]                      = zu[1] - t[1]
        zl[2]                      = zu[2] - t[2]
        zl[3]                      = zu[3] - t[3]

        aux1                       = zu[0] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])
        aux2                       = zu[1] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])
        aux3                       = zu[2] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])
        aux4                       = zu[3] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])
        aux5                       = zl[0] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])
        aux6                       = zl[1] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])
        aux7                       = zl[2] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])
        aux8                       = zl[3] - self.geo['wing']['yappex'] - (1.0/3.0) * (zu[0]+zl[0])        

        zu[0]                      = aux1
        zu[1]                      = aux2
        zu[2]                      = aux3
        zu[3]                      = aux4        
        zl[0]                      = aux5
        zl[1]                      = aux6
        zl[2]                      = aux7
        zl[3]                      = aux8
        
#--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,4):
            self.geo['wing']['zu'].append(str(zu[i]))
            self.geo['wing']['zl'].append(str(zl[i]))
        
#
#---- CMA
        self.geo['wing']['cma']       =  (2.0/3.0) * self.geo['wing']['croot'] * (np.power(self.geo['wing']['taper'],2)+ \
                                                       self.geo['wing']['taper']+1.0)/(self.geo['wing']['taper']+1.0)
        self.geo['wing']['ycma']      =  y[0] + (self.geo['wing']['cma'] - chords[0])/(chords[3]-chords[0]) * (y[3]-y[0])
        self.geo['wing']['xcma']      =  self.geo['wing']['xappex'] + (x[3]-x[0]) * ((self.geo['wing']['ycma']-y[0])/(y[3]-y[0]))
        self.geo['wing']['sweeple']   =  np.arctan((x[3]-x[0])/(y[3]-y[0])) *180.0/np.pi
        self.geo['wing']['sweepte1']  = -np.arctan( ((-x[2]-chords[2])-(-x[0]-chords[0]))/(y[2]-y[0]) ) * 180.0 /np.pi
        self.geo['wing']['sweepte2']  = -np.arctan( ((-x[3]-chords[3])-(-x[2]-chords[2]))/(y[3]-y[2]) ) * 180.0 /np.pi        

#
#---- Wing Swet...

        self.geo['wing']['swetin']    =  2.0*((chords[1]+chords[2])/2.0)* (y[2]-y[1])                         # Notice that I have upper and lower sides...
        self.geo['wing']['swetout']   =  2.0*((chords[3]+chords[2])/2.0)* (y[3]-y[2])         
        self.geo['wing']['swet']      =  2.0*(self.geo['wing']['swetin'] + self.geo['wing']['swetout'])   # I also have right and left wing...

#
#---- Average t/c ....

        if (self.geo['wing']['ycma'] > y[2]):
            self.geo['wing']['tcave'] = tc[2] - ((y[2]-self.geo['wing']['ycma'])/(y[2]-y[1]))*(tc[2]-tc[1])
        else:
            self.geo['wing']['tcave'] = tc[3] - ((y[3]-self.geo['wing']['ycma'])/(y[3]-y[2]))*(tc[3]-tc[2])

#
#---- Printing the data
        if self.screen_flag == True:
            print('  |-------------------------------------------------|')
            print('  |               Reference WING                    |')
            print('  |-------------------------------------------------|')
            print('   Sref          [m2]   --> ' + "{0:.3f}".format(self.geo['wing']['sref']))
            print('   AR            [-]    --> ' + "{0:.3f}".format(self.geo['wing']['ar']))
            print('   Sweep         [deg]  --> ' + "{0:.3f}".format(self.geo['wing']['sweep14']))
            print('   Taper         [-]    --> ' + "{0:.3f}".format(self.geo['wing']['taper']))
            print('   Span          [m]    --> ' + "{0:.3f}".format(self.geo['wing']['span']))        
            print('   Dihedral      [deg]  --> ' + "{0:.3f}".format(self.geo['wing']['dihedral']))
            print('   Wing_CMA      [m]    --> ' + "{0:.3f}".format(self.geo['wing']['cma']))
            print('   Wing_YCMA     [m]    --> ' + "{0:.3f}".format(self.geo['wing']['ycma']))
            print('   Wing_XCMA     [m]    --> ' + "{0:.3f}".format(self.geo['wing']['xcma']))        
            print('   Sweep_LE      [deg]  --> ' + "{0:.3f}".format(self.geo['wing']['sweeple']))
            print('   Sweep_TE1     [deg]  --> ' + "{0:.3f}".format(self.geo['wing']['sweepte1']))
            print('   Swet          [m2]   --> ' + "{0:.3f}".format(self.geo['wing']['swet']))        
            print('   Y_Kink        [m]    --> ' + "{0:.3f}".format(self.geo['wing']['kink']))
            print('   t/c_Root      [-]    --> ' + "{0:.3f}".format(self.geo['wing']['tcroot']))
            print('   t/c_Kink      [-]    --> ' + "{0:.3f}".format(self.geo['wing']['tckink']))
            print('   t/c_Tip       [-]    --> ' + "{0:.3f}".format(self.geo['wing']['tctip']))
            print('   Y_stub        [m]    --> ' + "{0:.3f}".format(self.geo['wing']['stubwidth']))
            print('   Y_Appex       [m]    --> ' + "{0:.3f}".format(self.geo['wing']['yappex']))
            print('   Wing_Sections [-]    --> ' + "{0:.3f}".format(self.geo['wing']['sections']))
            print('                                                                 ')        
       
        pass

#----------------------------------------------------------------------#
    def Converge_Wing_Area(self,x):

        fcr    = 1.3
        
# Defining the list to store the data for the wing with an TE Kink
        self.geo['Kink_wing']['chords'] = list()
        self.geo['Kink_wing']['xte']    = list()
        self.geo['Kink_wing']['x']      = list()
        self.geo['Kink_wing']['y']      = list()        

        chords  = np.zeros(4)
        xte     = np.zeros(4)   

# Geometry definition...
        dcr   = self.geo['wing']['croot']*fcr - self.geo['wing']['croot']
        self.geo['Kink_wing']['croot']   = 2.0*self.geo['wing']['sref']/ (self.geo['wing']['span'] *           \
                                            (1.0+self.geo['wing']['taper'])) + dcr
  
        self.geo['Kink_wing']['ctip']    = self.geo['wing']['ctip']

        chords[0]   = self.geo['Kink_wing']['croot']      
        chords[2]   = chords[0] + (self.geo['Kink_wing']['ctip']-self.geo['Kink_wing']['croot']) *             \
                        ( (float(self.geo['wing']['y'][2])-float(self.geo['wing']['y'][0]))      /             \
                        (float(self.geo['wing']['y'][3])-float(self.geo['wing']['y'][0]))  )
        
        chords[2]   = chords[2] - x
        chords[1]   = chords[0] + (chords[2]-chords[0])                                          *             \
                        ( (float(self.geo['wing']['y'][1])-float(self.geo['wing']['y'][0]))      /             \
                          (float(self.geo['wing']['y'][2])-float(self.geo['wing']['y'][0]))  )
        chords[3]   = self.geo['Kink_wing']['ctip']
        
        xte[0]      = -(float(self.geo['wing']['x'][0])- self.geo['wing']['xappex']) -  chords[0]
        xte[1]      = -(float(self.geo['wing']['x'][1])- self.geo['wing']['xappex']) -  chords[1] 
        xte[2]      = -(float(self.geo['wing']['x'][2])- self.geo['wing']['xappex']) -  chords[2] 
        xte[3]      = -(float(self.geo['wing']['x'][3])- self.geo['wing']['xappex']) -  chords[3] 
  
        m1          =  -(float(self.geo['wing']['xte'][0])-float(self.geo['wing']['xte'][2])) /                \
                        (float(self.geo['wing']['y'][0])-float(self.geo['wing']['y'][2]))
                        
        m2          =  (xte[0]-xte[2]) / (float(self.geo['wing']['y'][0])-float(self.geo['wing']['y'][2]))

        m3          =  ((-float(self.geo['wing']['xte'][0])-m1*float(self.geo['wing']['y'][0])) -              \
                        (xte[0]-m2*float((self.geo['wing']['y'][0])))) / (m2-m1)

        st1         = abs((-float(self.geo['wing']['xte'][2])-xte[2])* (float(self.geo['wing']['y'][3]) -      \
                            float(self.geo['wing']['y'][2]))/2.0)

        st2         = abs((-float(self.geo['wing']['xte'][2])-xte[2])* (m3 - float(self.geo['wing']['y'][2])) /2.0)
            
        st3         = abs((-float(self.geo['wing']['xte'][1])-xte[1])* (m3 - float(self.geo['wing']['y'][1])) /2.0)

        error       = abs(st1+st2-st3)
        
###--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,4):
            self.geo['Kink_wing']['x'].append(str(self.geo['wing']['x'][i]))
            self.geo['Kink_wing']['y'].append(str(self.geo['wing']['y'][i]))            
            self.geo['Kink_wing']['chords'].append(str(chords[i]))
            self.geo['Kink_wing']['xte'].append(str(-xte[i]))

        return error

#----------------------------------------------------------------------#
    def Wing_TE_Kink(self):

# First thing is to converge the area...
        print('Computing the Real Wing Planform -- Minimizing the Error to get Wing_Ref_Swet == Wing_Real_Swet')
        fmin(self.Converge_Wing_Area,2.0)
       
# Defining the lists...
        self.geo['Kink_wing']['tc']  = list()
        self.geo['Kink_wing']['t']   = list()
        self.geo['Kink_wing']['zu']  = list()
        self.geo['Kink_wing']['zl']  = list()        

        pi = np.arccos(-1.0)
        
        tc = np.zeros(4)
        t  = np.zeros(4)
        zu = np.zeros(4)
        zl = np.zeros(4)        

#  Wing Thick and t/c
        tc[1] = self.geo['wing']['tc'][1]
        tc[2] = self.geo['wing']['tc'][2]
        tc[3] = self.geo['wing']['tc'][3]
        
        t[1]  = tc[1] * float(self.geo['Kink_wing']['chords'][1])
        t[2]  = tc[2] * float(self.geo['Kink_wing']['chords'][2])
        t[3]  = tc[3] * float(self.geo['Kink_wing']['chords'][3])

        t[0]  = t[1]  + ((float(self.geo['wing']['y'][0])-float(self.geo['wing']['y'][1]))  /      \
                         (float(self.geo['wing']['y'][1])-float(self.geo['wing']['y'][2]))) *      \
                         (t[1]-t[2])

        tc[0] = t[0] / float(self.geo['Kink_wing']['chords'][0])
        
# Zupper and Zlower
        zu[0] = 0.0
        zu[3] = zu[0] - float(self.geo['wing']['y'][3])*np.tan(float(-self.geo['wing']['dihedral'])*pi/180) +             \
                        (t[3]/2.0 - t[0]/2.0)
        zu[1] = zu[0] + (zu[3]-zu[0])* ( (float(self.geo['wing']['y'][1])-float(self.geo['wing']['y'][0])) /             \
                        (float(self.geo['wing']['y'][3])-float(self.geo['wing']['y'][0]))  )
        zu[2] = zu[0] + (zu[3]-zu[0])* ( (float(self.geo['wing']['y'][2])-float(self.geo['wing']['y'][0])) /             \
                        (float(self.geo['wing']['y'][3])-float(self.geo['wing']['y'][0]))  )

        zl[0] = zu[0] - t[0]
        zl[1] = zu[1] - t[1]
        zl[2] = zu[2] - t[2]
        zl[3] = zu[3] - t[3]

        z0    = zu[0] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0])
        z1    = zu[1] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0])
        z2    = zu[2] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0])
        z3    = zu[3] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0])  
        z00   = zl[0] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0])
        z11   = zl[1] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0])
        z22   = zl[2] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0])
        z33   = zl[3] + float(self.geo['wing']['yappex']) - (1.0/3.0) * (zu[0]+zl[0]) 

        zu[0] = z0
        zu[1] = z1
        zu[2] = z2
        zu[3] = z3
        zl[0] = z00
        zl[1] = z11
        zl[2] = z22
        zl[3] = z33
        
###--- ...to List()...using a list is easier to later add new sections...
        for i in range(0,4):
            self.geo['Kink_wing']['tc'].append(str(tc[i]))
            self.geo['Kink_wing']['t'].append(str(t[i]))            
            self.geo['Kink_wing']['zu'].append(str(zu[i]))
            self.geo['Kink_wing']['zl'].append(str(zl[i]))

# Notice that I have upper and lower sides...        
        self.geo['Kink_wing']['swetin']    =  (float(self.geo['Kink_wing']['chords'][1])+float(self.geo['Kink_wing']['chords'][2])) * \
                                              (float(self.geo['wing']['y'][2])-float(self.geo['wing']['y'][1]))
                                              
        self.geo['Kink_wing']['swetout']   =  (float(self.geo['Kink_wing']['chords'][3])+float(self.geo['Kink_wing']['chords'][2])) * \
                                              (float(self.geo['wing']['y'][3])-float(self.geo['wing']['y'][2]))

# I also have right and left wing...        
        self.geo['Kink_wing']['swet']      =  2.0*(self.geo['Kink_wing']['swetin'] + self.geo['Kink_wing']['swetout'])   

      

