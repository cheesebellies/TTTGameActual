from game import Game
import algorithm
import copy
from pprint import pprint
import pickle
import random
import eval
from evolution import MidGameEvolution
import multiprocessing
import os
import math

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
    population = load_generation(modelname,25)
    evaluator = eval.SinglePlacementEvaluation()
    evaluator.tests = generate_boards()

    for gen in range(2000):
        for alg in population:
            alg.score = (evaluator.evaluate(alg))
        population.sort(key=lambda a: a.score, reverse = True)
        del population[-20:]
        npop = []
        for alg in population:
            for alg2 in population:
                if alg2 == alg: continue
                npop.append(alg.crossover(alg,alg2))
                
        

if __name__ == '__main__':
    main_script()