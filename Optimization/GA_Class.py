#------------------------------------------------------------------------------
# Name:        Genetic Algorithm
# Purpose:
#
# Author:      Alexandre Antunes
# Email:       alexandre.pequeno.antunes@gmail.com
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
from Optimization.Sobol import i4_sobol_generate
from matplotlib import pyplot as plt


#------------------------------------------------------------------------------
class Genetic(object):
    """
        Genetic Class - Main operators for a Single Genetic Algorithm.
        
        Gen            ---> Number fo Generations
        Pop            ---> Size of the Population
        Pmut           ---> Mutation Probability
        Pcross         ---> CrossOver Probability
        Mating_Pool    ---> Number of individuals in the Mating_Pool
        Tipo           ---> GA Type. So far, just the binary representation is
                            implemented
        Size           ---> Size of the binary string
        var            ---> Number of Design Variables
        Var_Lower      ---> Lower Range of the Design Variables       
        Var_Upper      ---> Upper Range of the Design Variables       
    """

    def __init__(self,gen,pop,pmut,pcross,mating_pool,tipo,alpha,size,var,
                 var_lower,var_upper,*args):
        
        self.gen           = int(gen)
        self.pop           = int(pop)
        self.pmut          = float(pmut)
        self.pcross        = float(pcross)
        self.mating_pool   = int(mating_pool)
        self.tipo          = str(tipo)
        self.alpha         = float(alpha)
        self.size          = int(size)
        self.var           = int(var)
        self.var_lower     = var_lower
        self.var_upper     = var_upper
        
        self.obj           = list()
        self.bit           = list()   
        self.pool          = list()
        
        self.eletism_index = int(0)
        self.eletism       = list()
        
# Size of the binary string        
        self.ngen_tot      = self.size * self.var                        

# Generating the chromossomes        
        self.cromo         = np.zeros((self.pop,self.ngen_tot))          

# Generating the auxiliary chromossomes                
        self.cromo_update  = np.zeros((self.pop,self.ngen_tot))        

# Generating the Design Vector
        self.cod           =  np.zeros((self.pop,self.var))
        
    pass
#-----------------------------------------------------------------------------#
#                    Creating the Initial Population                          #
#-----------------------------------------------------------------------------#
    def CreatePop_Binary(self,i):
        """ 
        This method creates the Initial Population for the GA Algorithm.
        
        """
        
# Generating the bits
        self.bit.append(np.random.uniform(0,1,self.ngen_tot))            

        for j in range(0,self.ngen_tot):
            if (self.bit[i][j] <= 0.5):
                self.cromo[i][j] = int(0)
            else:
                self.cromo[i][j] = int(1)
    pass

#-----------------------------------------------------------------------------#
#                            SBX  Operator                                    #
#-----------------------------------------------------------------------------#
    def CreatePop_Real(self,i):
        
        out = i4_sobol_generate ( self.var, i+1, 1)
        for j in range(0,self.var):
            self.cod[i][j] =   float(self.var_lower[j])  + (                  \
                               float(self.var_upper[j])  -                    \
                               float(self.var_lower[j])) *                    \
                               out[j][i]
            #print(i,j,self.cod[i][j])

    pass

#-----------------------------------------------------------------------------#
#                            Mutation Operator                                #
#-----------------------------------------------------------------------------#
    def Mutation(self,i):

        alimit1 = 0.5 - (self.pmut)/2.0
        alimit2 = 0.5 + (self.pmut)/2.0        

# It is important to say that I am not applying the mutation at the individual
# located at Npop/2 because at this specific location in the vector I am 
# storing the best individual from the previous generation and I do not want to
# mutate this individual because I can end with a worse fitness. 
# PAY ATTENTION HERE !!

        if i != int(self.pop/2):                 
            for j in range(0,self.ngen_tot):
                rnd = np.random.uniform()
                if (rnd > alimit1 and rnd < alimit2):
                    if self.cromo[i][j] ==1:
                        self.cromo[i][j] = 0
                    else:
                        self.cromo[i][j] = 1
    pass

#-----------------------------------------------------------------------------#
#                            Mutation Operator                                #
#-----------------------------------------------------------------------------#
    def Mutation_Real(self,i):

        alimit1 = 0.5 - (self.pmut)/2.0
        alimit2 = 0.5 + (self.pmut)/2.0        

# It is important to say that I am not applying the mutation at the individual
# located at Npop/2 because at this specific location in the vector I am 
# storing the best individual from the previous generation and I do not want to
# mutate this individual because I can end with a worse fitness. 
# PAY ATTENTION HERE !!
        b = 2
        if i != int(self.pop/2):                 
            for j in range(0,int(self.var)):
                rnd = np.random.uniform()
                if (rnd > alimit1 and rnd < alimit2):
                    rnd = np.random.uniform()
                    delta = (1.0 - rnd**(1-(i/self.gen))**b)
                    self.cod[i][j] =  self.cod[i][j]                       +  \
                                     ( float(self.var_upper[j])            -  \
                                       float(self.var_lower[j]) )          *  \
                                       delta
    pass
#-----------------------------------------------------------------------------#
#             Decoding the binary strings in Real values.                     #
#-----------------------------------------------------------------------------#
    def Decode(self,i):

        self.nscale  =  np.power(2,self.size)

        for j in range(0,self.var):
             summ  = 0.0
             aux1  = j*self.size
             aux2  = ((j+1)*self.size)
             for k in range(aux1,aux2):
                 summ = summ + self.cromo[i][k]*(np.power(2.0,(k-aux1)))

             self.cod[i][j] =   float(self.var_lower[j])  + (
                             ( (float(self.var_upper[j])  -
                                float(self.var_lower[j])) /
                                self.nscale) * summ          )
    pass

#-----------------------------------------------------------------------------#
#                      Selection Operator                                     #
#-----------------------------------------------------------------------------#
    def Fitness(self,fit):
        
        self.obj.append(fit)
    pass

#-----------------------------------------------------------------------------#
#                      Selection Operator                                     #
#-----------------------------------------------------------------------------#
    def Selection(self):
        
 # Reseting the pool list for every new generation... 
 # This is absolutely NECESSARY !!!!!
        ki                 = int(self.pop/self.mating_pool)
        self.pool          = list()                            
        
        for j in range(0,ki):
            for k in range(0,self.mating_pool):
                mate  = list()
                index = list()
        
# I am storing the fitness index from the best individual that survived in 
# the mating pool!!!!
                for l in range(0,self.mating_pool):
                    select = int(np.random.random()*self.pop)
                    mate.append(self.obj[select])
                    index.append(select)                        

# Notice that I can have the same fitness value in the list more than once
# I need to check that because I just want to store one value in the POOL list.
# Otherwise I crash the code !!!!! That's way I have this additional counter kj
# Once I find the best I am done.
                m  = max(mate)          
                kj = 0                                          
                for km in range(len(mate)):                     
                    if mate[km] == m:
                        if kj == 0:
                            kj += 1
                            self.pool.append(index[km])

        kj = 0
        mm = max(self.obj)
        for ii in range(0,self.pop):
            if (self.obj[ii] == mm):
                # What is the point here? Just taking the first best element 
                # stored in the vector (in case there are more than one).
                if kj == 0:                     
                    kj += 1                
                    self.eletism_index = ii
        print('Keeping Individual: ',self.eletism_index)
    pass

#-----------------------------------------------------------------------------#
#                       CrossOver Operator                                    #
#-----------------------------------------------------------------------------#
    def CrossOver(self):

        split = list()
        
        for ii in range(0,self.ngen_tot):
            self.eletism.append(self.cromo[self.eletism_index][ii])

        for i in range(0,self.var):
            pos = (np.random.random()*self.size)
            split.append((int(pos)+int(i*self.size)))

        for i in range(0,int(self.pop/2)):
            ind1 = 2*i
            ind2 = 2*i+1

            for jk in range(0,self.var):
                k     = 0
                aux1  = jk*self.size
                aux2  = ((jk+1)*self.size)                
                for lm in range(aux1,aux2):
                    if lm > split[jk]: k = 1
                    self.cromo_update[ind1][lm] =                             \
                                    self.cromo[self.pool[ind1]][lm] * (1-k) + \
                                    self.cromo[self.pool[ind2]][lm] *    k
                    self.cromo_update[ind2][lm] =                             \
                                    self.cromo[self.pool[ind1]][lm] *    k  + \
                                    self.cromo[self.pool[ind2]][lm] * (1-k)
        
        for ii in range(0,self.pop):
            for jj in range(0,self.ngen_tot):
                self.cromo[ii][jj] = self.cromo_update[ii][jj]
        
# Some Elitisms here in order to not loose the best individual...
        for ii in range(0,self.ngen_tot):
            self.cromo[int(self.pop/2)][ii] = self.eletism[ii]      

# Cleaning the list of the merit function for the next generation.                
# Cleaning the list of the eletism for the next generation.
# This is absolutely NECESSARY !!!!!

        self.obj       = list()                                     
        self.eletism   = list()                                     
    pass

#-----------------------------------------------------------------------------#
#                           BLX  Operator                                     #
#-----------------------------------------------------------------------------#
    def Blx(self):
        
        aux       =  np.zeros((1,self.var))
        cod_dummy =  np.zeros((self.pop,self.var))  
        
# Storing the best element in this aux variable...
        for k in range(0,self.var):
            aux[0][k] = self.cod[self.eletism_index][k]

        for i in range(0,int(self.pop/2)):
            
            ind1 = 2*i
            ind2 = 2*i+1
            
            select_a = int(np.random.random()*self.pop)
            select_b = int(np.random.random()*self.pop)
            
            for j in range(0,self.var):
               # dab = np.sqrt(self.cod[select_a][j]*self.cod[select_a][j] + 
               #               self.cod[select_b][j]*self.cod[select_b][j])    
                dab = abs(self.cod[select_a][j]-self.cod[select_b][j])

                l1  = ( min(self.cod[select_a][j],self.cod[select_b][j]) -
                        self.alpha*dab ) 
                
                l2  = ( max(self.cod[select_a][j],self.cod[select_b][j]) +
                        self.alpha*dab ) 

                cod_dummy[ind1][j] = l1 + np.random.random() * abs(l2-l1)
                cod_dummy[ind2][j] = l1 + np.random.random() * abs(l2-l1)

        # Fixing the range
        for i in range(0,int(self.pop)):    
            for j in range(0,int(self.var)):
                self.cod[i][j] = cod_dummy[i][j]
                if  self.cod[i][j] > float(self.var_upper[j]):
                    self.cod[i][j] = self.var_upper[j]
                    
                if  self.cod[i][j] < float(self.var_lower[j]):
                    self.cod[i][j] = self.var_lower[j]

        # Some Eletisms
        for k in range(0,self.var):
            self.cod[int(self.pop/2)][k] = aux[0][k]


# Cleaning the list of the merit function for the next generation.
# Cleaning the list of the eletism for the next generation.
# This is absolutely NECESSARY !!!!!

        self.obj       = list()                                     
        self.eletism   = list()                                     
            
    pass

#-----------------------------------------------------------------------------#
#                           BLX  Operator                                     #
#-----------------------------------------------------------------------------#
    def SBlx(self):
        
        aux       =  np.zeros((1,self.var))
        cod_dummy =  np.zeros((self.pop,self.var))
        
# Storing the best element in this aux variable...
        for k in range(0,self.var):
            aux[0][k] = self.cod[self.eletism_index][k]

        for i in range(0,int(self.pop/2)):

            ind1 = 2*i
            ind2 = 2*i+1

            select_a = int(np.random.random()*self.pop)
            select_b = int(np.random.random()*self.pop)            

            for j in range(0,self.var):
   
                rnd  = np.random.random()
                if rnd < 0.5:
                    bq = (2.0*rnd)**(1.0/(self.alpha+1.0))
                else:
                    bq = (1.0/(2.0*(1.0-rnd)))**(1.0/(self.alpha+1.0))
               
                if self.cod[select_a][j] > self.cod[select_b][j]:
                    swap                  = self.cod[select_a][j]
                    self.cod[select_a][j] = self.cod[select_b][j]
                    self.cod[select_b][j] = swap
                    
                cod_dummy[ind1][j] = 0.5 * ( (1+bq)*self.cod[select_a][j] + 
                                             (1-bq)*self.cod[select_b][j])
                
                cod_dummy[ind2][j] = 0.5 * ( (1-bq)*self.cod[select_a][j] + 
                                             (1+bq)*self.cod[select_b][j])
                
        # Fixing the range
        for i in range(0,int(self.pop)):    
            for j in range(0,int(self.var)):
                self.cod[i][j] = cod_dummy[i][j]

                if  self.cod[i][j] > float(self.var_upper[j]):
                    self.cod[i][j] = self.var_upper[j]
                    
                if  self.cod[i][j] < float(self.var_lower[j]):
                    self.cod[i][j] = self.var_lower[j]

        # Some Eletisms
        for k in range(0,self.var):
            self.cod[int(self.pop/2)][k] = aux[0][k]


# Cleaning the list of the merit function for the next generation.
# Cleaning the list of the eletism for the next generation.
# This is absolutely NECESSARY !!!!!

        self.obj       = list()                                     
        self.eletism   = list()                                     
            
    pass
#------------------------------------------------------------------------------

class Simple_GA(Genetic):
    """
        Implementation of the Simple Genetic Algorithm. The operators are
        defined in the Class Genetic.
    """
    def __init__(self,gen,pop,pmut,pcross,mating_pool,tipo,alpha,size,var,
                 var_lower,var_upper,*args):
        
        super(Simple_GA,self).__init__(gen,pop,pmut,pcross,mating_pool,tipo,
                                       alpha, size,var,var_lower,var_upper,
                                       *args)
        
        
    def Opt_SGA(self,Func):       
        """
            This method calls the GA operators to perform a single genetic 
            algorithm optimization.
        """         
# Auxiliary variables to plot the SGA convergence.
        x       = list()                    
        y       = list()
        y1      = list()

        f1   = open('SGA_Results.out','w')
        f1.write('%s \n' % ('Gen   |    Max   |   AVG     |  Design variables')
                 ) 
        f1.write('%s \n' % ('------------------------------------------------')
                 ) 

         #---------------------------------------------------------#
         #         BINARY CODING FOR THE SGA ALGORITHM             #
         #---------------------------------------------------------#
        if self.tipo == 'Binary':
            for gen in range(0,self.gen):
# I need this dummy vector here to store the decoded values from the variables.
                cod_aux = np.zeros((self.pop,self.var))      
                print(' ---- SGA Optimization | Generation :',gen,' ----')
                for ind in range(0,self.pop):
                    if gen == 0:
                        self.CreatePop_Binary(ind)   # Initial Population
# Mutation Operator.
                    Genetic.Mutation(self,ind)       

# Decoding the Binary string into real values for the design variable.
                    Genetic.Decode(self,ind)         
                    
 # Calling the USER Defined Function - UDF.
                    merit = Func(self.cod[ind])     
                
# Fitness assignment.
                    Genetic.Fitness(self,merit)      

# Dummy vector for post-processing 
                    for i in range(0,self.var):                            
                        cod_aux[ind][i] = self.cod[ind][i]
                    
#                    print('Ind --> ' + "{0:00d}".format(ind) +                \
#                          '  Merit Function  --> ' + "{0:.5f}".format(merit)) 

                print('Generation: ' + "{0:00d}".format(gen) +                \
                      ' |  Best Individual: ' + "{0:.2f}".format(max(self.obj)) 
                      + ' |  AVG: ' + "{0:.2f}".format(sum(self.obj)/           
                                                     len(self.obj)) ) 
                
                f1.write('%3d   | %6.3f   | %6.3f    | %20s  \n' %            \
                         (gen,max(self.obj),sum(self.obj)/len(self.obj),      \
                          cod_aux[np.argmax(self.obj)]))    

                x.append(gen)
                y.append(sum(self.obj)/len(self.obj))
                y1.append(max(self.obj))

#----     Last GA Operators  -------
# Selection Operator  - Mating_Pool Concept is Implemented here....
# CrossOver Operator
                Genetic.Selection(self)                                    
                Genetic.CrossOver(self)                                   
                print('  ')

          #---------------------------------------------------------#
          #           REAL CODING FOR THE SGA ALGORITHM             #
          #---------------------------------------------------------#
        if self.tipo == 'Real':
            for gen in range(0,self.gen):
# I need this dummy vector here to store the decoded values fromt he variables.
                cod_aux = np.zeros((self.pop,self.var))      
                print(' ---- SGA Optimization | Generation :',gen,' ----')
                for ind in range(0,self.pop):
                    if gen == 0:
                        self.CreatePop_Real(ind)      # Initial Population
# Mutation Operator.
                    Genetic.Mutation_Real(self,ind) 
                        
# Calling the USER Defined Function - UDF
                    merit = Func(self.cod[ind])      

# Fitness assignment
                    Genetic.Fitness(self,merit)                            

# Dummy vector for post-processing
                    for i in range(0,self.var):                            
                        cod_aux[ind][i] = self.cod[ind][i]
                    
                 #   print('Ind --> ' + "{0:00d}".format(ind) +                \
                 #         '  Merit Function  --> ' + "{0:.5f}".format(merit)) 

                print('Generation: ' + "{0:00d}".format(gen) +                \
                      ' |  Best Individual: ' + "{0:.2f}".format(max(self.obj)) 
                      + ' |  AVG: ' + "{0:.2f}".format(sum(self.obj)/           
                                                     len(self.obj)) ) 
                
                f1.write('%3d   | %6.3f   | %6.3f    | %20s  \n' %            \
                         (gen,max(self.obj),sum(self.obj)/len(self.obj),      \
                          cod_aux[np.argmax(self.obj)])) 
#
                x.append(gen)
                y.append(sum(self.obj)/len(self.obj))
                y1.append(max(self.obj))
#
#----     Last GA Operators  -------
# Selection Operator  - Mating_Pool Concept is Implemented here.
# CrossOver Operator for the Real Coding representation.

                Genetic.Selection(self)                                    
                Genetic.Blx(self)                                          
                print('  ')

#--- Plotting the  Figure
        
        plt.plot(x,y1)
        plt.pause(1)
        f1.close()                
