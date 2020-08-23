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

                        ----------------------
                          CLASS Performance  
                        ----------------------

    This class is responsible to compute the fuel burn necessary to
    accomplish the flight mission.
 

"""

from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                        PERFORMANCE  CLASS                            #
#----------------------------------------------------------------------#
class Performance(object, metaclass=AuxTools):
    """
        Initialization of the Class and reading the input file
        with the weight mass fractions for each flight phase.
    """
   
    def __init__(self, geo,*args, **kwargs):
        super(Performance, self).__init__(geo,*args, **kwargs)
        
        if 'Fperf' not in kwargs:
            raise ValueError("Cannot initiate Performance...provide the       \
                              argument Fperf = 'file_name'.")            
        self.file_name = kwargs['Fperf']

        self.perf['vd']           =  380.0
        self.perf['climb_time']   =   33.0
        self.perf['range']        = 2200.0
        self.perf['fuel_reserve'] =    1.000
        self.perf['warm_wf']      =    0.990
        self.perf['taxi_wf']      =    0.990
        self.perf['takeoff_wf']   =    0.995
        self.perf['climb_wf']     =    0.980
        self.perf['descend_wf']   =    0.990
        self.perf['land_wf']      =    0.992
        self.perf['ld']           =   13.000

# Set up an initial value for the L/D ratio at an previous convergence step. 
        self.perf['ld_old']       =    1.0
        
        vvars = list()
        vvals = list()
 
### Input file for the wing...
        f = open(self.file_name,'r')              
        for line in f:
            if(line[0] != '#' and line.isspace() == False):
                try:
                    vvars.append(line.strip().split('=')[0])
                    vvals.append(line.strip().split('=')[1])
                except:
                    pass
        f.close()

#--- Updating the variables...
        for i in range(0,len(vvars)):
            for key in (self.perf):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.perf[key] = float(vvals[i])

#------------------------------------------------------------------------------    
    def Compute_Mission(self):
        
        pass