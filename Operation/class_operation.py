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


                         CLASS Oper_Items
                        ----------------------

    This class is responsible to define the flight mission and the 
    mass-fraction for each phase of the flight.
 

"""

#----------------------------------------------------------------------#
#                     OPERATING ITEMS CLASS                            #
#----------------------------------------------------------------------#
class Oper_Items(object):
    """
        
        Initializing the Class...
        
    """
   
    def __init__(self,geo,weight,*args, **kwargs):
        super(Oper_Items, self).__init__(geo,*args, **kwargs)

        if 'Foper' not in kwargs:
            raise ValueError("Cannot initiate operating data for the aircraft.\
                              Provide the argument Foper = 'file_name'.")            
        self.file_name = kwargs['Foper']       

        self.operating['no_pass']        =   113
        self.operating['ncrew']          =     3
        self.operating['pass_weight']    =   100.0        
        self.operating['freight_weight'] =  1200.0   
        self.operating['mtow']           = 52000.0           

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
            for key in (self.operating):
                if str(vvars[i].strip()) == str(key.strip()):
                    self.operating[key] = float(vvals[i])
        print(self.operating['ncrew'])
        pass   
