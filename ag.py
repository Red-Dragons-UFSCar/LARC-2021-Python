from numpy import sqrt, zeros, random, argwhere, maximum, minimum, multiply, rad2deg, inf

from copy import deepcopy

import csv

class GA:
    def __init__(self,nvar,varmin,varmax,maxit,npop, K_t = 10, K_p = 8, K_d = 2):
        self.nvar = nvar
        self.varmin = varmin
        self.varmax = varmax
        self.maxit = maxit
        self.npop = npop

        self.K_t = K_t
        self.K_p = K_p
        self.K_d = K_d
        
        self.generation = 0
        self.position = 0
        self.individual = 0
        
        self.pop = []
        self.vec_cost = []
        self.vec_dy = []
        self.vec_dang = []
        self.vec_dt = []
        self.flagsTime = []

        self.index_better = 0
        self.cost_better = 1e6

        self.nextPop = []
        self.oldPop = []

        self.max_dt = []
        self.index_dt = []
        self.max_dy = []
        self.index_dy = []
        self.max_dang = []
        self.index_dang = []

        self.header = ['Generation','d_e', 'k_r','delta','k_o','d_min','Cost','index_dt','dt','index_dy','dy','index_dang','dang']
        self.data_csv = []

    def update_cost_param(self,dy,dang,dt, flagTime):
        self.vec_dy.append(dy)
        self.vec_dang.append(dang)
        self.vec_dt.append(dt)
        self.flagsTime.append(flagTime)

    def initialize_pop(self):

        self.pop = zeros([self.npop,self.nvar])
        for i in range(self.npop):
            self.pop[i] = random.uniform(self.varmin, self.varmax, self.nvar)
            if i < 5:
               self.pop[i] = [9.949208015204881, 5.563223824404487, 5.818062934476073, 0.7180865223544229, 2.4673089927053873]
            #    self.pop[i] = [9.302233213565474, 8.403007627366772, 6.35626706943918, 1.0363333802109564, 4.322376353319517]

    def cost_func(self, dt, dang, dy):
        self.cost = 0
        for i in range(len(dang)):
            self.cost += self.K_t*dt[i] + self.K_p*sqrt(rad2deg(dang[i])*rad2deg(dang[i])) + self.K_d*dy[i]*dy[i]
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
        self.flagsTime = []

    def findBetterCost(self):
        for i in range(len(self.vec_cost)):
            if self.vec_cost[i] < self.cost_better:
                self.index_better = i
                self.cost_better = self.vec_cost[i]

    def permutation(self):
        q = random.permutation(self.npop)
        p1 = self.pop[q[0]]
        p2 = self.pop[q[1]]
        return p1, p2

    def nextGen(self):
        for i in range(int(self.npop/2)):
            p1, p2 = self.permutation()
            c1, c2 = self.crossover(p1, p2)
            c1 = self.mutate(c1, 0.4, 0.5)
            c2 = self.mutate(c2, 0.4, 0.5)
            c1 = self.apply_bound(c1, self.varmin, self.varmax)
            c2 = self.apply_bound(c2, self.varmin, self.varmax)
            self.nextPop.append(c1)
            self.nextPop.append(c2)
        self.oldPop = deepcopy(self.pop)
        self.pop = deepcopy(self.nextPop)

        self.generation += 1
        self.position = 0
        self.individual = 0

        self.vec_dt = []
        self.vec_dy = []
        self.vec_dang = []
        self.flagsTime = []

    def crossover(self,p1, p2, gamma=0.1):
        c1 = deepcopy(p1)
        c2 = deepcopy(p2)
        alpha = random.uniform(-gamma, 1+gamma, self.nvar)
        c1 = multiply(alpha,p1) + multiply((1-alpha),p2)
        c2 = multiply(alpha,p2) + multiply((1-alpha),p1)
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
        aux_temp_pop = zeros([self.npop,self.nvar])
        aux_cost = []

        for i in range(self.npop):
            min_value = min(self.vec_cost)
            min_index = self.vec_cost.index(min_value)
            aux_cost.append(min_value)
            aux_temp_pop[i] = self.pop[min_index]
            self.vec_cost[min_index] = inf
        self.pop = deepcopy(aux_temp_pop)
        self.vec_cost = deepcopy(aux_cost)

    def writeData(self):
        if self.individual == self.npop:

            for i in range(self.npop):
                self.data_csv.append([self.generation,self.pop[i][0],self.pop[i][1],self.pop[i][2],self.pop[i][3],self.pop[i][4], self.vec_cost[i],
                                    self.index_dt[i], self.max_dt[i], self.index_dy[i], self.max_dy[i],self.index_dang[i], self.max_dang[i]])
            self.findBetterCost()
            with open('results.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(self.header)

                # write multiple rows
                writer.writerows(self.data_csv)

                f.close()
            print("\n-----GENERATION END-----")
            print("General infos:")
            print("Fitness Average: ", sum(self.vec_cost)/self.npop)
            print("Better fitness: ", self.cost_better)
            print("Better parameters: ", self.pop[self.index_better])
            print("-----")

            self.max_dt = []
            self.index_dt = []
            self.max_dy = []
            self.index_dy = []
            self.max_dang = []
            self.index_dang = []
            self.vec_cost = []
