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

        self.drag = {}
        if 'Method' not in kwargs:
            raise ValueError("Cannot initiate Aerodynamic computation. Provide\
                              the  argument Method = 'Torenbeek'.")            
        self.method = kwargs['Method']
        

#----------------------------------------------------------------------#
#                    Computing the Wing  Drag                          #
#----------------------------------------------------------------------#
    def FrictionDrag(self,airprop,Acomp,Fphase):
        """
            Acomp    --> Aircraft Components.
            Fphase   --> Flight Phase.
        """
        
        if self.screen_flag == True:
            print('  |-------------------------------------------------|')
            print('  |            Friction  Drag  Component            |')            
            print('  |-------------------------------------------------|')

# Loping over the Components...

        for item in enumerate(Acomp):
#
#--- Variables present in most of the methods...
            cs    = np.cos(self.geo[item[1]]['sweep14']*np.pi/180.0)
            asom  = np.sqrt(1.40 * 287.074 * airprop[Fphase]['temp_kelvin'])
            reym  = airprop[Fphase]['mach'] * asom *                          \
                    airprop[Fphase]['density'] / airprop[Fphase]['visc']

#----
#      Lift correction from the Roskan book VI pg 24 figure 4.2, I did 
#      considered a average value from the sum of the curves from 3 Mach
#      numbers (.25, .60 and .80) and adopted the polynomial regression
#      to obtain the RLS value.

# Reynolds number...
            rey              = reym * self.geo[item[1]]['cma']               

# Skin Friction...            
            self.drag['cf']  = 0.455/((np.log10(rey))**2.58)
            
            rls              = -2.1851*(cs)**3.0 + 3.9364*(cs)**2.0 -         \
                                1.5551*cs + 0.9623
                                
            self.drag['cdo'] =  rls * self.drag['cf'] * (1.0 + 1.2  *         \
                                self.geo[item[1]]['tcave'] + 100    *         \
                               ((self.geo[item[1]]['tcave'])**4.0)) *         \
                                 self.geo[item[1]]['swet'] /                  \
                                 self.geo['wing']['sref']
#
#---- Plotting the computed data...
            if self.screen_flag == True:
                print('   CDo '+item[1]+' [counts]    --> ' + "{0:.1f}".      \
                                                format(self.drag['cdo']*10000))

        pass
