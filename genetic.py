from random import random, randint, sample, choices, randrange
from typing import List, Optional, Callable, Tuple

#genome is one generated tune
Genome = List[int]

#population of genomes
Population = List[Genome]

#takes genome returns fitness value
FitnessFunc = Callable[[Genome], int]

#takes nothing and generates new solution
PopulateFunc = Callable[[], Population]

#takes population and fitness to select 2 parent solutions
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]

#takes genome and returns modified genome
MutationFunc = Callable[[Genome], Genome] 

#takes 2 genomes and returns 2 new crossed genomes
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]

PrinterFunc = Callable[[Population, int, FitnessFunc], None]

#genome for 1 solution list of 1 & 0 of length k
def genMelody(length: int) -> Genome:
    return choices([0, 1], k=length) 

#genertes tunes till population size chosen is filled
def genPop(size: int, genomek: int) -> Population:
    return [genMelody(genomek) for _ in range(size)]

#single point crossover takes 2 genomes as input parameters
def spcross(g1: Genome, g2: Genome) -> Tuple[Genome, Genome]:  
    if len(g1) != len(g2):
        raise ValueError("genome length is different") 

#must be same length for fair crossover, cant cut if length >2            
    length = len(g1) 
    if length < 2:
        return g1, g2

#random index chosen and returns 2 new genomes
    p = randint(1, length - 1)     
    return g1[0:p] + g2[p:], g2[0:p] + g2[p:]
                      
#at random indexes switches 1 and 0 if depending on a random probability
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))

# -1 because absolute value of abs(0-1) is 1 
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome
     
#takes population and Fitnessfunc as paraameters and returns genomes fitness
def fpop(population: Population, fitfunc: FitnessFunc) -> int:
    return sum([fitfunc(genome) for genome in population]) 

#selects 2 genomes depending on their fitness rating
def selectparents(population: Population, fitfunc: FitnessFunc) -> Population:
    return sample(
        population=weights(population, fitfunc), 
        k=2)


def weights(population: Population, fitfunc: FitnessFunc) -> Population:
    result = []

    for gene in population:
        result += [gene] * int(fitfunc(gene)+1)

    return result


def sortpop(population: Population, fitfunc: FitnessFunc) -> Population:
    return sorted(population, key=fitfunc, reverse=True) 


def transstr(genome: Genome) -> str:
    return "".join(map(str, genome))


def output(population: Population, generation_id: int, fitfunc: FitnessFunc):
    print("GENERATION %02d" % generation_id)
    print("=============")
    print("Population: [%s]" % ", ".join([transstr(gene) for gene in population]))
    print("Avg. Fitness: %f" % (fpop(population, fitfunc) / len(population)))
    sorted_population = sortpop(population, fitfunc)
    print(
        "Best: %s (%f)" % (transstr(sorted_population[0]), fitfunc(sorted_population[0])))
    print("Worst: %s (%f)" % (transstr(sorted_population[-1]),
                              fitfunc(sorted_population[-1])))
    print("")

    return sorted_population[0]

#takes the following parameters to run  
def startgen(
        spopulate: PopulateFunc,
        fitfunc: FitnessFunc, 

#if fitness of best solution exceeds this limit then done
        fitness_limit: int, 

#following initialised with default implementations    
        selectfunc: SelectionFunc = selectparents,
        crossfunc: CrossoverFunc = spcross,
        mutfunc: MutationFunc = mutation, 
        
#max number of evolutions if not reached limit        
        generationmax: int = 50, 

#first generation by calling populate function         
        printer: Optional[PrinterFunc] = None) \
        -> Tuple[Population, int]:
    population = spopulate()

#loop for generation limit
    i = 0
    for i in range(generationmax):

#sorting the population by fitness so best is top
        population = sorted(population, key=lambda genome: fitfunc(genome), reverse=True)

        if printer is not None:
            printer(population, i, fitfunc)

#sorting by fitness helps check if fitness limit reached
        if fitfunc(population[0]) >= fitness_limit:
            break

#elitism to keep top 2 solutions
        next_generation = population[0:2]

#to generate next generation, 2 parents, loop half length
        for j in range(int(len(population) / 2) - 1):

            #call selection for parents
            parents = selectfunc(population, fitfunc)

            #crossover called for parents to generate new offspring 
            offspring_a, offspring_b = crossfunc(parents[0], parents[1])

            #increase variety by mutating each offspring 
            offspring_a = mutfunc(offspring_a)
            offspring_b = mutfunc(offspring_b)

            #offspring is now the next generation after cross and mutation 
            next_generation += [offspring_a, offspring_b]

#replace population with next generation 
        population = next_generation

    return population, i 
