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

                         CLASS Flight_Mechanics
                        -----------------------

    Here should come the flight mechnics implementation.
 
"""
from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                       FLIGHT MECHANICS CLASS                         #
#----------------------------------------------------------------------#
class Flight_Mechanics(object, metaclass=AuxTools):
    """
        Aircraft Weight - The call SUPER does not contains the *args, **kwargs 
        because it is the last Father Class passed to Aircraft Class.    
    """
        
    def __init__(self, geo,*args, **kwargs):
        super(Flight_Mechanics, self).__init__()        


    def Trim(self):

        self.mechanics['TailV'] = ( ((self.geo['horz']['xcma']          +     \
                                     (0.25*self.geo['horz']['cma']))    -     \
                                     (self.geo['wing']['xcma']          +     \
                                     (0.25*self.geo['wing']['cma'])))   *     \
                                      self.geo['horz']['sref'])         /     \
                                     (self.geo['wing']['xcma']          *     \
                                      self.geo['wing']['sref'])

        if self.screen_flag == True:        
            print('                                                     ')  
            print('  |-------------------------------------------------|')
            print('  |                 Flight Mechanics                |')
            print('  |-------------------------------------------------|')
            print('   Tail_Volume   [-]    --> ' + "{0:.3f}".                 \
                                               format(self.mechanics['TailV']))        
            print('                                                     ')        

    
