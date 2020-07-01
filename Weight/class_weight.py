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
    
"""
import numpy as np
from Auxilliary.class_aux import AuxTools

#----------------------------------------------------------------------#
#                               WEIGHT CLASS                           #
#----------------------------------------------------------------------#
class Weight(object, metaclass=AuxTools):
    """
        Aircraft Weight  - Wing, HT, VT, Fuselage, Fuel.
        
        Wing     -  Torenbeek
        HT       -  Torenbeek
        VT       -  Torenbeek
        Fuselage -  Torenbeek
        
    """
   
    def __init__(self,geo,perf,weight,*args, **kwargs):
        super(Weight, self).__init__(perf,geo,*args, **kwargs)


# Creating a libraries 

# A initial lvalue for the MTOW is necessary to obtain the first estimation for
# some of the aircraft components. Later the value is updated in an iteractive
# process.

        self.weight['mtow']           =  self.operating['mtow'] 
        self.weight['engine']         =  self.propulsion['weight']
        self.weight['freight_weight'] = self.operating['freight_weight']
        
        self.weight['fus']    =  {}
        self.weight['vert']   =  {}
        self.weight['horz']   =  {}  
        self.weight['misc']   =  {}    
        self.weight['wing']   =  {}            

#----------------------------------------------------------------------
    def Diving_Velocity(self,airprop,phase):
        
# Here the diving velocity computed. This velocity is considered in the weight
# model from Torenbeek.
        vd    = self.perf['vd']
        
        vkeas = 1479*(airprop[phase]['p_pref']*(((((((1.0+0.2*(vd/661.5)**2.0)\
                      **3.5)-1.0)/airprop[phase]['p_pref'])+1.0)**(1.0/3.5))  \
                      -1.0))**0.5
                      
        vktas = vkeas/(airprop[phase]['ro_roref']**0.5)
        
        vt    = vktas * 0.51444440

        return vt

#----------------------------------------------------------------------#
#                    Computing the HT Weight                           #
#----------------------------------------------------------------------#
    def HT_Weight(self,airprop):
        """ 
            This subroutine computes the HT weight. Torenbeek Methodology       
            Digitalized figure pg 281 and a polynomial fit to obtain the        
            curve.
        """

#        
        pi    = np.arccos(-1.0)

# Computing the True Speed of the Diving Velocity...I need to select the flight
# phase: 'climb', 'cruise', 'landing' (these are the phases so far considered)

        key = 'cruise'
        vel_diving = self.Diving_Velocity(airprop,key)
        
        kht = 0.783
        fht = (vel_diving/1000) * np.power(self.geo['horz']['sref'],0.2)/     \
               np.cos(pi*self.geo['horz']['sweep14']/180.0)
              
        self.weight['horz']['total'] = (-86.045*(np.power(fht,2.0)) +         \
                                         127.4*fht-16.803)          *         \
                                         self.geo['horz']['sref'] * kht

#----------------------------------------------------------------------#
#                    Computing the VT Weight                           #
#----------------------------------------------------------------------#
    def VT_Weight(self,airprop):
        """ 
            This subroutine computes the VT weight. Torenbeek Methodology       
            Digitalized figure pg 281 and a polynomial fit to obtain the        
            curve.
        """
        pi    = np.arccos(-1.0)
        
# Computing the True Speed of the Diving Velocity...I need to select the flight
# phase: 'climb', 'cruise', 'landing' (these are the phases so far considered)

        key = 'cruise'
        vel_diving = self.Diving_Velocity(airprop,key)
        
        kvt = 0.71 
        fvt = (vel_diving/1000) * np.power(self.geo['vert']['sref'],0.2)/     \
               np.cos(pi*self.geo['vert']['sweep14']/180.0)
              
        self.weight['vert']['total'] = (-86.045*(np.power(fvt,2.0)) +         \
                                         127.4*fvt-16.803) *                  \
                                        self.geo['vert']['sref'] *kvt

#----------------------------------------------------------------------#
#                    Computing the Fuselage Weight                     #
#----------------------------------------------------------------------#
    def Fus_Weight(self,airprop):

# Nult is hard-coded must be an input...
        nult = 3.75
        ltt  = 3.0/5.0 * self.geo['fus']['fus_length']
        kl   = 0.56 * np.power((ltt/(2.0*self.geo['fus']['diameter'])),      \
                               (3.0/4.0))
#
        if (kl > 2.610): kl = 1.150

# Computing the True Speed of the Diving Velocity...I need to select the flight
# phase: 'climb', 'cruise', 'landing' (these are the phases so far considered)

        key = 'cruise'
        vel_diving = self.Diving_Velocity(airprop,key)
        
        self.weight['fus']['skin'] = 0.05428                                * \
                                     np.power(self.geo['fus']['swet'],1.07) * \
                                     np.power(vel_diving,0.743) * kl
                                     
        self.weight['fus']['stringer'] = 0.0117 * kl                         *\
                                       np.power(self.geo['fus']['swet'],1.45)*\
                                       np.power(vel_diving,0.39)             *\
                                       np.power(nult,0.316)
                                       
        self.weight['fus']['frame'] = 0.190 * (self.weight['fus']['skin']    +\
                                               self.weight['fus']['stringer'])

        if (self.weight['fus']['skin']+self.weight['fus']['stringer']) < 286.0:
            aux = (self.weight['fus']['skin'] + self.weight['fus']['stringer'])
            self.weight['fus']['frame'] = 0.0911 * np.power(aux,1.13)


#----      Torenbeek pg 460  --> kf  gross shell modification
        kf    = 1.80
        self.weight['fus']['total'] = kf * (self.weight['fus']['skin']       +\
                                            self.weight['fus']['stringer']   +\
                                            self.weight['fus']['frame'])

#----------------------------------------------------------------------#
#                 Computing the Landing Gear Weight                    #
#----------------------------------------------------------------------#
    def LG_Weight(self):

#----   Main Landing Gear Parameters
#
        a1 = 18.10
        b1 = 0.131           
        c1 = 0.015                 # This value was changed in order 
        d1 = 0.00002230            # to better represent the reality.

#----   Nose Landing Gear Parameters
#
        a2 = 9.100
        b2 = 0.082
        c2 = 0.000
        d2 = 0.00000297                     

        self.weight['mlg'] = a1 + b1*np.power(self.weight['mtow'],(3.0/4.0)) +\
                             c1 * self.weight['mtow']                        +\
                             d1 * np.power(self.weight['mtow'],(3.0/2.0))

        self.weight['nlg'] = a2 + b2*np.power(self.weight['mtow'],(3.0/4.0)) +\
                             c2 * self.weight['mtow']                        +\
                             d2 * np.power(self.weight['mtow'],(3.0/2.0))

#----------------------------------------------------------------------#
#                          Wing  Weight                                #
#----------------------------------------------------------------------#
    def Wing_Weight(self):

#----
#      Here is the Torenbeek definition of the wing weight - It produced more 
#      realistic weight values.
#----
        kw      = 0.0049
        nult    = 3.75
        
        cs      = np.cos(np.pi*self.geo['wing']['sweep14']/180.0)
        bs      = self.geo['wing']['span'] / cs
        brefbs  = self.geo['wing']['span'] / bs
        tr      = self.geo['wing']['croot'] * self.geo['wing']['tcroot']
        frac    = ((bs/tr)/(self.weight['mtow']/                              \
                            self.geo['wing']['sref']))**0.30
        ww      = kw * np.power(bs,0.75) * (1.0 + brefbs) *                   \
                  np.power(nult,0.55) * frac

# This weight already consider the high-lift devices and the ailerons...
        
        self.weight['wing']['total']  = ww * self.weight['mtow']   

#  Considering the spoilers and the speed breakes and the under wing 
#  mounted engine...
        
        kspoiler     = 1.02
        kengine      = 0.95
        kcalibration = 0.98
        
        self.weight['wing']['total']  =  kspoiler * kengine * kcalibration *  \
                                         self.weight['wing']['total']
        
#----------------------------------------------------------------------#
#                      Operational Itens Weight                        #
#----------------------------------------------------------------------#
    def Operational_Weight(self):
        """
            Operational itens - Torenbeek pg 288
        """
        self.weight['oper'] = (186.0 + self.operating['ncrew']*68.0)   +      \
                              (6.35  * self.operating['no_pass'])      +      \
                              (1.13  * self.operating['no_pass'])      +      \
                              (0.907 * self.operating['no_pass'])  

#----------------------------------------------------------------------#
#                    Computing the Payload Weight                      #
#----------------------------------------------------------------------#
    def Payload_Weight(self):

#
#--- Simply the weight of the (passengers+baggage) + cargo 
#               
        self.weight['payload'] = self.operating['no_pass']        *           \
                                 self.operating['pass_weight']    +           \
                                 self.operating['freight_weight']

#----------------------------------------------------------------------#
#                    Computing the Miscellaneous Weight                #
#----------------------------------------------------------------------#
    def Miscellaneous_Weight(self):

#
#----    Furnishing weight  - torenbeek pg-291 (lower right side)

        self.weight['misc']['furnishing'] = 6.5 * self.operating['no_pass'] + \
                                            self.geo['fus']['vol'] * 16.0
#
#----    Anti-Icing weight  - pg 293 eq:  ( 14.0 * fus_central^1.28 ) [m]

        self.weight['misc']['icing'] = 14.0 *                                 \
                                      np.power(self.geo['fus']['central'],1.28)

#
#----    APU - Torenbeek pg 289
        aux = (self.operating['no_pass']*0.5)
        self.weight['misc']['apu'] = 11.7 * np.power(aux,(3.0/5.0))


#----    Hydraulics + peneumatic + eletrical weight - Torenbeek pg 290  
#        ( MZFW =  MTOW - MUFW )
        self.weight['misc']['hydraulics'] = (0.015 * (self.weight['mtow'] -   \
                                             self.weight['fuel'])) + 272.0

#----    Fire detection + fixed oxygen + escape provisions
        self.weight['misc']['oxygen'] = 13.6+(0.544*self.operating['no_pass'])
        self.weight['misc']['fire']   = 0.00120 * self.weight['mtow']
        self.weight['misc']['escape'] = 0.453 * self.operating['no_pass']

#
#----    Avionics weight - Torenbeek pg 289 (eq. 8-32)
        self.weight['misc']['avionics'] =0.347*(np.power((self.weight['mtow']-\
                                          self.weight['fuel']),(5/9)))       *\
                                          np.power((1.6*self.perf['range']),  \
                                                                          0.25)
       # print(dir(self.perf))
       # print('range %s '%(self.perf['range']))
                                         
#----------------------------------------------------------------------#
#                    Computing the Wing Fuel Tank                      #
#----------------------------------------------------------------------#
    def Fuel_Tank_Weight(self):
        """
            Computes the wing fuel tank volume and after thad the weight based 
            on the fuel density.
        """

# Hard-coded must be transfered to input file...
        fuel_density = 0.8030
        fuel_end_sta = self.geo['wing']['tank_y']
        y_end        = fuel_end_sta * self.geo['wing']['span'] / 2.0

#
#---  First Segment...
        c0    = (self.geo['wing']['spar_TE']-self.geo['wing']['spar_LE']) *   \
                float(self.geo['Kink_wing']['chords'][0])
                
        c1    = (self.geo['wing']['spar_TE']  -                               \
                 self.geo['wing']['spar_LE']) *                               \
                float(self.geo['Kink_wing']['chords'][1])        
                
        t0    = float(self.geo['Kink_wing']['t'][0])
        
        t1    = float(self.geo['Kink_wing']['t'][1])
        
        l10   = float(self.geo['Kink_wing']['y'][1]) -                        \
                float(self.geo['Kink_wing']['y'][0])
                
        vol1  = l10/6.0 * ((2.0*c0+c1)*t0 + (2*c1+c0)*t1)
#
#---  Second Segment...
        c1    = (self.geo['wing']['spar_TE'] - self.geo['wing']['spar_LE']) * \
                float(self.geo['Kink_wing']['chords'][1])

        c2    = (self.geo['wing']['spar_TE']  -                               \
                 self.geo['wing']['spar_LE']) *                               \
                float(self.geo['Kink_wing']['chords'][2])        
                
        t1    = float(self.geo['Kink_wing']['t'][1])
        
        t2    = float(self.geo['Kink_wing']['t'][2])
        
        l21   = float(self.geo['Kink_wing']['y'][2]) -                        \
                float(self.geo['Kink_wing']['y'][1])

        vol2  = l21/6.0 * ((2.0*c1+c2)*t1 + (2*c2+c1)*t2)        
#
#---  Third Segment...
        chord_end = Weight.Interp(y_end,self.geo['Kink_wing']['y'],           \
                                        self.geo['Kink_wing']['chords'])
        
        t_end     = Weight.Interp(y_end,self.geo['Kink_wing']['y'],           \
                                        self.geo['Kink_wing']['t'])

        c2    = (self.geo['wing']['spar_TE']-self.geo['wing']['spar_LE']) *   \
                float(self.geo['Kink_wing']['chords'][2])
        c3    = (self.geo['wing']['spar_TE']-self.geo['wing']['spar_LE']) *   \
                float(chord_end)        
        t2    = float(self.geo['Kink_wing']['t'][2])
        t3    = float(t_end)
        
        l32   = float(y_end)-float(self.geo['Kink_wing']['y'][2])
        
# Volume...        
        vol3  = l32/6.0 * ((2.0*c2+c3)*t2 + (2*c3+c2)*t3)        
        
        self.geo['wing']['vol'] = vol1 + vol2 + vol3
        
# Weight...
        self.tank_efficiency            = 0.87
        self.no_wings                   = 2.0
        self.weight['wing']['Maxfuel']  = self.geo['wing']['vol'] *           \
                                           self.no_wings           *          \
                                           self.tank_efficiency    *          \
                                           1000.0 * fuel_density 

#----------------------------------------------------------------------#
#                Computing the Usable Fuel Tank                        #
#----------------------------------------------------------------------#
    def Usable_Fuel_Weight(self,airprop):
        """
            Here I will compute the cruise mass fraction in order to have an 
            idea about the amount of fuel to accomplish the mission range with 
            the especified payload. I am disccounting from the total range the
            distance flew during the climb stage.        
        """
# Distance covered during the climb phase...        
        aux1 = self.perf['range'] - (airprop['climb']['velocity']  *          \
                                    self.perf['climb_time'] / 60.0 / 0.51444)       

        ld   = 13.0
        sfc  = self.propulsion['sfc']
        aux2 = airprop['cruise']['velocity']/ 0.51444 * ld / sfc
        self.perf['cruise_wf'] = 1.0 / np.exp(aux1/aux2)        
#
#----   Here I compute the total amount of fuel weight to complete the entire mission...
        self.weight['fuel']  = (1.00 - (self.perf['warm_wf']       *  \
                                                self.perf['taxi_wf']       *  \
                          self.perf['takeoff_wf'] * self.perf['climb_wf']  *  \
                          self.perf['cruise_wf'] * self.perf['descend_wf'] *  \
                          self.perf['land_wf'])) * self.weight['mtow']

# Here the fuel is being limited to 75% of the total amount the fuel the
# wing can carry + full payload. In case the range demands an amount of 
# fuel above this limit a message will be displayed on the screen.

        if self.weight['fuel'] > 0.75*self.weight['wing']['Maxfuel']:
            self.weight['fuel'] = 0.75*self.weight['wing']['Maxfuel']
            
# Computing the possible range for this amount of fuel that is limied to 75%
# of the wing fuel capacity.

            mff    = (1.0 - (self.weight['fuel']/self.weight['mtow']))
            fother = ( self.perf['warm_wf']    * self.perf['taxi_wf']     *   \
                       self.perf['takeoff_wf'] * self.perf['climb_wf']    *   \
                       self.perf['descend_wf'] * self.perf['land_wf']  )
            f5     = mff / fother
            new_range = aux2*np.log(1.0/f5) + airprop['climb']['velocity'] * \
                                 self.perf['climb_time'] / 60.0 / 0.51444

# For optimization purpose...
            self.perf['curr_range'] = new_range
            print(new_range)

            print('Maximum range achieved with this number of pax is: {:06.2f}'.format(new_range[0]))

            
#----------------------------------------------------------------------#
#                  Method to Converge the Weight                       #
#----------------------------------------------------------------------#
    def Total_Weight(self):
        
        self.weight['total'] = self.weight['wing']['total']        +          \
                               self.weight['horz']['total']        +          \
                               self.weight['vert']['total']        +          \
                               self.weight['fus']['total']         +          \
                               self.weight['mlg']                  +          \
                               self.weight['nlg']                  +          \
                               self.weight['oper']                 +          \
                               self.weight['payload']              +          \
                               self.weight['misc']['furnishing']   +          \
                               self.weight['misc']['icing']        +          \
                               self.weight['misc']['apu']          +          \
                               self.weight['misc']['hydraulics']   +          \
                               self.weight['misc']['oxygen']       +          \
                               self.weight['misc']['fire']         +          \
                               self.weight['misc']['escape']       +          \
                               self.weight['misc']['avionics']     +          \
                               self.weight['engine']               +          \
                               self.weight['freight_weight']       +          \
                               self.weight['fuel']
        

#----------------------------------------------------------------------#
#                Printing the Weight on the Screen                     #
#----------------------------------------------------------------------#
    def Print_Weight(self):

        print('  |-------------------------------------------------|')
        print('  |                  WEIGHT                         |')
        print('  |-------------------------------------------------|')
            
        print('   HT                 [Kg]  --> ' + "{0:.3f}".format(      \
                                          float(self.weight['horz']['total'])))

        print('   VT                 [Kg]  --> ' + "{0:.3f}".format(      \
                                          float(self.weight['vert']['total'])))

        print('   Fuselage           [Kg]  --> ' + "{0:.3f}".format(      \
                                           float(self.weight['fus']['total'])))

        print('   Wing               [Kg]  --> ' + "{0:.3f}".format(      \
                                          float(self.weight['wing']['total'])))

        print('   Engine             [Kg]  --> ' + "{0:.3f}".format(      \
                                                 float(self.weight['engine'])))

        print('   Payload            [Kg]  --> ' + "{0:.3f}".format(      \
                                                float(self.weight['payload'])))          

        print('   Wing Fuel Demanded [Kg]  --> ' + "{0:.3f}".format(      \
                                                   float(self.weight['fuel'])))
        
        print('   Operational        [Kg]  --> ' + "{0:.3f}".format(      \
                                                   float(self.weight['oper'])))

        print('   Main Landing Gear  [Kg]  --> ' + "{0:.3f}".format(      \
                                                    float(self.weight['mlg'])))

        print('   Nose Landing Gear  [Kg]  --> ' + "{0:.3f}".format(      \
                                                    float(self.weight['nlg'])))

        print('   Furnishing         [Kg]  --> ' + "{0:.3f}".format(      \
                                     float(self.weight['misc']['furnishing'])))
            
        print('   Icing System       [Kg]  --> ' + "{0:.3f}".format(      \
                                          float(self.weight['misc']['icing'])))          

        print('   APU                [Kg]  --> ' + "{0:.3f}".format(      \
                                            float(self.weight['misc']['apu']))) 

        print('   Hydraulics         [Kg]  --> ' + "{0:.3f}".format(      \
                                     float(self.weight['misc']['hydraulics']))) 

        print('   Oxygen             [Kg]  --> ' + "{0:.3f}".format(      \
                                         float(self.weight['misc']['oxygen']))) 

        print('   Fire               [Kg]  --> ' + "{0:.3f}".format(      \
                                           float(self.weight['misc']['fire'])))             

        print('   Escape             [Kg]  --> ' + "{0:.3f}".format(      \
                                         float(self.weight['misc']['escape']))) 

        print('   Avionics Weight    [Kg]  --> ' + "{0:.3f}".format(      \
                                       float(self.weight['misc']['avionics']))) 
            
        print('   Wing MaxFuel       [Kg]  --> ' + "{0:.3f}".format(      \
                                        float(self.weight['wing']['Maxfuel'])))
        
        print('   Freight            [Kg]  --> ' + "{0:.3f}".format(      \
                                         float(self.weight['freight_weight'])))

        print('   MTOW               [Kg]  --> ' + "{0:.3f}".format(      \
                                                   float(self.weight['mtow'])))
        
        print('                                                          ')  

#!
#!----   I do not allow the fuel weight to be higher than the total fuel tank capacity...

