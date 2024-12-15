from algorithm import Algorithm
from game import Game
import random
import copy

class Evaluation:
    def __init__(self, load_path: str = "tests/advanced.txt"):
        # self.algorithm = algorithm
        self.loadpath = load_path
        self.tests = []
        self.score = 0
        self.load_boards_from_file()

    @staticmethod
    def get_inputs(res: list):
        
        is_swap = bool(res[0] == 0.0)
        mi = res[0:17].index(max(res[0:17]))
        mf = res[17:].index(max(res[17:]))
        xi=mi%4
        yi=int(mi/4)
        xf=mf%4
        yf=int(mf/4)
        return (is_swap,xi,yi,xf,yf)
    
    def place_from_inputs(self, res: list, game: Game, type: int):
        is_swap,xi,yi,xf,yf = self.get_inputs(res)
        if is_swap:
            return game.swap(type,xi,yi,xf,yf)
        else:
            return game.place(type,xi,yi)

    def load_boards_from_file(self, load_path: str = None):
        with open(self.loadpath, 'r') as f:
            self.tests = eval(f.read())
    
    def reset_score(self):
        self.score = 0

class SinglePlacementEvaluation(Evaluation):
    
    def evaluate(self, algorithm: Algorithm, print_boards: bool = False):
        score = 0.0
        # locations = []
        c = 0
        for board in self.tests:
            # score_increase = (18.0)/(2*((c/90.0)+1.0))+0.25
            c += 1
            game = Game(copy.deepcopy(board))
            algorithm_input = game.alginp()
            result = algorithm.run([1] + algorithm_input)
            is_swap, xi, yi, xf, yf = self.get_inputs(result)
            success_code = 0
            if is_swap:
                success_code = game.swap(1,xi,yi,xf,yf)
            else:
                success_code = game.place(1,xi,yi)
            if success_code != 0:
                score -= 2#score_increase
            else:
                score += 1#score_increase
            if print_boards:
                print(game)
            # locations.append((xi,yi))
        # locations_set = set(locations)
        # self.score += (len(locations_set))*2
        return score

# class AutoDuelEvaluation(Evaluation):
    
#     def evaluate(self, algorithm: Algorithm, print_boards: bool = False):
        

class DuelEvaluation(Evaluation):
    
    def evaluate(self, algorithm_one: Algorithm, algorithm_two: Algorithm):
        game = Game()
        for i in range(8):
            a1r = self.place_from_inputs(algorithm_one.run(game.alginp(1)),game,1)
            a2r = self.place_from_inputs(algorithm_two.run(game.alginp(2)),game,2)
            if a1r == 0:
                a1r.score += 1.0
            else:
                a1r.score -= 1.0
            if a2r == 0:
                a2r.score += 1.0
            else:
                a2r.score -= 1.0
            ws = game.winstate()
            if ws == 0:
                continue
            elif ws == 3:
                a2r.score += 2.0
                a1r.score += 1.0
            elif ws == 1:
                a1r.score += 6.0
                a2r.score -= 3.0
            elif ws == 2:
                a2r.score += 6.0
                a1r.score -= 3.0
            return
                

class AutoDuelEvaluation(Evaluation):
    
    def evaluate(self, algorithm: Algorithm, print_boards: bool = False):
        game = Game()
        for i in range(16):
            t = i%2 + 1
            is_swap,xi,yi,xf,yf = self.get_inputs(algorithm.run([t] + game.alginp(t)))
            res = 0
            if is_swap:
                res = game.swap(t,xi,yi,xf,yf)
            else:
                res = game.place(t,xi,yi)
            if res == 0:
                self.score += 1
            else:
                self.score -= 1
        return self.score

# if __name__ == '__main__':
#     with open("tests/basic.txt", "w") as f:
#         t = []
#         for i in range(16):
#             g = Game()
#             g.board[int(i/4)][int(i%4)] = 1
#             t.append(g.board)
#         f.write(str(t))