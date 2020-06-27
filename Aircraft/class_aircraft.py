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
    classes in a logical way one would perform an aircraft analysis.
    
    The idea here is to avoid the user to have some deep knowledge about
    the entire code. In this sense the Class Create_Aircraft does the 
    dirty work behind the scenes.
"""

from Geometry.Wing.class_wing import Create_Wing
from Geometry.Horizontal.class_horizontal_tail import Create_Horizontal
from Geometry.Vertical.class_vertical_tail import Create_Vertical
from Geometry.Fuselage.class_fus import Create_Fuselage
from Geometry.Nacelle.class_nacelle import Create_Nacelle
from Geometry.Pylon.class_pylon import Create_Pylon
from Aerodynamics.class_aerocoef import Coefficients
from Performance.class_performance import Performance
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
                      Coefficients,
                      Weight,
                      Performance,
                      Oper_Items,
                      Flight_Mechanics):

    # Printing the Dictionaries from the Class Create_Aircraft
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# Initializing the Classes...
    def __init__(self, *args, **kwargs):

        # Getting the Flag to print the data in the screen...

        self.screen_flag = kwargs['Screen']

# Initializing the Dictionaries....
        self.geo = {}
        self.weight = {}
        self.mechanics = {}
        self.perf = {}
        self.operating = {}

        super(Create_Aircraft, self).__init__(self.geo,
                                              self.weight,
                                              self.perf,
                                              self.operating,
                                              self.mechanics,
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
            print('|                        Last Modification: Sept  2017                       |')
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
       # self.Nacelle()

# Calling the Method to Compute the Pylon Geometry - Class Create_Pylon.
       # self.Pylon()

# Calling the rendering Method
      #  Rendering(self)

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

# Fuel Tank Weight.
        self.Fuel_Tank_Weight()

# Miscellaneous Weight.
        self.Miscellaneous_Weight()

# Wing Weight.
        self.Wing_Weight()

# Performing the computation of the initial total weight.
        self.Total_Weight()

#  Returning the difference between the imposed maximum take-off weight 
#  and the MTOW computed by the methods above called. This difference must
#  be equal to zero.... Another important check is the difference between the 
#  wing fuel capacity and the requirent fuel to accomplish the mission.
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
        fmin(self.Converge_Weight,3000,args=(airprop,),maxiter = 1000,ftol=2.0)         

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
        phases = ('landing')

        self.FrictionDrag(airprop, phases)

#
#---- Printing data
    #    if self.screen_flag == True:
    #       self.Print_Weight()


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

        self.Converge_MTOW()

# -----------------------------------------------------------------------------

    def Destructor(self):
        """
            Computing the Drag of the aircraft components.
        """

        print('Closing files...')
        self.f.close()
