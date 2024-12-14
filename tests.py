# from game import Game
# from algorithm import Algorithm, Node, Layer
# import pickle
# import eval
# alg = None

# with open("genetic_models/17x1x48x33_WSPE_25/model_0.pkl", "rb") as f:
#     alg = pickle.load(f)

# def get_inputs(res: list):
#     is_swap = res[0] < 0.5
#     xi = round(res[1]*3.0)
#     yi = round(res[2]*3.0)
#     xf = round(res[3]*3.0)
#     yf = round(res[4]*3.0)
#     return (is_swap,xi,yi,xf,yf)
# e = eval.SinglePlacementEvaluation()
# r = e.evaluate(alg,False)
# print(r)

# g = Game()
# while True:
#     print(g)
#     xi = int(input("x: "))
#     yi = int(input("y: "))
#     s = input("swap(y/n): ")=="y"
#     if s:
#         xf = int(input("x: "))
#         yf = int(input("y: "))
#         g.swap(1,xi,yi,xf,yf)
#     g.place(1,xi,yi)
#     res = alg.run([2] + g.alginp(2))
#     print(res)
#     is_swap,xi,yi,xf,yf = get_inputs(res)
#     if is_swap:
#         g.swap(2,xi,yi,xf,yf)
#     else:
#         g.place(2,xi,yi)
                
# # # # import random
# # # # boards = []
# # # # for i in range(500):
# # # #     b = ([[random.randint(0,2) for i in range(4)] for j in range(4)])
# # # #     if not (b in boards):
# # # #         boards.append(b) 


# # # # with open("tests/advanced.txt", "w") as f:
# # # #     f.write(str(boards))
# # # for i in range(500):
# # #     print(max(0.1*(1/max(0.1,(i*0.002))),0.05))

# p = [i for i in range(20)]
# print(p[0:10])


#     # for gen in range(2000):
#     #     pass
#        # evaluator.tests = generate_boards()
#     #     scores = []
#     #     print(len(population))
#     #     algscores = {}
#     #     for alg in population:
#     #         algscores[alg] = evaluator.evaluate(alg)
#     #    # print("\n".join([str(j) for j in scores]))
#     #     # gen_res, gsc = generation(evaluator, 0.25*(1.0/(1.0+(math.e**(i/100.0))))+0.75, 15, gen_res)
#     #     print("Generation " + str(gen) + " complete. Score: " + str(max(algscores.values())))
#     #     if gen%5 == 0:
#     #         if not os.path.isdir(f"genetic_models/{modelname}"):
#     #             os.mkdir(f"genetic_models/{modelname}")
#     #         for i, alg in enumerate(population.keys()):
#     #             pass
#     #             # with open(f'genetic_models/{modelname}/model_{str(i)}.pkl', 'wb') as f:
#     #             #     pickle.dump(alg, f)
#     #         n = [l for l in algscores.values()]
#     #         n.sort()
#     #         print(n)
#     #         print(population)
#     #     with open(f'genetic_models/{modelname}/score.txt','a') as f:
#     #         f.write("\n" + str(max(scores)))
#     #     nscores = []
#     #     npop = []
#     #     for j in range(len(scores)):
#     #         i = len(scores)-j-1
#     #         ms = max(scores)
#     #         msi = scores.index(ms)
#     #         nscores.append(ms)
#     #         scores.pop(msi)
#     #         npop.append(population[msi])
#     #     population = npop
#     #     scores = nscores
#     #     cpop = population[0:5]
#     #     nalgs = []
#     #     for i in range(5):
#     #         a = cpop[i]
#     #         for j in range(5):
#     #             b = cpop[j]
#     #             if b == a: continue
#     #             nalgs.append(population[0].crossover(a,b))
#     #     for j in nalgs:
#     #         j.mutate(1.0)
#     #     for j in cpop:
#     #         j.mutate(0.075)
#     #     cpop += nalgs
#     #     population = cpop
import datetime

tobj = datetime.datetime(datetime.timedelta(seconds=24523))
print(tobj.strftime())