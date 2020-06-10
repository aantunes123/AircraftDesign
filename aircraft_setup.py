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

    DEVELOPERS:                              
    
    Alexandre Antunes - alexandre.pequeno.antunes@gmail.com
            
                         ---------------------
                                 MAIN         
                         ---------------------

    This is the method that starts the enitre set of numerical
    computation.

    Last Modification:...................01/03/2020 - Alexandre Antunes    
"""

from Flight_Conditions.flight_cond import Flight_Setup
from Aircraft.class_aircraft import Create_Aircraft
from Plotting.plot import Plot_Figure
#from Optimization.GA_Class import Simple_GA
#from Optimization.GA_Setup import GA_Setup
#import scipy
#from scipy.optimize import minimize
#import pprint


# -----------------------------------------------------------------------------
def Aircraft_Opt(x):
    """
        This method defines the optimization problem. Thus, the user
        must select the objective function and perform the setup of
        the input file from the GA algorithm to specify the range of 
        the design variables.
    """
    p100.geo['wing']['sref'] = float(x)

# Computing the Geometry of the Wing, Horizontal tail, Vertical Tail, Fuselage.
    p100.Compute_Geometry()
    p100.Fuel_Tank_Weight()

    return p100.geo['wing']['vol']


pass


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # Creating the Aircraft Object using the Input Files from the respective
    # components....
    p100 = Create_Aircraft(Fwing='.\\Input_files\\wing_w65.inp',
                           Fhorz='.\\Input_files\\horz_h30.inp',
                           Fvertical='.\\Input_files\\vert_v20.inp',
                           Fus='.\\Input_files\\fuselage_f40.inp',
                           Fnacelle='.\\Input_files\\nacelle_n10.inp',
                           Fpylon='.\\Input_files\\pylon_p5.inp',
                           Fperf='.\\Input_files\\performance.inp',
                           Foper='.\\Input_files\\operating.inp',
                           Fprop='.\\Input_files\\propulsion.inp',
                           Method='Torenbeek',
                           Screen=True
                           )

# Flight Conditions and computing the Atmospheric Properties
    atmos = Flight_Setup('.\\Input_files\\flight_cond.inp')

# Computing the Geometry of the Wing, Horizontal tail, Vertical Tail, Fuselage.
    p100.Compute_Geometry()

# Computing the Weight...
    p100.Compute_Weight(atmos)

# Computing the Drag....
    p100.Compute_Drag(atmos)

    print(p100.weight['fus'])
    # print(p100.__str__())
# Computing the Flight Mechanics....
# p100.Compute_Flight_Mechanics()


# ---------------------  Optimization GA Here ----------------------------------

    # gen_vals = GA_Setup()                          # Input File: 'ga_setup.inp'
    # ga       = Simple_GA(*gen_vals)                # Creating the Object ga

    # ga.Opt_SGA(Aircraft_Opt)                       # Calling the SGA Method

# ---------------------  Optimization Gradient Here ----------------------------
    #x = 120.0
    # res = minimize(Aircraft_Opt, x, method='BFGS', bounds=((112.0,120.0)),    \
    #      options={'gtol': 1e-6, 'disp': True, 'iprint': 1, 'eps': 0.05,      \
    #                'maxiter': 400})

# Plotting the Geometry
    Plot_Figure(True, 3, p100)

# Deleting the Object...
   # p100.Destructor()

# Printing the variables from the respective objects...
   # attrs = vars(p100)
   # pprint.pprint(attrs,width=1)

#    print(atmos.items())
# print(p100.geo['wing'].items())
#    print(p100.geo['horz'].items())
#    print(p100.geo['fus'].items())
