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

                         PARAMETERIZATION METHODS
                        -------------------------

"""
import math as m
import numpy as np

#------------------------------------------------------------------------------
def Bezier(input_file, output_file,stations):
    """
       Bezier Parameterization - Control Points to Define the Geometry.
       
    """
#
# Auxiliary variables: counters and stretching function.
    pi        = m.acos(-1.0)
    i         = 0
    npts      = 58
    stre_coef = 95.0
    dx        = 1.0 / npts
    etau      = list()
    x         = list()
    aux       = list()
    
# Reading the Input File to get the number of control Points Bezier...
    f = open(input_file,'r')
    for line in f:
        if( i > 0):
            aux = line.strip('\t\n\r').split(" ")
            for ii in range(0,len(aux)):
                if(aux[ii] != ""):
                    aux.append(aux[ii])
        i += 1    
    order = i-2          # Polynomial Order
    nocp  = i-1          # Number of control Points
    f.close()

# Getting the data
    f = open(input_file,'r')
    data  = [line.split() for line in f]
    auxer = np.array(data)
    f.close()

# Putting the data in the cpx and cpy vectors...

    cpx = np.zeros((nocp,int(stations)))
    cpy = np.zeros((nocp,int(stations)))
    
    for k in range(0,int(stations)):
        for ii in range(0,nocp):
            ki        = 2*k
            kp        = 2*k + 1
            cpx[ii,k] = auxer[ii+1][ki]
            cpy[ii,k] = auxer[ii+1][kp]

#  Generating the profile bunching  - ATANH  distribution
#
    for i in range(npts+1):
        x.append(float(0.0 + i * dx))
        stre  = 1.0 + m.tanh(stre_coef*(x[i]-1.0)*pi/180.0) /                 \
                      m.tanh(stre_coef*pi/180.0)
        etau.append(float(stre+0.0))

# Defining the coefficients of the PASCAL TRIANGLE.....
#
    lcni = list()
    for i in range(0, order+1, 1):
        aux = fat(order)/(fat(i)*fat(order-i))
        lcni.append(int(aux))
#
    duaux = [[0. for i in range(npts+1)] for k in range(order+1)]
    for i in range(0,npts+1,1):
        for k in range(0, order+1,1):
            duaux[int(k)][int(i)] = lcni[k]*(m.pow(etau[i],k))*(m.pow((1-etau[i]),(order-k)))

##
##   Here I am putting the dul array into other arrays using the numpy lib.
    du            = np.matrix(duaux).T
    cpx2          = np.reshape(cpx, (nocp,int(stations)))
    cpy2          = np.reshape(cpy, (nocp,int(stations)))
    x_bezier      = np.dot(du,cpx2)
    y_bezier      = np.dot(du,cpy2)    

# Name of the output files and writting the airfoils...

    name  = output_file.split('.')[1]
    for k in range(0,int(stations)):
#
        blade = "." + name + "_" + str(k+1) + ".dat"        # Opening the file
        f1 = open(blade,'w')
        for i in reversed(range(0,npts+1)):
            f1.write('%9.6f %9.6f\n' % (x_bezier[i,k],y_bezier[i,k]))
        for i in range(1,npts+1):
            f1.write('%9.6f %9.6f\n' % (x_bezier[i,k],-y_bezier[i,k]))
        f1.close()




#
#
#    f1.close()

#    data  = [line.split() for line in f]
#    auxer = np.array(data)
#    f.close()
#    
#    print(auxer)
    #cpx = np.zeros((nocp,stations[0]))
    #cpy = np.zeros((nocp,stations[0]))


#------------------------------------------------------------------------------
def fat(n):
     if n == 0:
         return 1
     else:
         return n * fat(n-1)