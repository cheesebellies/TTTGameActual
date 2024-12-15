class Game:
    def __init__(self, board: list = None):
        if board:
            self.board = board
        else:
            self.board = [[0 for i in range(4)] for j in range(4)]

    def __str__(self):
        rstr = "Game Board:\n"
        for y in self.board:
            rstr += " "
            for x in y:
                rstr += (" " if x == 0 else ("X" if x == 1 else "O")) + " | "
            rstr = rstr[0:-3]
            rstr += "\n---------------\n"
        rstr = rstr[0:-17]
        return rstr

    def alginp(self, type: int = 1):
        if (type != 1) and (type != 2):
            type = 1
        t = self.board[0] + self.board[1] + self.board[2] + self.board[3]
        tr = []
        for i in t:
            if i == 0:
                tr.append(1.0)
            elif i == type:
                tr.append(0.0)
            elif i == abs(type-3):
                tr.append(-1.0)
        return tr

    def place(self, type: int, x: int, y: int):
        if (((type > 2) | (type < 1)) | ((x < 0) | (x > 3)) | ((y < 0) | (y > 3))):
            return 1
        if self.board[y][x] == 0:
            self.board[y][x] = type
            return 0
        else:
            return 2

    def swap(self, type: int, xi: int, yi: int, xf: int, yf: int):
        ot = abs(type-3)
        if ((((type > 2) | (type < 1)) | ((xi < 0) | (xi > 3)) | ((yi < 0) | (yi > 3))) | (((xf < 0) | (xf > 3)) | ((yf < 0) | (yf > 3)))):
            return 1
        if self.board[yi][xi] != ot:
            return 2
        if self.board[yf][xf] != 0:
            return 3
        t1 = self.board[yi][xi]
        t2 = self.board[yf][xf]
        self.board[yi][xi] = type
        self.board[yf][xf] = ot
        if self.winstate() == 0:
            return 0
        else:
            self.board[yi][xi] = t1
            self.board[yf][xf] = t2

    def winstate(self) -> int:
        for y in range(4):
            ct = -1
            wc = 0
            for x in range(4):
                pl = self.board[x][y] #get 90d rot val
                if pl == 0:
                    wc = 0
                    ct = -1
                    continue
                if pl == ct:
                    wc += 1
                else:
                    wc = 0
                ct = pl
                if wc == 2:
                    return ct

        for y in self.board:
            ct = -1
            wc = 0
            for x in y:
                if x == ct:
                    wc += 1
                else:
                    wc = 0
                ct = x
                if wc == 2:
                    return ct
        srsltr = [[1,0,0,1],[0,0,1,1]]
        srsrtl = [[0,0,1,1],[2,3,3,2]]
        for i in range(4):
            ct = -1
            wc = 0
            for j in range(3):
                pl = self.board[srsltr[0][i]+j][srsltr[1][i]+j]
                if pl == 0:
                    wc = 0
                    ct = -1
                    continue
                if pl == ct:
                    wc += 1
                else:
                    wc = 0
                ct = pl
                if wc == 2:
                    return ct
        for i in range(4):
            ct = -1
            wc = 0
            for j in range(3):
                pl = self.board[srsrtl[0][i]+j][srsrtl[1][i]-j]
                if pl == 0:
                    wc = 0
                    ct = -1
                    continue
                if pl == ct:
                    wc += 1
                else:
                    wc = 0
                ct = pl
                if wc == 2:
                    return ct
        for i in self.board:
            for j in i:
                if j == 0:
                    return 0
        return 3