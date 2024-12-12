from algorithm import Algorithm
from eval import Evaluation
from game import Game
from copy import deepcopy

class MidGameEvolution:
    
    def __init__(self, algorithm: Algorithm, generations: int, children: int):
        self.from_parent = algorithm
        self.generations = generations
        self.children = children
    
    def turn(self, game: Game, turn: int, alg: Algorithm):
        for i in range(50):
            is_swap,xi,yi,xf,yf = Evaluation.get_inputs(alg.run([turn] + game.alginp(turn)))
            res = -1
            if is_swap:
                res = game.swap(turn, xi,yi,xf,yf)
            else:
                res = game.place(turn,xi,yi)
            if res == 0:
                return alg
            else:
                alg.randomize(.1)
        return alg
                
    
    def evolve(self):
        for generation in range(self.generations):
            print(generation)
            a1: Algorithm = deepcopy(self.from_parent)
            a2: Algorithm = deepcopy(self.from_parent)
            a1.randomize(0.2)
            a2.randomize(0.2)
            l=[a1,a2]
            game = Game()
            for turn in range(16):
                t = turn%2 + 1
                a = self.turn(game,t,l[t-1])
                l.remove(l[t-1])
                l.insert(t-1,a)
                s = game.winstate()
                if s == 1:
                    self.from_parent = a1
                    break
                else:
                    self.from_parent = a2
                    break
        return self.from_parent
    
                