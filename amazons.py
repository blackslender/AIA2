# ======================== Class Player =======================================
class Player:
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name
        self.mov = 0

    def __str__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2), (row3, col3)] with:
        # (row1, col1): current position of selected amazon
        # (row2, col2): new position of selected amazon
        # (row3, col3): position of the square is shot
    def nextMove(self, state):
        self.mov += 1
        import copy
        # result = [(0,3),(5,3),(8,6)] # example move in wikipedia
        maxDepth = 1
        if self.mov > 10:
            maxDepth = 2
        if self.mov > 26:
            maxDepth = 3
        if self.mov > 30:
            maxDepth = 4
        mapsize = (10, 10)

        # Convert into State format
        class State:
            def __init__(self, state):
                self.l = dict()
                self.l['X'] = set()
                self.l['b'] = [(0, 0)]*4
                self.l['w'] = [(0, 0)]*4
                m, n = 0, 0
                for i in range(len(state)):
                    for j in range(len(state[0])):
                        if state[i][j] == 'X':
                            self.l['X'].add((i, j))
                        elif state[i][j] == 'w':
                            self.l['w'][m] = i, j
                            m += 1
                        elif state[i][j] == 'b':
                            self.l['b'][n] = i, j
                            n += 1

        state = State(state)

        # Static evaluation

        def evaluate(st, pChar, M, N):
            if pChar == 'w':
                eChar = 'b'
            else:
                eChar = 'w'

            res = 0
            track = []
            for i in range(mapsize[0]):
                track.append([True]*mapsize[1])

            for i in st.l['X']:
                track[i[0]][i[1]] = False
            for i in st.l[pChar]:
                track[i[0]][i[1]] = False

            def bfs(track, x, y):
                if x < 0 or x >= 10 or y < 0 or y >= 10:
                    return 0
                if not track[x][y]:
                    return 0
                res = 1
                track[x][y] = False
                res += bfs(track, x-1, y-1)
                res += bfs(track, x, y-1)
                res += bfs(track, x+1, y-1)
                res += bfs(track, x-1, y)
                res += bfs(track, x+1, y)
                res += bfs(track, x-1, y+1)
                res += bfs(track, x, y+1)
                res += bfs(track, x+1, y+1)
                return res

            for i in st.l[eChar]:
                res += bfs(track, i[0], i[1])
            return 100-res
        # maxDepth = (evaluate(state, self.str, 10, 10)//40)+1

        def validtile(tile, state):
            if tile[0] < 0 or tile[0] >= 10 or tile[1] < 0 or tile[1] >= 10:
                return False
            if tile in state.l['X']:
                return False
            if tile in state.l['b']:
                return False
            if tile in state.l['w']:
                return False
            return True

        def eChar(c):
            if c == 'w':
                return 'b'
            else:
                return 'w'

        def minimax(depth, st, pChar, bound):
            sE = evaluate(st, self.str, 10, 10)

            if depth >= maxDepth or sE >= 100:
                return [(0, 0), (0, 0), (0, 0), sE]
            p = st.l[pChar]
            x = st.l['X']
            overbound = False
            if depth % 2 == 0:
                # Max but not greater than $bound
                bestvalue = [(0, 0), (0, 0), (0, 0), 0]
                for i in range(len(p)):  # For each queen
                    # For each moving direction
                    for (m, n) in [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]:
                        home = copy.deepcopy(p[i])
                        # The tile where the queen move to

                        while validtile((p[i][0]+m, p[i][1]+n), st) and (not overbound):
                            p[i] = (p[i][0]+m, p[i][1]+n)
                            # For each shooting direction
                            for (mm, nn) in [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]:
                                # The tile where the queen shoot at
                                q = p[i]
                                while validtile((q[0]+mm, q[1]+nn), st) and (not overbound):
                                    q = (q[0]+mm, q[1]+nn)
                                    x.add(q)
                                    mov = [home, p[i], q]
                                    tmp = minimax(depth+1, st,
                                                  eChar(pChar), bestvalue[3])
                                    x.remove(q)
                                    if tmp[3] >= bestvalue[3]:
                                        bestvalue = mov+[tmp[3]]
                                    if bestvalue[3] >= bound:
                                        overbound = True

                        p[i] = home

                if overbound:
                    return [(0, 0), (0, 0), (0, 0), 101]
                else:
                    return bestvalue

            else:
                # Min but not lower than $bound
                bestvalue = [(0, 0), (0, 0), (0, 0), 101]
                for i in range(len(p)):  # For each queen
                    # For each moving direction
                    for (m, n) in [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]:
                        home = copy.deepcopy(p[i])
                        # The tile where the queen move to

                        while validtile((p[i][0]+m, p[i][1]+n), st) and (not overbound):
                            p[i] = (p[i][0]+m, p[i][1]+n)
                            # For each shooting direction
                            for (mm, nn) in [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1), (+1, -1), (+1, 0), (+1, +1)]:
                                # The tile where the queen shoot at
                                q = p[i]
                                while validtile((q[0]+mm, q[1]+nn), st) and (not overbound):
                                    q = (q[0]+mm, q[1]+nn)
                                    x.add(q)
                                    mov = [home, p[i], q]
                                    tmp = minimax(depth+1, st,
                                                  eChar(pChar), bestvalue[3])
                                    x.remove(q)
                                    if tmp[3] <= bestvalue[3]:
                                        bestvalue = mov+[tmp[3]]
                                    if bestvalue[3] <= bound:
                                        overbound = True

                        p[i] = home

                if overbound:
                    return [(0, 0), (0, 0), (0, 0), -1]
                else:
                    return bestvalue

            return [(0, 0), (0, 0), (0, 0), 0]

        result = minimax(0, state, self.str, 101)
        if result[:-1] == [(0, 0), (0, 0), (0, 0)]:
            return None
        return result[0], result[1], result[2]
