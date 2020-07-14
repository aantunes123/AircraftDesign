# -*- coding: utf-8 -*-
"""
 
    Code   :  Aircraft Design (03/02/2017)                                              
    Created:  14/07/2020
    Licence:  GNU AGPLv3                                                        
                                                                             
    Permissions of this strongest copyleft license are conditioned             
    on making available complete source code of licensed works and             
    modifications, which include larger works using a licensed work,           
    under the same license. Copyright and license notices must be 
    preserved. Contributors provide an express grant of patent rights.
    When a modified version is used to provide a service over a 
    network, the complete source code of the modified version must 
    be made available.
    
    
"""   
from time import time

# -----------------------------------------------------------------------------
def Performance(fn):
    """
        Decorator to measure the total time spend on the computation:
        Analysis or Optimization.
       
    """
    def wrapper(*args, **kargs):
        t1 = time()
        result = fn(*args, **kargs)
        t2 = time()
        print(f'Computation time ', '{:02.6f}'.format(t2-t1),' seconds')
        return result
    return wrapper