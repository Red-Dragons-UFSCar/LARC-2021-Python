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


    def update_cost_param(self,dy,dang,dt):
        self.vec_dy.append(dy)
        self.vec_dang.append(dang)
        self.vec_dt.append(dt)
        self.flagsTime.append(flagTime)

    def initialize_pop(self):

        self.pop = zeros([self.npop,self.nvar])
        for i in range(self.npop):
            self.pop[i] = random.uniform(self.varmin, self.varmax, self.nvar)
            #self.pop[i][0] = 4.084236529565755
            #self.pop[i][1] = 26.655381503697267


    def cost_func(self, dt, dang, dy):
        cost = 0
        for i in range(len(dang)):
            cost += self.K_t*dt[i] + self.K_p*sqrt(rad2deg(dang[i])*rad2deg(dang[i])) + self.K_d*dy[i]*dy[i]
        self.max_dt.append(max(dt))
        self.index_dt.append(dt.index(self.max_dt[-1]) + 1)
        self.max_dy.append(max(dy))
        self.index_dy.append(dy.index(self.max_dy[-1]) + 1)
        self.max_dang.append(max(dang))
        self.index_dang.append(dang.index(self.max_dang[-1]) + 1)
        self.vec_cost.append(cost)

        print("Custos: ", self.vec_cost)

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
            c1 = self.mutate(c1, 0.24, 2)
            c2 = self.mutate(c2, 0.24, 2)
            c1 = self.apply_bound(c1, self.varmin, self.varmax)
            c2 = self.apply_bound(c2, self.varmin, self.varmax)
            self.nextPop.append(c1)
            self.nextPop.append(c2)
        self.oldPop = deepcopy(self.pop)
        self.pop = deepcopy(self.nextPop)
        #print("Vai filhão")

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
        #ind = argwhere(flag)
        #y[ind] += sigma*random.randn(len(ind))
        y += multiply(flag, sigma*random.randn(self.nvar))
        return y

    def apply_bound(self,x, varmin, varmax):
        x = maximum(x, varmin)
        x = minimum(x, varmax)
        return x

    def roulette_wheel_selection(self,p):
        c = cumsum(p)
        r = sum(p)*random.rand()
        ind = argwhere(r <= c)
        return ind[0][0]
