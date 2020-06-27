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
from Auxilliary.class_aux import AuxTools

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

            self.drag[item] = {}            
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

#---- Fuselage
            fac  = 0.05

#
#----  Drag computation  -        ROSKAN   -

            fus_diameter_base  = fac * self.geo['fus']['diameter']
            fus_area_base      = np.pi*(fus_diameter_base**2.0)/4.0
            fus_area           = np.pi*(self.geo['fus']['diameter']**2.0)/4.0
           
            reyfus    = reym * self.geo['fus']['fus_length']

            cffus     = 0.455/((np.log10(reyfus))**2.580) 

            cdofus    = cffus * ( (1.0 +60.0/(self.geo['fus']['esb']**3.0))     +   \
                                          0.0025*self.geo['fus']['esb']) *    \
                                         (self.geo['fus']['swet']        /    \
                                          self.geo['wing']['sref'])
                                         
            cdobfus   = cffus*(fus_area_base/self.geo['wing']['sref'])
           
            cdbfus    = ((0.029*(fus_diameter_base/                           \
                                 self.geo['fus']['diameter'])**3.0) /         \
                                  (cdobfus*(self.geo['wing']['sref']/fus_area))**0.5) *      \
                                   (self.geo['fus']['swet']/                  \
                                    self.geo['wing']['sref'])
                                         
            self.drag['fus']['cdo'] =  cdofus + cdbfus
           
            print('Fuselagem: ', self.drag['fus']['cdo'])

            """
            PILONE           
           
           cs   = cos(pyl_sweep*pi/180.0d0)
!
!---  Wing Reynolds number.
!              
           reypyl = reyms * pyl_cma
!
!---   Skin friction of the pylon...
!           
           cfpyl  = 0.455d0/((log10(reypyl))**2.580d0)                     
!
!----  Pylon Form Factor
!
           FFpyl  = 1.0d0 + ( (2.7d0*pyl_tc + 100.0d0*pyl_tc**4.0d0) * (cs**.25d0) )
!
!----  Drag
!            
           cdopyl_torennbeek  = nac_no * cfpyl * FFpyl * pyl_swet/wing_area           
           
           
           
                    NACELLE           
           
           reynac = reyms * nac_lmax 
!
!---   Skin friction of the pylon...
!           
           cfnac  = 0.455d0/((log10(reynac))**2.580d0)                     
!
!----  Pylon Form Factor
!
           FFnac  = 1.0d0 +  (2.7d0*nac_tc + 100.0d0*nac_tc**4.0d0)
!
!----  Drag
!            
           cdonac_torennbeek  = nac_no * cfnac * FFnac * nac_swet/wing_area           
           
           
           
           
           
           """           


#
#---- Plotting the computed data...
        if self.screen_flag == True:
            print('  |-------------------------------------------------|')
            print('  |            Friction  Drag  Component            |')            
            print('  |-------------------------------------------------|')
            
            for item in components:
                print('   CDo '+item[1]+' [counts]    --> ' + "{0:.1f}".      \
                                          format(self.drag[item]['cdo']*10000))

        pass
