#------------------------------------------------------------------------------
# Name:        Genetic Algorithm
# Purpose:
#
# Author:      Alexandre Antunes
#
# Created:     05/07/2017
# Licence:     GNU AGPLv3
#
#	Permissions of this strongest copyleft license are conditioned
#	on making available complete source code of licensed works and
#	modifications, which include larger works using a licensed work,
#	under the same license. Copyright and license notices must be preserved.
#	Contributors provide an express grant of patent rights. When a
#	modified version is used to provide a service over a network,
#	the complete source code of the modified version must be made available.
#
#------------------------------------------------------------------------------
import numpy as np
import sys

def GA_Setup():
    """  This module reads the GA setup.
    """

# Definition of the lists. Key names to look in the setup file
    itens   = ['Generation', 'Population', 'Pmut', 'Pcross', 'Mating_Pool',
               'Type', 'Blx_alpha','Var_Size','Variables'] 
    
# Here I store the values for each of the itens above.
    itens2  = ['Var_Lower','Var_Upper']                                                                     
    values  = list()                                     

# Reading the setup
    f=open('.\\Input_Files\\ga_setup.inp','r')
    data  = np.array([line.split() for line in f])
    f.close()

# Attributing the values for each itens from the above described list.....
    for i in range(0,len(itens)):
        if filter(lambda x: itens[i] in x, data):
            values.append(data[i][2])

    values2 = list()
    for j in range(0,len(itens2)):
        for i in range(0,len(data)):
            if(itens2[j] == data[i][0]):
                  values2.append(data[i][2:])
                  #values2.append(filter(None, re.split('[, ]',data[i])))

# Sanity Check...
    if(len(values2[0]) != len(values2[1])):
        sys.exit('Number of lower and upper range not equal.....')

    if(int(len(values2[0])) != int(values[-1])):
        sys.exit('Number of defined upper and lower range is different from \
                 the number of design variables.....')

    if ( int(values[1]) % int(values[4]) != 0):
        sys.exit('Population is not a multiple from Mating_Pool.')
        
    return values+values2
