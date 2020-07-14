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


def Flight_Setup(file_name):
        """
            This subroutine generates a dictionary with the atmospheric 
            properties and return this information to atmos variable in 
            main code.
            
            Because I need data at different flight phases I am going to 
            create a dictionary to each flight phase.
        """
#
#-- Dictionary with the flight condition properties...
        flight                  = {}   
        flight['climb']         = {}                   
        flight['cruise']        = {}                           
        flight['landing']       = {}                                   
        
# Items that I am going to add to each above defined dictionary.. in the future
# if someone wants to have additional atmospheric property it should definde
# here the property...
        dict_item = ( 'flag'          ,                                       \
		               'altitude'      ,                                       \
                      'velocity'      ,                                       \
                      'isa'           ,                                       \
                      'vcas'          ,                                       \
                      'temp_celsius'  ,                                       \
                      'temp_kelvin'   ,                                       \
                      'p_pref'        ,                                       \
                      't_tref'        ,                                       \
                      'ro_roref'      ,                                       \
                      'pressure'      ,                                       \
                      'density'       ,                                       \
                      'kin'           ,                                       \
                      'kin_vis'       ,                                       \
                      'veas'          ,                                       \
                      'vtas'          ,                                       \
                      'akts'          ,                                       \
                      'mach'          ,                                       \
                      'vsound'        ,                                       \
                      'q'
                    )
        
# Adding the above items to each dict that represents different flight phases..        
        for keys in flight:
            for i in range(0,len(dict_item)):
                flight[keys].setdefault(dict_item[i],float('5.0'))

#--- Reading the input data for the Flight Phases...
        f = open(file_name,'r')             
        chunck = [line.split() for line in f if line.strip()[0] != '#']
        f.close()

#--- List to inform the order in the Input file and the variabl names...
        vvars   = ('flag','altitude','velocity','mach','isa')
        j = 0

#--- Here I am attributing the data from the input file to the respective
#    dictionary...

        for keys in flight:
            for i in range(0,len(vvars)):
                flight[keys][vvars[i]] = float(chunck[j][i])

            j  += 1

#  LOOPING OVER THE FLIGHT PHASES TO GET THE ATMOSPHERIC PROPERTIES....
        for keys in flight:

## Initial Vtrue based on the VCAS initial....
            if flight[keys]['flag'] == 0:  
                vtarget0  = flight[keys]['velocity']         
#            
            if flight[keys]['flag'] == 1: 
                mtarget0  = flight[keys]['mach']         
#
##
##--- Computing the properties...
            if (flight[keys]['altitude'] > 36089.0):
                flight[keys]['temp_celsius'] = -56.5 + flight[keys]['isa']
                
                flight[keys]['temp_kelvin']  = flight[keys]['temp_celsius'] + \
                                               273.15
                                               
                flight[keys]['p_pref']       = 0.22336*np.exp(-0.0000480634 * \
                                                 (flight[keys]['altitude']  - \
                                                  36089))
            else:
                flight[keys]['temp_celsius'] = ((1.0 - 0.00000687535        * \
                                           flight[keys]['altitude'])*288.15)- \
                                           273.15 + flight[keys]['isa']
#                
                flight[keys]['temp_kelvin']  = flight[keys]['temp_celsius'] + \
                                               273.15
#                
                flight[keys]['p_pref']       = (1.0 - 0.00000687535         * \
                                          flight[keys]['altitude'])**5.2561
#
            vtarget1, mtarget1 = Converge(keys,flight)
#
## Checking the error...First iteration...
            if flight[keys]['flag'] == 0:          
                eps  = abs(vtarget0-vtarget1)
#
            if flight[keys]['flag'] == 1: 
                eps  = abs(mtarget0-mtarget1)
#
##---  Looping in VCAS to get the imposed VTRUE:
##     Notice the EPS limits for flag=0 is different from flag=1
#
            if flight[keys]['flag'] == 0: 
                k    = 0
                while(eps > 0.1):
                    flight[keys]['vcas']      = flight[keys]['vcas'] + 0.1
                    vtarget1,mtarget1   = Converge(keys,flight)
                    eps  = abs(vtarget0-vtarget1)
                    k                  += 1
#
                    if(k>50000):
                        break
#
##---  Looping in VCAS to get the imposed Mach Number:
            if flight[keys]['flag'] == 1:          
                k    = 1
                while(eps > 0.0001):
                    flight[keys]['vcas']      = flight[keys]['vcas'] + 0.05
                    vtarget1,mtarget1   = Converge(keys,flight)
                    eps  = abs(mtarget0-mtarget1)
                    k                  += 1
#
                    if(k>50000):
                        break
#
#--- Printing the Data...

            print('Atmospheric Properties  : ',keys,' condition.')
            print('------------------------------------------------')
            print('   Altitude     [Ft]      --> ' + "{0:.3f}".format(        \
                                                     flight[keys]['altitude']))
          
            print('   Mach         [-]       --> ' + "{0:.3f}".format(        \
                                                         flight[keys]['mach']))
          
            print('   V_True       [m/s]     --> ' + "{0:.3f}".format(        \
                                                     flight[keys]['velocity']))      
          
            print('   Pressure     [Pa]      --> ' + "{0:.3f}".format(        \
                                                     flight[keys]['pressure']))         
          
            print('   Density      [Kg/m3]   --> ' + "{0:.3f}".format(        \
                                                      flight[keys]['density']))            
          
            print('   Viscosity    [Kg/ms]   --> ' + "{0:.3e}".format(        \
                                                         flight[keys]['visc']))
          
            print('   Temperature  [K]       --> ' + "{0:.3f}".format(        \
                                                  flight[keys]['temp_kelvin']))              
          
            print('   Temperature  [C]       --> ' + "{0:.3f}".format(        \
                                                 flight[keys]['temp_celsius']))
          
            print('   Delta_ISA    [C]       --> ' + "{0:.3f}".format(        \
                                                          flight[keys]['isa']))
          
            print('   KCAS         [Knot]    --> ' + "{0:.3f}".format(        \
                                                         flight[keys]['vcas']))  
          
            print('   VEAS         [Knot]    --> ' + "{0:.3f}".format(        \
                                                         flight[keys]['veas']))
          
            print('   VKTAS        [Knot]    --> ' + "{0:.3f}".format(        \
                                                         flight[keys]['vtas']))
          
            print('   AKTS         [Knot]    --> ' + "{0:.3f}".format(        \
                                                         flight[keys]['akts']))
          
            print('   VSound       [m/s]     --> ' + "{0:.3f}".format(        \
                                                       flight[keys]['asound']))
            
            print('   Q            [Kgf/m2]  --> ' + "{0:.3f}".format(        \
                                                            flight[keys]['q']))        
          
            print('   P_ref        [Pa]      --> ' + "{0:.3f}".format(        \
                                                       flight[keys]['p_pref']))    
          
            print('   T_ref        [K]       --> ' + "{0:.3f}".format(        \
                                                       flight[keys]['t_tref']))      
          
            print('   R_ref        [Kg/m3]   --> ' + "{0:.3f}".format(        \
                                                     flight[keys]['ro_roref']))      
          
            print('   Kin          [-]       --> ' + "{0:.3e}".format(        \
                                                          flight[keys]['kin']))             
          
            print('   Kin_Visc     [m2/s]    --> ' + "{0:.3e}".format(        \
                                                      flight[keys]['kin_vis']))
       
            print('                                                          ')        

        return flight       
#    
##----------------------------------------------------------------#
##                Method to converge the VTRUE.                   #
##----------------------------------------------------------------#
def Converge(keys,flight):
    
#
#  Computing the properties

    flight[keys]['t_tref']   = (flight[keys]['temp_celsius']+273.15)/288.16
         
    flight[keys]['ro_roref'] = flight[keys]['p_pref']/flight[keys]['t_tref']
                  
    flight[keys]['pressure'] = 101325.0 * flight[keys]['p_pref']
         
    flight[keys]['density']  = 1.225 * flight[keys]['ro_roref']
         
    flight[keys]['kin']      = ((flight[keys]['temp_celsius']+273.15)**1.5)/  \
                               ((flight[keys]['temp_celsius']+273.15+110.4)*  \
                                 12.2732*flight[keys]['ro_roref'])
                               
    flight[keys]['kin_vis']  = 0.000014607*flight[keys]['kin']
         
    flight[keys]['visc']     = flight[keys]['density']*flight[keys]['kin_vis']
         
    flight[keys]['veas']     = 1479*(flight[keys]['p_pref']*(((((((1.0+0.2 *  \
                              (flight[keys]['vcas']/661.5)**2.0)**3.5)-1.0)/  \
                               flight[keys]['p_pref'])+1.0)**(1.0/3.5))-1.0)) \
                                **0.5
         
    flight[keys]['vtas']     = flight[keys]['veas']/(flight[keys]['ro_roref'] \
                               **0.5)
         
    flight[keys]['akts']     = 661.5*flight[keys]['t_tref']**0.5
         
    flight[keys]['mach']     = flight[keys]['vtas']/flight[keys]['akts']
         
    flight[keys]['velocity'] = flight[keys]['vtas']*0.514444444444444
         
    flight[keys]['q']        = 0.5*flight[keys]['density']  *                 \
                                   flight[keys]['velocity'] *                 \
                                   flight[keys]['velocity']

    flight[keys]['asound']   = flight[keys]['velocity']/flight[keys]['mach']
    
    return flight[keys]['velocity'], flight[keys]['mach']

         



