from numpy import sqrt, zeros, random, argwhere, maximum, minimum, multiply, rad2deg, inf

from copy import deepcopy

import csv
from datetime import datetime

class GA:
    def __init__(self,nvar,varmin,varmax,maxit,npop, K_t = 1, K_p = 8, K_d = 2):
        self.nvar = nvar
        self.varmin = varmin
        self.varmax = varmax
        self.maxit = maxit
        self.npop = npop

        self.K_t = K_t
        self.K_p = K_p
        self.K_d = K_d

        self.mutationRate = 0.1
        self.mutationStandardDerivation = 0.5
        self.crossoverRate = 0.9
        self.crossoverGamma = 0.1
        
        self.generation = 0
        self.position = 0
        self.individual = 0
        
        self.pop = []
        self.vec_cost = []
        self.vec_dy = []
        self.vec_dang = []
        self.vec_dt = []

        self.index_better = 0
        self.cost_better = 1e6
        self.cost_better_all = 1e6

        self.nextPop = []
        self.oldPop = []

        self.max_dt = []
        self.index_dt = []
        self.max_dy = []
        self.index_dy = []
        self.max_dang = []
        self.index_dang = []

        self.header = ['Generation','d_e', 'k_r','delta','k_o','d_min','fitness','index_dt','dt','index_dy','dy','index_dang','dang']
        self.header1 = ['Generation','d_e', 'k_r','delta','k_o','d_min','fitness','index_dt','dt','index_dy','dy','index_dang','dang','average_fitness']
        self.data_csv = []

        self.startFile()

    def startFile(self):
        now = datetime.now()
        self.nameFile = now.strftime("%d-%m-%Y_%H:%M:%S")
        with open('data/'+self.nameFile+'.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(self.header1)

            f.close()

    def addFile(self, data):
        with open('data/'+self.nameFile+'.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(data)

            f.close()

    def update_cost_param(self,dy,dang,dt):
        self.vec_dy.append(dy)
        self.vec_dang.append(dang)
        self.vec_dt.append(dt)

    def initialize_pop(self):

        self.pop = zeros([self.npop,self.nvar])
        for i in range(self.npop):
            self.pop[i] = random.uniform(self.varmin, self.varmax, self.nvar)
            if i < 2:
               #self.pop[i] = [9.949208015204881, 5.563223824404487, 5.818062934476073, 0.7180865223544229, 2.4673089927053873]
               self.pop[i] = [2.653303339730094, 6.8860973487077874, 6.435074375051041, 5.994451248691961, 5.918745940902441]
            elif i<4:
                self.pop[i] = [2.1813530138094825,7.857709951079561,6.582757598795251,5.705388249266784,6.123060951431255]
    
    def cost_func(self, dt, dang, dy, flagTime, flagColision):
        self.cost = 0
        for i in range(len(dang)):
            self.cost += self.K_t*dt[i] + self.K_p*sqrt(rad2deg(dang[i])*rad2deg(dang[i])) + self.K_d*dy[i]*dy[i]
            #print("K_t: ", self.K_t*dt[i])
            #print("K_p: ", self.K_p*sqrt(rad2deg(dang[i])*rad2deg(dang[i])))
            #print("K_d: ", self.K_d*dy[i]*dy[i])

        if flagTime or flagColision:
            #print("Computei")
            self.cost += 1e6
        
        self.max_dt.append(max(dt))
        self.index_dt.append(dt.index(self.max_dt[-1]) + 1)
        self.max_dy.append(max(dy))
        self.index_dy.append(dy.index(self.max_dy[-1]) + 1)
        self.max_dang.append(max(dang))
        self.index_dang.append(dang.index(self.max_dang[-1]) + 1)
        self.vec_cost.append(self.cost)

        self.vec_dt = []
        self.vec_dy = []
        self.vec_dang = []

    def findBetterCost(self):
        self.cost_better = 1e6

        for i in range(len(self.vec_cost)):
            if self.vec_cost[i] < self.cost_better:
                self.index_better = i
                self.cost_better = self.vec_cost[i]
        
        if self.cost_better_all < self.cost_better:
            self.cost_better_all = self.cost_better

    def permutation(self):
        self.q = random.permutation(self.npop)
        #p1 = self.pop[q[0]]
        #p2 = self.pop[q[1]]
        #return p1, p2

    def nextGen(self):

        #print("\nPop atual: ")
        #print(self.pop)

        self.findBetterCost()

        self.writeData()

        self.selection()
        #self.permutation()
        #print("\nPop atual 2: ")
        #print(self.pop)
        for i in range(int(self.npop/2)):
            #print("\nIndividuos " + str(2*i) + " e " + str(2*i+1))
            p1, p2 = deepcopy(self.pop[2*i]), deepcopy(self.pop[2*i+1])
            #print("Pai 1: ", p1)
            #print("Pai 2: ", p2)
            c1, c2 = self.crossover(p1, p2, self.crossoverGamma)
            #print("Cross 1: ", c1)
            #print("Cross 2: ", c2)
            c1 = self.mutate(c1, self.mutationRate, self.mutationStandardDerivation)
            c2 = self.mutate(c2, self.mutationRate, self.mutationStandardDerivation)
            #print("Mut 1: ", c1)
            #print("Mut 2: ", c2)
            c1 = self.apply_bound(c1, self.varmin, self.varmax)
            c2 = self.apply_bound(c2, self.varmin, self.varmax)
            #print("Bound 1: ", c1)
            #print("Bound 2: ", c2)
            self.nextPop.append(c1)
            self.nextPop.append(c2)
        self.oldPop = deepcopy(self.pop)
        self.pop = deepcopy(self.nextPop)

        #print("\nPop nova: ")
        #print(len(self.pop))
        #print(self.pop)

        # self.generation += 1
        # self.position = 0
        # self.individual = 0

        # self.vec_dt = []
        # self.vec_dy = []
        # self.vec_dang = []

    def crossover(self,p1, p2, gamma):
        # Crossover BLX-alpha
        #c1 = deepcopy(p1)
        #c2 = deepcopy(p2)
        
        beta = random.uniform(0, 1)
        
        if beta < self.crossoverRate:
            alpha = random.uniform(-gamma, 1+gamma, self.nvar)
            #print("Alpha: ",alpha)
            #print("p1: ", p1)
            #print("multiply1: ", multiply(alpha,p1))
            #print("multiply2: ", multiply((1-alpha),p2))
            #print("Soma: ", multiply(alpha,p1) + multiply((1-alpha),p2))
            c1 = multiply(alpha,p1) + multiply((1-alpha),p2)
            c2 = multiply(alpha,p2) + multiply((1-alpha),p1)
        else:
            #print("Nao dei crossover")
            c1 = deepcopy(p1)
            c2 = deepcopy(p2)
        return c1, c2

    def mutate(self,x, mu, sigma):
        y = deepcopy(x)
        flag = random.rand(self.nvar) <= mu
        y += multiply(flag, sigma*random.randn(self.nvar))
        return y

    def apply_bound(self,x, varmin, varmax):
        x = maximum(x, varmin)
        x = minimum(x, varmax)
        return x
    
    def selection(self):
        # Método de torneio

        aux_temp_pop = zeros([self.npop,self.nvar])

        for j in range(self.npop):

            candidatos = int(self.npop*0.3)
            sel = random.randint(0, self.npop, candidatos)

            custos = []
            for i in range(candidatos):
                custos.append(self.vec_cost[sel[i]])
            min_cost = min(custos)
            min_index = custos.index(min_cost)
            ind = self.pop[sel[min_index]]
            aux_temp_pop[j] = ind

        self.pop = deepcopy(aux_temp_pop)

    def writeData(self):
        if self.individual == self.npop:            
            self.generationData = []
            self.generationData.append(self.generation)
            self.generationData += self.pop[self.index_better].tolist()
            self.generationData.append(self.vec_cost[self.index_better])
            self.generationData.append(self.index_dt[self.index_better])
            self.generationData.append(self.max_dt[self.index_better])
            self.generationData.append(self.index_dy[self.index_better])
            self.generationData.append(self.max_dy[self.index_better])
            self.generationData.append(self.index_dang[self.index_better])
            self.generationData.append(self.max_dang[self.index_better])
            self.generationData.append(sum(self.vec_cost)/self.npop)

            self.addFile(self.generationData)

            # print("\n-----GENERATION END-----")
            # print("General infos:")
            # print("Fitness Average: ", sum(self.vec_cost)/self.npop)
            # print("Better fitness: ", self.cost_better)
            # print("Better parameters: ", self.pop[self.index_better])
            # print("-----")

            # self.max_dt = []
            # self.index_dt = []
            # self.max_dy = []
            # self.index_dy = []
            # self.max_dang = []
            # self.index_dang = []
            # self.vec_cost = []

    def resetInfos(self):
        self.generation += 1
        self.position = 0
        self.individual = 0

        self.vec_dt = []
        self.vec_dy = []
        self.vec_dang = []

        self.max_dt = []
        self.index_dt = []
        self.max_dy = []
        self.index_dy = []
        self.max_dang = []
        self.index_dang = []
        self.vec_cost = []

        self.nextPop = []
