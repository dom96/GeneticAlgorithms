#!/usr/bin/env python
# This is a genetic algorithm which finds solutions to getting 42 by only
# using numbers 0 through 9; +, -, * and / operators.

# I added some functions which slow down the process of mating heh.

import random, time
POPULATION = 10
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1 # This value determines the chance of a bit 'negating'
                    # i.e 0 to 1, 1 to 0

SLEEP = False # Whether to slow down the process using sleep()
SLEEP_TIME = 0.01 # Sleep time in seconds

SOLUTIONS = []

def encode(a):
    t = {'0':'0000','1':'0001','2':'0010','3':'0011',
        '4':'0100','5':'0101','6':'0110','7':'0111', '8':'1000', '9':'1001',
        '+':'1010','-':'1011','*':'1100','/':'1101'}
  
    return t[a]

def decode(gene):
    t = {'0000':'0','0001':'1','0010':'2','0011':'3',
        '0100':'4','0101':'5','0110':'6','0111':'7','1000':'8','1001':'9',
        '1010':'+','1011':'-','1100':'*','1101':'/'}
    try:
        return t[gene]
    except KeyError:
        return ' '

def isOp(gene):
    if gene == '+' or gene == '-' or gene == '*' or gene == '/':
        return True
    return False

def isFaultyGene(result, dgene):
    # Having; 5 5; doesn't make sense.
    # + +; doesn't either
    # 5 +; does
    if len(result) != 0:
        if not isOp(result[len(result)-1]) and not isOp(dgene):
            return True
        elif isOp(result[len(result)-1]) and isOp(dgene):
            return True
    else:
        if isOp(dgene):
            return True
    
    return False

def decodeChromosome(chromosome):
    result = []
    while chromosome != '':
        gene = chromosome[:4]
        chromosome = chromosome[4:]
        
        decodedGene = decode(gene)
        if not isFaultyGene(result, decodedGene) and decodedGene != ' ':
            result.append(decodedGene)
    
    if len(result[-1:]) != 0:
        if isOp(result[-1:][0]):
            result = result[:-1]
            
    return result

def execute(dchromosome):
    if len(dchromosome) != 0:
        print "Evaluating", " ".join(dchromosome)
        try:
            return int(eval(" ".join(dchromosome)))
        except ZeroDivisionError:
            print "Useless chromosome(ZeroDivision)"
            # This chromosome isn't doing too well, because it caused an exception heh.
            return 0
    else:
        print "Useless chromosome(Empty)"
        return 0
    
def fitness(value):
    return 42-value
    
def crossover(chromosome, chromosome2):
    random.seed()
    if random.random() < CROSSOVER_RATE:
        random.seed()
        rand = random.randint(4, min(len(chromosome), len(chromosome2))-1)
        
        first = chromosome[:rand]
        second = chromosome2[rand:]
        return first + second
    else:
        return chromosome

def mutate(chromosome):
    result = ""
    
    for i in chromosome:
        random.seed()
        if random.random() < MUTATION_RATE:
            if i == "1":
                result += "0"
            else:
                result += "1"
        else:
            result += i

    return result

def genChroms():
    result = []
    
    nums = {0:'0000', 1:'0001', 2:'0010', 3:'0011',
            4:'0100', 5:'0101', 6:'0110', 7:'0111', 8:'1000', 9:'1001'}
    ops = {0:'1010', 1:'1011', 2:'1100', 3:'1101'}
    
    for i in range(POPULATION):
        chrom = ""
        op = False
        for x in range(7):
            random.seed()
            
            if op:
                r = random.randint(0, 3)
                chrom += ops[r]
            else:
                r = random.randint(0, 8)
                chrom += nums[r]
            
            op = not op
        
        result.append(chrom)
    return result

def testChroms(chromosomes):
    global SOLUTIONS
    result = []
    for i in chromosomes:
        dChromosome = decodeChromosome(i)
        #print "Evaluating chromosome", i
        value = execute(dChromosome)
        fitnessLvl = fitness(value)
        if fitnessLvl == 0 and (not dChromosome in SOLUTIONS):
            SOLUTIONS.append(dChromosome)
            print "Solution found! -", dChromosome
        
        result.append((fitnessLvl, i))
    return result

def compareFitness(x, y):
    if abs(x[0]) == abs(y[0]):
        return 0
    elif abs(x[0]) > abs(y[0]):
        return 1
    else:
        return -1

def init():
    global SOLUTIONS
    SOLUTIONS = []
    
    generation = 0
    # Create random chromosomes
    chromosomes = genChroms()
    
    while generation < 50000:
        if SLEEP:
            time.sleep(SLEEP_TIME)
    
        # Test each chromosome
        chromsTested = testChroms(chromosomes)
        
        # Sort the chromosomes against their fitness, closer to 0 the better the fitness.
        chromsTested.sort(cmp=compareFitness)
    
        # New population
        chromosomes = []
        
        for t in range(POPULATION):
            # Apply roulette selection
            newChromsTested = []
            # Multiply the chromosomes; according to the fitness.
            for i in range(0, len(chromsTested)-1):
                for c in range(0, POPULATION-i):
                    newChromsTested.append(chromsTested[i])
            
            # Now choose the chromosomes to mate heh
            random.seed()
            rfirst = random.randint(0, len(newChromsTested)-1)
            random.seed()
            rsecond = random.randint(0, len(newChromsTested)-1)
            first = newChromsTested[rfirst][1]
            second = newChromsTested[rsecond][1]
            
            # Mate - Crossover
            child = crossover(first, second)
        
            # Mutate
            child = mutate(child)
            
            chromosomes.append(child)
        

        print "At generation", generation, "-", len(SOLUTIONS), "solutions"
        print chromosomes
        print ""
        generation += 1

        if SOLUTIONS != []:
            print "Break at generation", generation
            break

    print SOLUTIONS

if __name__ == "__main__":
    init()
