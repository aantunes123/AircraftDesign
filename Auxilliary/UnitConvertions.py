# -*- coding: utf-8 -*-
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
                             CLASS WEIGHT
                        ----------------------

    This Class computes the weight for different components from the 
    aircraft. At the present moment, most of the computation is done
    with the Torenbeek method, but in the future other methods shall
    be part of the class.

    Created on Thu Jul 16 10:40:03 2020

"""
def Units(inn,out):
    
    if inn == 'inch' and out == 'meters':
        return 0.0254
        
    if inn == 'meters' and out == 'inch':
        return 39.3701
    
   


