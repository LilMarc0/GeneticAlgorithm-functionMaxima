import numpy as np
import time
from random import randint, random
import os

NRPOP = 100
KEEPRATIO = 16
DISCARDRATIO = 10
MAXDEV =  -9999999
MUTATION_PROB = 0.2

class individ:
    def __init__(self, crom, decoded=0, fit=0):
        self.crom = crom
        self.fit = fit
        self.decoded = int(crom, 2)

    def __repr__(self):
        return str(self.decoded)

class population:
    def __init__(self, nr = NRPOP, kr = KEEPRATIO, dr = DISCARDRATIO, mp = MUTATION_PROB):
        self.nr = nr
        self.kr = kr
        self.dr = dr
        self.mp = mp
        self.pop = self.initial_pop()

    # functia de aproximat
    def eval(self, x):
        return -x**2 + x + 1

    # decimal to binary ( max 64 - 7 cifre )
    def encode(self, crom):
        s = str(bin(crom)[2:])
        for _ in range(7 - len(s)):
            s = '0' + s
        return s

    def decode(self, crom):
        return int(crom, 2)

    def initial_pop(self):
        pop = []
        for i in range(NRPOP):
            c = randint(0, 64)
            pop.append(individ(self.encode(c), c))
        return pop

    def crossover(self):
        new_pop, rem_pop = self.pop[:self.kr], self.pop[self.kr:]
        while len(new_pop) != NRPOP:
            for i, ind in enumerate(rem_pop):
                crom = ind.crom
                other = randint(0, len(self.pop)-1)
                other1 = randint(0, len(self.pop) - 1)
                crom1 = self.pop[other].crom
                crom2 = self.pop[other1].crom
                Ncrom = crom[:len(crom) // 2] + crom1[len(crom1) // 2:]
                Ncrom1 = crom[:len(crom) // 2] + crom2[len(crom2) // 2:]

                new_pop.append(individ(Ncrom))
                new_pop.append(individ(Ncrom1))
                #print(len(new_pop))
                del rem_pop[i]
        print(new_pop)
        return new_pop

    def fitness(self):
        f = 0
        for ind in self.pop:
            ind.fit = abs(1-ind.decoded)
            f += ind.fit
        print('Overall fitness: ' + str(f))
        self.pop = sorted(self.pop, key=lambda x: x.fit)

    def point_mutation(self):
        for ind in self.pop:
            ol = len(ind.crom)
            if random() < self.mp:
                p = randint(1, len(ind.crom)-1)
                if ind.crom[p] == '0':
                    ind.crom = ind.crom[:p] + '1' + ind.crom[p+1:]
                elif ind.crom[p] == '1':
                    ind.crom = ind.crom[:p] + '0' + ind.crom[p + 1:]
            if ol != len(ind.crom):
                exit(-1)


class GA:
    def __init__(self, pop, nr_epochs, gen_per_epoch, mp_decay_rate):
        self.nr_epochs = nr_epochs
        self.gen_per_epoch = gen_per_epoch
        self.pop = pop
        self.mp_decay_rate = mp_decay_rate

    def run(self):
        t = time.time()
        e = 1
        for epoch in range(self.nr_epochs):
            print('EPOCH{} --------------'.format(e))
            self.pop.mp -= self.pop.mp / self.mp_decay_rate
            g = 0
            for gen in range(self.gen_per_epoch):
                print('EPOCH{}\nGEN{}:'.format(e,g))
                self.pop.fitness()
                self.pop.pop = self.pop.crossover()
                self.pop.point_mutation()
                os.system('cls')
                g += 1
            e += 1
        print('Run time: ' + str(time.time()-t))


populatie = population(NRPOP, KEEPRATIO, DISCARDRATIO, MUTATION_PROB)
print(populatie.pop)
ga = GA(populatie, 500, 100, 15)
ga.run()
print(ga.pop.pop)