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
