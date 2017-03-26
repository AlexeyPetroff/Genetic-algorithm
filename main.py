
import random

items = [(4, 12), (2,2), (2,1), (1,4), (1,1), (5,3), (7,4), (3,3), (1,4), (3,5)]


# Fitness function
def fit(o):
    value = 0
    weight = 0
    for i in range((len(o))):
        if o[i]==1:
            value+=items[i][0]
            weight+=items[i][1]
    if weight > 15:
        return 0
    return value


# Initialize first population by random
def rand_ind():
    ind = []
    for i in items:
        temp = random.randint(0, 1)
        ind.append(temp)
    return ind


def roulette_select(population, fitnesses, num):
    total_fitness = (sum(fitnesses))
    rel_fitness = [f/total_fitness for f in fitnesses]
    probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
    new_population = []
    for n in range(num):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probs[i]:
                new_population.append(individual)
                break
    return new_population


def cross_over(p1, p2):
    divider = random.randrange(1, len(p1))
    r = random.randint(0,1)
    if r == 0:
        child = p1[:divider]+p2[divider:]
    else:
        child = p2[:divider]+p1[divider:]
    return child


def mutation(entity):
    gen = random.randrange(0, len(entity))
    if entity[gen]==1:
        entity[gen]=0
    else:
        entity[gen]=1
    return entity

def fun(pop_size, number_of_generations, surv_size=0.4, child_proc = 0.5, mut_prob=0.05):
    bests=[]
    worsts=[]
    avgs=[]
    population=[]
    for i in range(pop_size):
        population.append(rand_ind())
    perfect = population[0]
    while number_of_generations>0:
        fits=[]
        for i in population:
            f = fit(i)
            fits.append(f)
            if fit(perfect)<f:
                perfect = i
        bests.append(max(fits))
        worsts.append(min(fits))
        avg = sum(fits) / len(fits)
        avgs.append(avg)
        new_population = roulette_select(population, fits, int(surv_size*pop_size))
        for c in range(int(child_proc*pop_size)):
            p1 = random.choice(new_population)
            p2 = random.choice(new_population)
            child = cross_over(p1,p2)
            new_population.append(child)
        missing = pop_size - len(new_population)
        for m in range(missing):
            new_population.append(rand_ind())
        for i in range(len(new_population)):
            r = random.random()
            if r <= mut_prob:
                new_population[i] = mutation(new_population[i])
        population = new_population
        number_of_generations -= 1
    return perfect
