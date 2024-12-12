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

def gres(res):
    is_swap = res[0] < 0.5
    xi = round(res[1]*3.0)
    yi = round(res[2]*3.0)
    xf = round(res[3]*3.0)
    yf = round(res[4]*3.0)
    return (is_swap,xi,yi,xf,yf)

def match(ai_one, ai_two):
    a1s = 0
    a2s = 0
    game = Game()
    # game = Game([
    #     [0, 1, 2, 1],
    #     [1, 0, 0, 0],
    #     [2, 0, 0, 2],
    #     [0, 1, 2, 0]
    # ])
    c = 0
    while (game.winstate() == 0) and (c < 17):
        c += 1
        board = game.alginp(1)
        res = ai_one.run([0.0] + board)
        r2 = 0
        is_swap,xi,yi,xf,yf = gres(res)
        if is_swap:
            r2 = game.swap(1,xi,yi,xf,yf)
        else:
            r2 = game.place(1,xi,yi)
        if r2 != 0:
            a1s -= 3
        else:
            a1s += 1
        board = game.alginp(2)
        res = ai_two.run([1.0] + board)
        r2 = 0
        is_swap,xi,yi,xf,yf = gres(res)
        if is_swap:
            r2 = game.swap(2,xi,yi,xf,yf)
        else:
            r2 = game.place(2,xi,yi)
        if r2 != 0:
            a2s -= 3
        else:
            a2s += 1
    w = game.winstate()
    if w == 1:
        a1s += 100
    elif w == 2:
        a2s += 100
    return (game, w, a1s, a2s)

def worker(a, e, q):
    l = q.get()
    s = e.evaluate(a)
    l.append(s)
    q.put(l)
    return

def generation(evaluator: eval.Evaluation, randomizer: float, versions: int, from_parent: algorithm.Algorithm) -> algorithm.Algorithm:
    alglist = [from_parent]
    reslist = {}
    for i in range(versions-1):
        nalg = copy.deepcopy(from_parent)
        nalg.mutate(randomizer)
        alglist.append(nalg)
    q = multiprocessing.Queue()
    q.put([])
    jobs = []
    for algorithm in alglist:
        job = multiprocessing.Process(daemon=True,target=worker,args=(algorithm,evaluator,q))
        job.start()
        jobs.append(job)
    for job in jobs:
        job.join()
    reslist: list = q.get()
    # print(reslist)
    v = max(reslist)
    hres = alglist[reslist.index(v)]
    print(str(v) + ":" + str(hres))
    return (hres, v)


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


def main_script():
    modelname = "17x1x48x33_GEN_WSPE_RELU"
    population = [algorithm.Algorithm(17,1,48,33) for i in range(25)]
    scores = []
    # gen_res = None
    # with open("new_models/17x1x60x33_SPE.pkl", "rb") as f:
        # gen_res = pickle.load(f) 
    evaluator = eval.SinglePlacementEvaluation()
    evaluator.tests = generate_boards()

    for gen in range(2000):
       # evaluator.tests = generate_boards()
        scores = []
        for alg in population:
            scores.append(evaluator.evaluate(alg))
       # print("\n".join([str(j) for j in scores]))
        # gen_res, gsc = generation(evaluator, 0.25*(1.0/(1.0+(math.e**(i/100.0))))+0.75, 15, gen_res)
        print("Generation " + str(gen) + " complete. Score: " + str(max(scores)) + "\n     " + str(population[scores.index(max(scores))]))
        if gen%5 == 0:
            if not os.path.isdir(f"genetic_models/{modelname}"):
                os.mkdir(f"genetic_models/{modelname}")
            for i, alg in enumerate(population):
                with open(f'genetic_models/{modelname}/model_{str(i)}.pkl', 'wb') as f:
                    pickle.dump(alg, f)
        with open(f'genetic_models/{modelname}/score.txt','a') as f:
            f.write("\n" + str(max(scores)))
        nscores = []
        npop = []
        for i in range(len(scores)):
            ms = max(scores)
            msi = scores.index(ms)
            nscores.append(ms)
            scores.pop(msi)
            npop.append(population[msi])
        population = npop
        scores = nscores
        cpop = population[0:5]
        nalgs = []
        for i in range(5):
            a = cpop[i]
            for j in range(5):
                b = cpop[j]
                if b == a: continue
                nalgs.append(population[0].crossover(a,b))
        for j in nalgs:
            j.mutate(0.5)
        cpop += nalgs
        population = cpop
        

if __name__ == '__main__':
    main_script()