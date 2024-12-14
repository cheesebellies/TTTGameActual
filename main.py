from game import Game
import algorithm
import copy
import time, datetime
from pprint import pprint
import pickle
import random
import eval
from evolution import MidGameEvolution
import multiprocessing
import os
import math

def generate_boards():
    boards = []
    for i in range(16):
        g = [[0 for a in range(4)] for b in range(4)]
        g[int(i/4)][int(i%4)] = 1
        boards.append(g)
    for i in range(15):
        for j in range(30):
            g = [[0 for a in range(4)] for b in range(4)]
            for l in range(i+2):
                g[random.randint(0,3)][random.randint(0,3)] = (l%2) + 1
            boards.append(g)
    return boards

def save_generation(modelname, population):
    if not os.path.isdir(f"genetic_models/{modelname}"):
            os.mkdir(f"genetic_models/{modelname}")
    for i, alg in enumerate(population):
        with open(f'genetic_models/{modelname}/model_{str(i)}.pkl', 'wb') as f:
            pickle.dump(alg, f)

def load_generation(modelname, popcount):
    population = []
    for i in range(popcount):
        with open(f'genetic_models/{modelname}/model_{str(i)}.pkl', 'rb') as f:
            population.append(pickle.load(f))
    return population

def SexLector(population: list, cull_ratio: int = 3):
    """Modify population in place to reproduce top scorers.
cull_ratio (>= 2) is set to a default of 3, meaning 1/3 the population is culled"""

    population.sort(key= lambda x: x.score, reverse=True)
    save_count = int((cull_ratio-1)*len(population)/(cull_ratio))
    before_count = len(population)
    for i, pop in enumerate(population):
        save_count -= 1
        if save_count <= 0:
            break
        pop.fitness += int((2*i)/save_count)+3
    for pop in population:
        pop.fitness -= 1
        if pop.fitness <= 0:
            population.remove(pop)
    spots_left = before_count - len(population)
    population.sort(key=lambda x: x.fitness, reverse=True)
    spops_weights = [i.fitness*5 for i in population]
    parents = [
        random.choices(population, weights = spops_weights, k = spots_left),
        random.choices(population, weights = spops_weights, k = spots_left)
    ]
    nalgs = []
    for i in range(len(parents[0])):
        nalg = parents[0][0].crossover(parents[0][i],parents[1][i])
        nalg.mutate(1.0)
        nalgs.append(nalg)
    population = population + nalgs
    return population



def main_script():
    modelname = "17x1x48x33_WSPE_100"
    # population = load_generation(modelname,25)
    population = [algorithm.Algorithm(17,1,48,33) for i in range(100)]
    tests = generate_boards()
    tte = 0.0
    
    for gen in range(2000):
        evaluator = eval.SinglePlacementEvaluation()
        evaluator.tests = tests
        gen_start_time = time.time()
        for alg in population:
            alg.score = (evaluator.evaluate(alg))
        population = SexLector(population,2)
        # population.sort(key=lambda a: a.score, reverse = True)
        # del population[-20:]
        # npop = []
        # for alg in population:
        #     for alg2 in population:
        #         if alg2 == alg: continue
        #         npop.append(alg.crossover(alg,alg2))
        # for alg in npop:
        #     alg.mutate(1.0)
        # # for alg in population:
        # #     alg.mutate(0.075)
        # population = population+npop
        # 54837 kill PID
        if gen%2 == 0:
            save_generation(modelname,population)
        with open(f"genetic_models/{ modelname}/score.txt","a") as f:
            f.write(str(population[0].score) + "\n")
        end_time = time.time()-gen_start_time
        tte += end_time
        eta = int(((tte/(gen+1))*2000) - tte)
        print(f"Generation {gen} complete. Time: {int(end_time)} | Left: {str(datetime.timedelta(seconds=eta))} | Score: {population[0].score}")
        

if __name__ == '__main__':
    main_script()