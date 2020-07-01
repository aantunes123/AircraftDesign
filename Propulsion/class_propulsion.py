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
class Propulsion(object, metaclass=AuxTools):
    """

       Any method associated with the propulsion system should be implemented
       on this class. The methods can be encapsulated on the Created_Aircraft
       class or simply adopted on the aircraft_setup to define the optimization
       problem.
        
    """
        
    def __init__(self, geo,*args, **kwargs):
        super(Propulsion, self).__init__(geo,*args, **kwargs)

        if 'Fprop' not in kwargs:
            raise ValueError("Cannot initiate Propulsion...provide the \
                              argument Fprop = 'file_name'.")            
        self.file_name = kwargs['Fprop'] 
        
# Data for the wing...some setup to avoid crashing

        self.propulsion = {}  
        self.propulsion['weight']  =   63000.00
        self.propulsion['sfc']     =       0.45
        self.propulsion['thrust']  =   93450.00
        self.propulsion['bypass']  =      11.00

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
            for key in (self.propulsion):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.propulsion[key] = float(vvals[i])       


#------------------------------------------------------------------------------    
    def RubberEngine(self):    
        
        pass
        
        
        
        