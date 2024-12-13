from game import Game
import algorithm
import copy
import time
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

def main_script():
    modelname = "17x1x48x33_WSPE_25"
    # population = load_generation(modelname,25)
    population = [algorithm.Algorithm(17,1,48,33) for i in range(25)]
    tests = generate_boards()

    for gen in range(2000):
        evaluator = eval.SinglePlacementEvaluation()
        evaluator.tests = tests
        gen_start_time = time.time()
        for alg in population:
            alg.score = (evaluator.evaluate(alg))
        population.sort(key=lambda a: a.score, reverse = True)
        del population[-20:]
        npop = []
        for alg in population:
            for alg2 in population:
                if alg2 == alg: continue
                npop.append(alg.crossover(alg,alg2))
        for alg in npop:
            alg.mutate(1.0)
        for alg in population:
            alg.mutate(0.075)
        population = population+npop
        if gen%5 == 0:
            save_generation(modelname,population)
        print(f"Generation complete. Time: {int(time.time()-gen_start_time)} | Score: {population[0].score}")
        

if __name__ == '__main__':
    main_script()