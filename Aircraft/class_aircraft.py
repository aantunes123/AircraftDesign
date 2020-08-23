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


                         CLASS CREATE_AIRCRAFT
                        ----------------------

    Here I am importing the different implemented classes. Notice that the
    Class Create_Aircraft recieves by Heritance many other classes.
 
    In this class I am calling the respective methods from the different
    classes. The order these methods are invoked should be in a logical way 
    one would perform an aircraft analysis.
    
    The idea here is to avoid the user to have some deep knowledge about
    the entire code. In this sense the Class Create_Aircraft does the 
    dirty work behind the scenes. The user can only change the main code
    to setup the analysis or optimization stydy.
    
    In case the user would like to perform modifications then he/she should
    knows in details what is implemented here and on the other classes.
    
"""

from Geometry.Wing.class_wing import Create_Wing
from Geometry.Horizontal.class_horizontal_tail import Create_Horizontal
from Geometry.Vertical.class_vertical_tail import Create_Vertical
from Geometry.Fuselage.class_fus import Create_Fuselage
from Geometry.Nacelle.class_nacelle import Create_Nacelle
from Geometry.Pylon.class_pylon import Create_Pylon
from Geometry.HighLift.class_highlift import Create_HighLift
from Aerodynamics.class_aerocoef import Coefficients
from Performance.class_performance import Performance
from Propulsion.class_propulsion import Propulsion
from Flight_Mechanics.class_mechanics import Flight_Mechanics
from Weight.class_weight import Weight
from Operation.class_operation import Oper_Items
from Plotting.plot import Rendering


from scipy.optimize import fmin
#from Writting.class_writting import Tee
#import sys
import os

#----------------------------------------------------------------------#
#                         AIRCRAFT  CLASS                              #
#----------------------------------------------------------------------#


class Create_Aircraft(Create_Wing,
                      Create_Horizontal,
                      Create_Vertical,
                      Create_Fuselage,
                      Create_Nacelle,
                      Create_Pylon,
                      Create_HighLift,
                      Coefficients,
                      Weight,
                      Performance,
                      Propulsion,
                      Oper_Items,
                      Flight_Mechanics):

    # Printing the Dictionaries from the Class Create_Aircraft
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# Initializing the Classes...
    def __init__(self, *args, **kwargs):

        # Getting the Flag to print the data in the screen...

        self.screen_flag = kwargs['Screen']
        self.render      = kwargs['Render']

# Initializing the Dictionaries....
        self.geo        = {}
        self.weight     = {}
        self.mechanics  = {}
        self.perf       = {}
        self.operating  = {}
        self.propulsion = {}

        super(Create_Aircraft, self).__init__(self.geo,
                                              self.weight,
                                              self.perf,
                                              self.operating,
                                              self.mechanics,
                                              self.propulsion,
                                              *args, **kwargs)

# This file contains the output information from the performed analysis.

        name = 'aircraft.out'

# Deleting the file if it exists...
        if os.path.isfile(name):
            os.remove(name)

# Here I am creating the object Tee to send the printing to computer screen
# to file: 'aircraft.out'

       # self.f = open(name,'w')
       # sys.stdout = Tee(sys.stdout, self.f)
        if self.screen_flag == True:
            print('|----------------------------------------------------------------------------|')
            print('|   ___  _                     __ _    ______          _                     |')
            print('|  / _ \(_)                   / _| |   |  _  \        (_)                    |')
            print('| / /_\ \_ _ __ ___ _ __ __ _| |_| |_  | | | |___  ___ _  __ _ _ __          |')
            print('| |  _  | |  __/ __|  __/ _  |  _| __| | | | / _ \/ __| |/ _  |  _ \         |')
            print('| | | | | | | | (__| | | (_| | | | |_  | |/ /  __/\__ \ | (_| | | | |        |')
            print('| \_| |_/_|_|  \___|_|  \__,_|_|  \__| |___/ \___||___/_|\__, |_| |_|        |')
            print('|                                                         __/ |              |')
            print('|                                                        |___/               |')
            print('|                                                                            |')
            print('|                                                                            |')
            print('|                        Created : Sept  2017                                |')
            print('|                                                                            |')
            print('| Developers:                                                                |')
            print('|                                                                            |')
            print('| Alexandre Antunes - alexandre.pequeno.antunes@gmail.com                    |')
            print('|                                                                            |')
            print('|----------------------------------------------------------------------------|')
            print(' ')
        else:
            print('  Running without outputing information to screen. ')

# Closing the Output File
#        self.f.close()

# ------------------------------------------------------------------------------
    def Compute_Geometry(self):
        """

            This method calls some of the implemented methods that are
            defined inside the Classes WING, HT, VT, FUSELAGE. 

            The reason to call these methods here is to obtain the data 
            for the Planform for some of the components from the aircraft:

                - Wing
                - HT
                - VT

            Moreover, it is also desired to get other geometric information
            to obain the aerodynamic coefficients using lower-medium 
            fidelity methods.

            In the future this method should have some checks about what
            type of analysis is intended to be performed in order to not 
            call all the implemented methods in the above mentioned 
            Classes.
        """

# Calling the Method to Compute the Wing Reference Planform data.
        self.Wing_Reference_Planform()

# Calling the Method to Compute the Wing Planform data with a TE Kink.
        self.Wing_TE_Kink()

# Calling the Method to Compute the HT Reference Planform data.
        self.Horz_Planform()

# Calling the Method to Compute the VT Reference Planform data.
        self.Vert_Planform()
        # self.Vert_Profile()

# Calling the Method to Compute the Fuselage Geometry - Class Create_Fuselage.
        self.Fus_Torenbeek()

# Calling the Method to Compute the Nacelle Geometry - Class Create_Nacelle.
        self.Nacelle()

# Calling the Method to Compute the Pylon Geometry - Class Create_Pylon.
        self.Pylon()

# Calling the Method to Compute the Flap Geometry - Class Create_Flap.
        self.Flaps_Slats()
        
# Calling the rendering Method
        if self.render == True:
            Rendering(self)

#
#---- Printing data
        if self.screen_flag == True:
            self.Print_HTGeo()
            self.Print_WingGeo()    
            self.Print_VerticalGeo()
            self.Print_Pylon()
            self.Print_Nacelle()            
      
    pass
# ------------------------------------------------------------------------------

    def Converge_Weight(self, mtow0,*args):
        """
            This method calls those other methods that are available inside
            the Class Weight. 

            The methods in the Class Weight are mnemonic in the sense
            that the name of the method already defines for what
            weight component is being computed.

        """
        self.weight['mtow'] = mtow0
        airprop             = args[0]
        
# Fuel Tank Weight.
        self.Fuel_Tank_Weight()
        
# Usuable Fuel...
        self.Usable_Fuel_Weight(airprop)
        
# Horizontal Tail Weight.
        self.HT_Weight(airprop)

# Vertical Tail Weight.
        self.VT_Weight(airprop)

# Payload Weight.
        self.Payload_Weight()

# Landing Gear Weight.
        self.LG_Weight()

# Operational Weight.
        self.Operational_Weight()

# Fuselage Weight.
        self.Fus_Weight(airprop)

# Miscellaneous Weight.
        self.Miscellaneous_Weight()

# Wing Weight.
        self.Wing_Weight()

# Pylon Weight.
        self.Pylon_Weight()        

# high-Lift Weight.
        self.HighLift_Weight()

# Performing the computation of the initial total weight.
        self.Total_Weight()

#  Returning the difference between the imposed maximum take-off weight 
#  and the MTOW computed by the methods above called. This difference must
#  be equal to zero.... 
#

        return abs(self.weight['total'] - self.weight['mtow'])

# -----------------------------------------------------------------------------
    def Compute_Weight(self,airprop):
        """
            This method perform the iterative process to get the MTWO of the 
            aircraft. It starts with a very low MTOW and keep raising until the
            guess MTOW converges to the right value. Here the concept is the
            one described on ROSKAN book No.02.
        
        """
        print(' ')
        print('Converging MTOW....Roskan concept')
        print(' ')
        
        fmin(self.Converge_Weight,52000,args=(airprop,),maxiter = 1000,ftol=2.0) 
        print(' ')        

#
#---- Printing data
        if self.screen_flag == True:
            self.Print_Weight()
            
# -----------------------------------------------------------------------------
    def Compute_Drag(self, airprop):
        """
            Computing the Drag of the aircraft components using 
            semi-empirical methods defined in the Class Aerodynamics

        """

#        phases    = ('climb','cruise','landing')
        phases = ('cruise')

        self.FrictionDrag(airprop, phases)
        self.InducedDrag(airprop,phases)
        self.WaveDrag(airprop,phases)

#
#---- Printing data
    #    if self.screen_flag == True:
    #       self.Print_Weight()

# -----------------------------------------------------------------------------
    def Geometry_Weight_Drag(self,airprop):
        """
            This method calls other methods to compute the Geometry, the Weight 
            and the Drag. It is an iteractive process. An initioal value for 
            the L/D is assumed and then it is computed the fuel weight to 
            accomplish the mission. This implies in a certain MTOW value and, 
            thus, we can get the induced drag (the CL is defined at the cruise
            mission phase). Once value for the induced drag is obtained
            we can compose the total drag and obtain the new L/D and go back
            to compute the mission fuel weight and so one. Notice that the L/D
            is being considered just for the cruise phase. The other phases are
            computed using the fule mass fraction concept described on the 
            Roskan books. The process should converge in two or three 
            iteractions. No more then this!        
        
        """
        error = abs(self.perf['ld'] - self.perf['ld_old'])


# Computing the Geometry outside the looping because the convergence is for the
# l/D for a given geometrical configuration. The propulsion system must be
# insied the looping because in the future it will update the SFC coefficient.

        self.Compute_Geometry()

# Looping to update the L/D....
        while error > 0.2:

            self.Compute_Weight(airprop)     # Computing the Weight.
            self.Compute_Drag(airprop)       # Computing the Drag.
            self.Compute_Propulsion()        # Computing the Propulsion System.
            
            #error = abs(self.perf['ld'][0]-self.perf['ld_old'])
            error = abs(self.perf['ld']-self.perf['ld_old'])
# -----------------------------------------------------------------------------

    def Compute_Flight_Mechanics(self):
        """
            Computing the necessary data to perform the Flight Mechnics 
            analyses. 

            The Class Flight Mechanics must be implemented.

        """

        self.Trim()

# -----------------------------------------------------------------------------

    def Compute_Performance(self):
        """
            Computing the perforamnce computation.

            The Class Performance must be implemented.

        """
        self.Compute_Mission()


# -----------------------------------------------------------------------------

    def Compute_Propulsion(self):
        """
            Computing the perforamnce computation.

            The Class Performance must be implemented.

        """
        self.RubberEngine()

# -----------------------------------------------------------------------------

    def Destructor(self):
        """
            Computing the Drag of the aircraft components.
        """

        print('Closing files...')
        self.f.close()
