#-----------------------------------------------------------------------------#
#   Program to compute the aircraft main geometrical parameters.              #
#                                                                             #
#   Alexandre Antunes (03/02/2017)                                            #
#                                                                             #
#                                                                             #                       
# Created:     03/03/2017                                                     #
# Licence:     GNU AGPLv3                                                     #
#                                                                             #
#  Permissions of this strongest copyleft license are conditioned             #
#  on making available complete source code of licensed works and             #
#  modifications, which include larger works using a licensed work,           #
#  under the same license. Copyright and license notices must be preserved.   #
#  Contributors provide an express grant of patent rights. When a             #
#  modified version is used to provide a service over a network,              #
#  the complete source code of the modified version must be made available.   #
#                                                                             #
#-----------------------------------------------------------------------------#
import numpy as np
import os

from Auxilliary.class_aux import AuxTools
from scipy import interpolate
import scipy.integrate as integrate
#dire = os.path.dirname(os.path.abspath(__file__))

#----------------------------------------------------------------------#
#                               WING CLASS                             #
#----------------------------------------------------------------------#
class Coefficients(object, metaclass=AuxTools):
    """
        Aerodynamics Coefficients
    """
    
    def __init__(self, geo,*args, **kwargs):
        super(Coefficients, self).__init__(geo,*args, **kwargs)

# The Wing, HT and VT dictionary will be defined inside the loop of the method
# once the CDo from these components are computed using the same method.

        self.drag            = {}
        self.drag['fus']     = {}
        self.drag['pylon']   = {}
        self.drag['nacelle'] = {}

# Raise error...
        if 'Method' not in kwargs:
            raise ValueError("Cannot initiate Aerodynamic computation. Provide\
                              the  argument Method = 'Torenbeek'.")            
        self.method = kwargs['Method']
        

#----------------------------------------------------------------------#
#                    Computing the Wing  Drag                          #
#----------------------------------------------------------------------#
    def FrictionDrag(self,airprop,Fphase):
        """

            Fphase   --> Flight Phase.


        """

        components = ('wing', 'horz', 'vert')
        

# Loping over the Components...

        for item in components:

            self.drag[item]     = {}            
# 
#--- Variables present in most of the methods...
            cs    = np.cos(self.geo[item]['sweep14']*np.pi/180.0)
            asom  = np.sqrt(1.40 * 287.074 * airprop[Fphase]['temp_kelvin'])
            reym  = airprop[Fphase]['mach'] * asom *                          \
                    airprop[Fphase]['density'] / airprop[Fphase]['visc']

#----
#      Lift correction from the Roskan book VI pg 24 figure 4.2, I did 
#      considered a average value from the sum of the curves from 3 Mach
#      numbers (.25, .60 and .80) and adopted the polynomial regression
#      to obtain the RLS value.

# Reynolds number...
            rey              = reym * self.geo[item]['cma']               

# Skin Friction...            
            self.drag[item]['cf']  = 0.455/((np.log10(rey))**2.58)
            
            rls              = -2.1851*(cs)**3.0 + 3.9364*(cs)**2.0 -         \
                                1.5551*cs + 0.9623
                                
            self.drag[item]['cdo'] =  rls * self.drag[item]['cf']*(1.0 + 1.2* \
                                self.geo[item]['tcave'] + 100    *            \
                               ((self.geo[item]['tcave'])**4.0)) *            \
                             self.geo[item]['swet']/self.geo['wing']['sref']

#------------                     FUSELAGE        -----------------------------

#
#----  Drag computation  -        ROSKAN   -

        fac                = 0.05
        fus_diameter_base  = fac * self.geo['fus']['diameter']
        fus_area_base      = np.pi*(fus_diameter_base**2.0)/4.0
        fus_area           = np.pi*(self.geo['fus']['diameter']**2.0)/4.0
           
        self.geo['fus']['fus_length'] = 32.096
        reyfus    = reym * self.geo['fus']['fus_length']

        cffus     = 0.455/((np.log10(reyfus))**2.580) 

        cdofus    = cffus * ( (1.0 +60.0/(self.geo['fus']['esb']**3.0)) +     \
                                          0.0025*self.geo['fus']['esb']) *    \
                                         (self.geo['fus']['swet']        /    \
                                          self.geo['wing']['sref'])
                                         
        cdobfus   = cffus*(fus_area_base/self.geo['wing']['sref'])
           
        cdbfus    = ((0.029*(fus_diameter_base/                               \
                             self.geo['fus']['diameter'])**3.0) /             \
                        (cdobfus*(self.geo['wing']['sref']/fus_area))**0.5) * \
                        (fus_area/self.geo['wing']['sref'])

        self.drag['fus']['cdo'] =  cdofus + cdbfus

#----  Drag computation  -        TORENBEEK   -
#            self.drag['fus']['cdo'] = 0.0031 *self.geo['fus']['fus_length'] * \
#                                     (self.geo['fus']['diameter']           + \
#                                      self.geo['fus']['diameter'])          / \
#                                      self.geo['wing']['sref']

           
#----------------                   PYLON                ----------------------

        cs   = np.cos(self.geo['pylon']['sweep']*np.pi/180.0)

#---  Wing Reynolds number.
#              
        reypyl = reym * self.geo['pylon']['pyl_cma']

#---   Skin friction of the pylon...
#           
        cfpyl  = 0.455/((np.log10(reypyl))**2.580)                     

#----  Pylon Form Factor
#
        FFpyl  = 1.0 + ( (2.7*self.geo['pylon']['tc']  +                      \
                          100.0*self.geo['pylon']['tc']**4.0) * (cs**.25) )

#----  Drag
        self.drag['pylon']['cdo'] =  self.geo['nacelle']['no']  *             \
                                        cfpyl * FFpyl              *          \
                                        self.geo['pylon']['swet'] /           \
                                        self.geo['wing']['sref']

#----------------                 NACELLE                ----------------------        
           
        reynac = reym * self.geo['nacelle']['lmax'] 

##---   Skin friction of the pylon...
#           
        cfnac  = 0.455/((np.log10(reynac))**2.580)                     

##----  Pylon Form Factor
#
        FFnac  = 1.00 +  (2.70  * self.geo['nacelle']['tc'] +                 \
                              100.0 * self.geo['nacelle']['tc']**4.0)

#----  Drag
#            
        self.drag['nacelle']['cdo']  = self.geo['nacelle']['no'] * cfnac   *  \
                                       FFnac * self.geo['nacelle']['swet'] /  \
                                               self.geo['wing']['sref']
#
#---- Plotting the computed data...
        if self.screen_flag == True:
            print('  |-------------------------------------------------|')
            print('  |            Friction  Drag  Component            |')            
            print('  |-------------------------------------------------|')
            
            for item in components:
                print('   CDo '+item +'     [counts]    --> ' + "{0:.1f}".   \
                                          format(self.drag[item]['cdo']*10000))
            print('   CDo Fuselage [counts]    --> ' + "{0:.1f}".      \
                                         format(self.drag['fus']['cdo']*10000))
            print('   CDo Pylon    [counts]    --> ' + "{0:.1f}".      \
                                       format(self.drag['pylon']['cdo']*10000))            
            print('   CDo Nacelle  [counts]    --> ' + "{0:.1f}".      \
                                     format(self.drag['nacelle']['cdo']*10000)) 

#------------------------------------------------------------------------------
    def InducedDrag(self,airprop,Fphase):
        """    
            This method computes the induced drag using the AVL software.
            
            
        """
        
# AVL case name
        file     = 'AVL_Sim'        
        file_geo = file+'.avl'

        f1       = open(file_geo,'w')
        f1.write('%s  \n' %('AircraftDesign'))
        f1.write('%s  \n' %('#Mach  '))
        f1.write('%s  \n' %('0.00  '))
        f1.write('%s  \n' %('#IYsym   IZsym   Zsym  '))
        f1.write('%s  \n' %('0       0       0.0  '))
        f1.write('%s  \n' %('#Sref    Cref    Bref  '))
        line = '{:06.3f}'.format(self.geo['wing']['sref'])   + '  ' +         \
               '{:06.3f}'.format(self.geo['wing']['cma'])    + '  ' +         \
               '{:06.3f}'.format(self.geo['wing']['span']) 
        line = str(line)                
        f1.write('%s  \n' %(line))

        f1.write('%s  \n' %('#Xref    Yref    Zref  '))
        line = '{:06.3f}'.format(self.geo['wing']['xappex']) +  '  ' +        \
               '{:06.3f}'.format(self.geo['wing']['yappex']) +  '  ' +        \
               '{:06.3f}'.format(00.0000000) 
        line = str(line)

# Model Definition       
        f1.write('%s  \n' %(line))
        f1.write('%s  \n' %('0.0  '))
        f1.write('%s  \n' %('#------------------------------------------------------------------------------------------  '))
        f1.write('%s  \n' %('#  '))
        f1.write('%s  \n' %('SURFACE   '))
        f1.write('%s  \n' %('Right_Wing   '))
        f1.write('%s  \n' %('!Nchordwise  Cspace  Nspanwise  Sspace  '))
        f1.write('%s  \n' %('16         1.0       40        3.0  '))
        f1.write('%s  \n' %('COMPONENT   '))
        f1.write('%s  \n' %('1  '))
        f1.write('%s  \n' %('ANGLE  '))
        f1.write('%s  \n' %('0.0  '))
        f1.write('%s  \n' %('SCALE  '))
        f1.write('%s  \n' %('1.0   1.0   1.0  '))
        f1.write('%s  \n' %('TRANSLATE  '))
        f1.write('%s  \n' %('0.0   0.0   0.0  '))

# Right Wing
        for i in range(3,0,-1):
            f1.write('%s  \n' %('#------------------------------------------------------------------------------------------  '))
            f1.write('%s  \n' %('SECTION  '))
            f1.write('%s  \n' %('#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace  '))
            
            zmed =  0.5 * (float(self.geo['Kink_wing']['zu'][i]) +                 \
                           float(self.geo['Kink_wing']['zl'][i])   )
            
            line = '{:06.3f}'.format(float(self.geo['Kink_wing']['x'][i]))  + \
                   ' '                                                      + \
                   '{:06.3f}'.format(-float(self.geo['Kink_wing']['y'][i]))  + \
                   ' '                                                      + \
                   '{:06.3f}'.format(float(zmed))                           + \
                   '  '                                                     + \
               '{:06.3f}'.format(float(self.geo['Kink_wing']['chords'][i])) + \
                   '  '  + '0.0  0.0    0.0'
            line = str(line)                   
            f1.write('%s  \n' %(line))
            f1.write('%s  \n' %('AFILE  '))
            f1.write('%s  \n' %('naca0012.dat  '))
            
# Left Wing
        for i in range(0,4):
            f1.write('%s  \n' %('#------------------------------------------------------------------------------------------  '))
            f1.write('%s  \n' %('SECTION  '))
            f1.write('%s  \n' %('#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace  '))
            
            zmed =  0.5 * (float(self.geo['Kink_wing']['zu'][i]) +                 \
                           float(self.geo['Kink_wing']['zl'][i])   )
            
            line = '{:06.3f}'.format(float(self.geo['Kink_wing']['x'][i]))  + \
                   ' '                                                      + \
                   '{:06.3f}'.format(float(self.geo['Kink_wing']['y'][i]))  + \
                   ' '                                                      + \
                   '{:06.3f}'.format(float(zmed))                           + \
                   '  '                                                     + \
               '{:06.3f}'.format(float(self.geo['Kink_wing']['chords'][i])) + \
                   '  '  + '0.0  0.0    0.0'
                   
            line = str(line)                   
            f1.write('%s  \n' %(line))
            f1.write('%s  \n' %('AFILE  '))
            f1.write('%s  \n' %('naca0012.dat  '))  
        f1.close()
            
#  Writting the AVL Execution Commands...
        file_run  = file+'.run'
        file_out  = file+'.out'
        file_stp  = file+'_strip.out'
        file_ben  = file+'_bending.out'
        file_star = '*.out'

# deleting the output with the bending moment information
        dire = os.getcwd()
        path = os.path.join(dire,file_ben)

        if os.path.isfile(path):   
            os.system('del '+file_ben)

# deleting the output files
        dire = os.getcwd()
        path = os.path.join(dire,file_out)

        if os.path.isfile(path):   
            os.system('del '+file_star)

# Writting the run file...and conisdering the required CL

        self.perf['CL'] = self.weight['total'] * 9.81  /                      \
                          ( 0.5 * airprop[Fphase]['density']              *   \
                          airprop[Fphase]['velocity']                     *   \
                          airprop[Fphase]['velocity']                     *   \
                          self.geo['wing']['sref'] )

        f2       = open(file_run,'w')
        f2.write('%s   \n' %('load'))
        f2.write('%s   \n' %(file_geo))    
        f2.write('%s   \n' %('oper'))
        f2.write('%s   \n' %('a'))
        f2.write('%s   \n' %('c'))
        f2.write('%s   \n' %(float(self.perf['CL'])))
        f2.write('%s   \n' %('x'))    
        f2.write('%s   \n' %('FT'))  

# check if the file exists...than I need a additional command...
        cfile = os.path.join(dire,file_out)  
        flag  = os.path.isfile(cfile)

        if flag == True:
            f2.write('%s   \n' %(file_out))        
            f2.write('%s   \n' %('o'))                
        if flag == False:
            f2.write('%s   \n' %(file_out))
        f2.write('%s   \n' %('FS'))
        f2.write('%s   \n' %(file_stp))                
        f2.write('%s   \n' %('VM'))
        f2.write('%s   \n' %(file_ben))    
        f2.write('%s   \n' %(' '))        
        f2.write('%s   \n' %('quit'))            
        f2.close()

# Command to run the case
        command = 'avl.exe < ' + file_run 
        case = os.path.join(dire,command)

# running...
        os.system(case)

# PostProcessing the AVL simulation for the computed CL
        file_post = file+'.out'
        f3        = open(file_post,'r')

        flag = False
        for line in f3:
            aux = line.strip().split()
            for key in aux:
                if key == 'CDind':
                    flag = True
            if flag:
                self.drag['wing']['induced'] = float(aux[5]) 
                flag                         = False
        f3.close()
#
#---- Print the Induced drag...
        print('  ')
        print('   Induced and Wave drag @ CL ' + "{0:.3f}".      \
                                    format(self.perf['CL'][0])) 
        print('   --------------------------------  ')        
        print('   CD_Ind       [counts]    --> ' + "{0:.1f}".      \
                                    format(self.drag['wing']['induced']*10000)) 

# Post-Processing the CL versus Span file
        aux             = []
        self.avl_y      = []
        self.avl_chord  = []
        self.avl_cly    = []


        k = 0
        f6  = open(file_stp,'r')
        for line in f6:

            if line[0:6] ==' -----':
                continue

            if k > 18:
                aux.append(line.strip().split())
                self.avl_y.append(float(line.strip().split()[1]))
                self.avl_chord.append(float(line.strip().split()[2]))
                self.avl_cly.append(float(line.strip().split()[7]))
                
            k +=1
        f6.close()

#------------------------------------------------------------------------------
    def WaveDrag(self,airprop,Fphase):        
        """ 
            Airfoil Technology Factor
            ka = 0.87  mid 70's transport
            ka = 0.95  supercritical airfoils
            
            Reference
            D:\Thesis\articles_books\_Drag_decomposition\ConfigAeroDrag.pdf

            Divergence Mach Number
            Mdd =  κA /cosΛ − (t/c)/cos(Λ)2 − cl/ 10cos(Λ)3

        """       
# Factors
        ka = 0.95
        k11   = 0.928
        k22   = 3.000
        k33   = 0.500
        
# Interpolation Function
        x   = list(map(float,self.geo['wing']['y']))
        y1  = list(map(float,self.geo['wing']['tc']))
        y2  = list(map(float,self.geo['wing']['chords']))

        x3  = list(map(float,self.avl_y))
        y3  = list(map(float,self.avl_chord))
             

# Interpolation Objects...
        tc  = interpolate.interp1d(x,y1)
        cl  = interpolate.interp1d(x3,y3)

        mcr = []       
# Computing the divergence Mach Number
        j = 0
        for i in range(0,len(self.avl_y)):
            if abs(float(self.avl_y[i])) >                                    \
               abs(float(self.geo['wing']['y'][1])):
                   cos = np.cos(self.geo['wing']['sweep14']*np.pi/180)
                   k1  = ka / cos
                   k2  = tc(abs(float(self.avl_y[i]))) / (cos*cos)
                   k3  = abs(float(self.avl_cly[i]))/ (10.0 * np.power(cos,3))
                   mdd = k1 - k2 - k3
           
#                   mdd = (  k11 - (0.1*abs(float(self.avl_cly[i]))*k22*cos) -   \
#                                 (k33*tc(abs(float(self.avl_y[i])))*cos) ) /   \
#                            cos

                   aux = mdd - np.power((0.1/80.0),(1.0/3.0))
                   mcr.append(float(aux))
            if abs(float(self.avl_y[i])) <                                  \
               abs(float(self.geo['wing']['y'][1])):                  
                   j += 1
                
# Getting the left side and then I double the Cdwave..
        idx    = int((len(x3)/2)-(j/2))
        cdwave = 0.0
        for i in range(1,idx+1):
            ds = -integrate.simps(x3[i-1:i+1],y3[i-1:i+1])
            if airprop['cruise']['mach'] > mcr[i]:
                cdwave = cdwave + 20.0* np.power((airprop['cruise']['mach'] - \
                                              mcr[i]),4.0)                  * \
                                              ds / self.geo['wing']['sref']
                aux5=20.0* np.power((airprop['cruise']['mach'] - \
                                              mcr[i]),4.0)
                #print(self.avl_y[i],aux5,ds)

        self.drag['wing']['wave'] = 2.0*cdwave
#
#---- Print the Induced drag...

        print('   CD_Wave Wing [counts]    --> ' + "{0:.1f}".      \
                                    format(self.drag['wing']['wave']*10000)) 

        """
        Checking the wave drag for different mach number..saity check...
        mach = np.arange(0.60,0.98,0.02)
        for item in mach:
            cdwave = 0.0
            for i in range(1,idx+1):
                ds = -integrate.simps(x3[i-1:i+1],y3[i-1:i+1])
                if item > mcr[i]:
                    cdwave = cdwave + 20.0* np.power((item - mcr[i]),4.0) *  \
                                              ds / self.geo['wing']['sref']
            
            print(item,2.0*cdwave*10000)

         """

#        I2 = integrate.simps(x3[0:idx],y3[0:idx])
 #       print(np.trapz(x3[0:idx],y3[0:idx]))
#        print(x3[0:idx])