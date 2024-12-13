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
        
        is_swap = res[0] < 0.5
        mi = 0
        t=-99.0
        for i,v in enumerate(res[1:17]):
            if v > t:
                t=v
                mi=i
        mf = 0
        t =-99.0
        for i, v in enumerate(res[17:]):
            if v>t:
                t=v
                mf=i
        xi=mi%4
        yi=int(mi/4)
        xf=mf%4
        yf=int(mf/4)
        return (is_swap,xi,yi,xf,yf)

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
    
    def evaluate(self, algorithm_one: Algorithm, algorithm_two: Algorithm, print_boards: bool = False):
        game = Game()
        for i in range(8):
            is_swap,xi,yi,xf,yf = self.get_inputs(algorithm_one.run([1] + game.alginp(1)))
            valid_move = 0
            if is_swap:
                valid_move = game.swap(1,xi,yi,xf,yf)
            else:
                valid_move = game.place(1,xi,yi)
            if game.winstate() != 0:
                # self.score += 10
                # self.score += 30-i
                if print_boards: print(game)
                break
            if valid_move != 0:
                self.score -= 2
            else:
                self.score += 1
            is_swap,xi,yi,xf,yf = self.get_inputs(algorithm_two.run([2] + game.alginp(2)))
            valid_move = 0
            if is_swap:
                valid_move = game.swap(2,xi,yi,xf,yf)
            else:
                valid_move = game.place(2,xi,yi)
            if game.winstate() != 0:
                if print_boards: print(game)
                break
            if print_boards: print(game)
        return self.score

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