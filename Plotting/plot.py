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
    
    
"""    
from matplotlib import pyplot as plt
import airconics
from airconics import fuselage_oml
import airconics.AirCONICStools as act
from OCC.Display.SimpleGui import init_display
#import pprint


from airconics import liftingsurface, engine, fuselage_oml
import airconics.AirCONICStools as act
from airconics.Addons.WebServer.TornadoWeb import TornadoWebRenderer
from IPython.display import display


#def plot(flag_plot,flag_time,comp1,comp2):
def Plot_Figure(flag_plot,flag_time,comp1):    

#
#---- Plot Reference Wing...
    if flag_plot == True:
        yref1 = list()
        xref1 = list()

        ykink  = list()
        xkink  = list()
        zkink  = list()

        yht    = list()
        xht    = list()        

# Getting the Geometries from the object...
        for i in range(0,4):
            yref1.append(float(comp1.geo['wing']['y'][i]))
            xref1.append(float(comp1.geo['wing']['x'][i]))
            zkink.append(float(comp1.geo['Kink_wing']['zu'][i]))
            ykink.append(float(comp1.geo['Kink_wing']['y'][i]))
            xkink.append(float(comp1.geo['Kink_wing']['x'][i]))

        for i in range(0,3):
            yht.append(float(comp1.geo['horz']['y'][i]))
            xht.append(float(comp1.geo['horz']['x'][i]))

        for i in reversed(range(0,4,1)):                
            yref1.append(float(comp1.geo['wing']['y'][i]))
            xref1.append(float(comp1.geo['wing']['xte'][i]))
            zkink.append(float(comp1.geo['Kink_wing']['zl'][i]))
            ykink.append(float(comp1.geo['Kink_wing']['y'][i]))
            xkink.append(float(comp1.geo['Kink_wing']['xte'][i]))

        for i in reversed(range(0,3,1)):                            
            yht.append(float(comp1.geo['horz']['y'][i]))
            xht.append(float(comp1.geo['horz']['xte'][i]))

        fig = plt.figure(figsize=(8,8))
        plt.title('Aircraft Planform')
        plt.xlim([0,20])
        plt.plot(yref1,xref1)
        plt.plot(ykink,xkink)
        plt.plot(yht,xht)        
        plt.xlabel('y')
        plt.ylabel('X')
        plt.grid(True)
        fig.show()
        
        fig2 = plt.figure(figsize=(8,8))
        plt.title('Aircraft Planform')
        plt.xlim([0,20])
        plt.ylim([-4,4])        
        plt.plot(ykink,zkink)
        plt.xlabel('y')
        plt.ylabel('Z')
        plt.grid(True)
        fig2.show()
        
##        fig2 = plt.figure(figsize=(4,5))
##        plt.title('HT Planform')
##        plt.plot(yht,xht)
##        plt.xlabel('y')
##        plt.ylabel('X')
##        plt.grid(True)
##        fig2.show()

        
#        plt.savefig("test.png")
#        plt.pause(flag_time)
        #plt.close()

#------------------------------------------------------------------------------
def Rendering(obj):
   
    display, start_display, add_menu, add_function_to_menu = init_display()

# Printing the variables from the aircraft object...
#    attrs = vars(aircraft)
#    pprint.pprint(attrs,width=1)    


#-------------       WING    --------------------
# Add NACA 4 digit airfoils to loft between:

    x0 = float(obj.geo['Kink_wing']['x'][0])
    y0 = float(obj.geo['Kink_wing']['y'][0])
    z0 = 0.0
    c0 = float(obj.geo['Kink_wing']['chords'][0])
#    z0 = obj.geo['Kink_wing']['zu'][0]    

    x1 = float(obj.geo['Kink_wing']['x'][1])
    y1 = float(obj.geo['Kink_wing']['y'][1])
    z1 = 0.0
    c1 = float(obj.geo['Kink_wing']['chords'][1])
#
    x2 = float(obj.geo['Kink_wing']['x'][2])
    y2 = float(obj.geo['Kink_wing']['y'][2])
    z2 = 0.0
    c2 = float(obj.geo['Kink_wing']['chords'][2])    
#
    x3 = float(obj.geo['Kink_wing']['x'][3])
    y3 = float(obj.geo['Kink_wing']['y'][3])
    z3 = 0.0
    c3 = float(obj.geo['Kink_wing']['chords'][3])    

# Profiles...
    Af0 = airconics.primitives.Airfoil([x0,y0,z0], ChordLength=c0,
                                       Rotation=0,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af0.Curve, update=True, color='GREEN')

    Af1 = airconics.primitives.Airfoil([x1,y1,z1], ChordLength=c1,
                                       Rotation=0,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af1.Curve, update=True, color='GREEN')

    Af2 = airconics.primitives.Airfoil([x2,y2,z2], ChordLength=c2,
                                       Rotation=0,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af2.Curve, update=True, color='GREEN')

    Af3 = airconics.primitives.Airfoil([x3,y3,z3], ChordLength=c3,
                                       Rotation=0,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af3.Curve, update=True, color='GREEN')


    surf_wingin  = act.AddSurfaceLoft([Af0, Af1, Af2])
    surf_wingout = act.AddSurfaceLoft([Af2, Af3])    


#-------------       HT    --------------------
# Add NACA 4 digit airfoils to loft between:

    x0 = float(obj.geo['horz']['x'][0])
    y0 = float(obj.geo['horz']['y'][0])
    z0 = 0.0
    c0 = float(obj.geo['horz']['chords'][0])
#    z0 = obj.geo['Kink_wing']['zu'][0]    

    x1 = float(obj.geo['horz']['x'][1])
    y1 = float(obj.geo['horz']['y'][1])
    z1 = 0.0
    c1 = float(obj.geo['horz']['chords'][1])
    
    x2 = float(obj.geo['horz']['x'][2])
    y2 = float(obj.geo['horz']['y'][2])
    z2 = 0.0
    c2 = float(obj.geo['horz']['chords'][2])

# Profiles...    
    Af0 = airconics.primitives.Airfoil([x0,y0,z0], ChordLength=c0,
                                       Rotation=0,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af0.Curve, update=True, color='GREEN')

    Af1 = airconics.primitives.Airfoil([x1,y1,z1], ChordLength=c1,
                                       Rotation=0,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af1.Curve, update=True, color='GREEN')

    Af2 = airconics.primitives.Airfoil([x2,y2,z2], ChordLength=c2,
                                       Rotation=0,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af2.Curve, update=True, color='GREEN')

    surf_HT = act.AddSurfaceLoft([Af0, Af1, Af2])

#-------------       VT    --------------------
# Add NACA 4 digit airfoils to loft between:

  #  x0 = float(obj.geo['vert']['x'][0])
  #  y0 = 0.0
  #  z0 = float(obj.geo['vert']['z'][0])
    x0 = float(obj.geo['vert']['x'][0])
    y0 = 0.0
    z0 = 1.0
    c0 = float(obj.geo['vert']['chords'][0])
#    z0 = obj.geo['Kink_wing']['zu'][0]    

    #x1 = float(obj.geo['vert']['x'][1])
    #y1 = 0.0
  #  z1 = float(obj.geo['vert']['z'][0])
    x1 = float(obj.geo['vert']['x'][1])
    y0 = 0.0
    z1 = 5.5
    c1 = float(obj.geo['vert']['chords'][1])
    
# Profiles...

    Af0 = airconics.primitives.Airfoil([x0,y0,z0], ChordLength=c0,
                                       Rotation=90,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af0.Curve, update=True, color='GREEN')

    Af1 = airconics.primitives.Airfoil([x1,y1,z1], ChordLength=c1,
                                       Rotation=90,Twist=0,Naca4Profile='0012')
    display.DisplayShape(Af1.Curve, update=True, color='GREEN')

    surf_VT = act.AddSurfaceLoft([Af0, Af1])

    
#-------------       FUSELAGE    --------------------
##
#    fus = fuselage_oml.Fuselage(NoseLengthRatio=0.182, 
#                                TailLengthRatio=0.293, 
#                                Scaling=[55.902, 55.902, 55.902], 
#                                NoseCoordinates=[0.0, 0.0, 0], 
#                                CylindricalMidSection=False, 
#                                SimplificationReqd=False, 
#                                Maxi_attempt=5, 
#                                construct_geometry=True)


# Current Display of the WHTVT
    display.DisplayShape(surf_wingin, update=True)
    display.DisplayShape(surf_wingout, update=True)    
    display.DisplayShape(surf_HT, update=True)        
    display.DisplayShape(surf_VT, update=True)            
    #display.DisplayShape(fus, update=True)                
   # fus.Display()
    start_display()

#    Fus.Build(2)
#    Fus.Display(display)
#    renderer = TornadoWebRenderer()
#    Fin.Display(renderer)
#    TP.Display(renderer)
#    display(renderer)




