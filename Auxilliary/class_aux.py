#-----------------------------------------------------------------------------#
#   Program to compute the aircraft weight.                                   #
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

class AuxTools(type):
    """
      Class with miscellaneous methods...

    """

    def Interp(cls,c,a,b):
        
        x=np.zeros(len(a))
        y=np.zeros(len(b))
        
        for i in range(0,len(a)):
            x[i] = float(a[i])
            y[i] = float(b[i])            

        c = np.interp(c,x,y)

        return c

    def __str__(cls):
        return '%s as interpolate' % (cls.__name__,)

    def __repr__(cls):
        return '<class %s as interpolate>'%cls.__name__    
    

