class ChessPiece:
    def __init__(self, name, is_red):
        self.is_alive = True
        self.name = name
        self.is_red = is_red
        self.row = None
        self.col = None
        self.img = None

    def legal_moves(self, board):
        all_moves = self.all_moves(board.board_state)

        def simulate_move(new_pos):
            curr_row = self.row
            curr_col = self.col
            temp_piece = board.board_state[new_pos[0]][new_pos[1]]

            board.remove_from_board(self.name)
            board.add_to_board(self, new_pos[0], new_pos[1])
            is_legal = not board.is_under_check()
            board.remove_from_board(self.name)
            board.add_to_board(self, curr_row, curr_col)
            if temp_piece is not None:
                board.add_to_board(temp_piece, new_pos[0], new_pos[1])

            return is_legal

        return [move for move in all_moves if simulate_move(move)]


class Rook(ChessPiece):
    def __init__(self, name, is_red):
        super().__init__(name, is_red)

    def all_moves(self, board_state):
        moves = []
        # up
        for row in range(self.row + 1, 10, 1):
            if board_state[row][self.col] is None:
                moves.append((row, self.col))
            elif board_state[row][self.col].is_red != self.is_red:
                moves.append((row, self.col))
                break
            else:
                break

        # down
        for row in range(self.row - 1, -1, -1):
            if board_state[row][self.col] is None:
                moves.append((row, self.col))
            elif board_state[row][self.col].is_red != self.is_red:
                moves.append((row, self.col))
                break
            else:
                break

        # left
        for col in range(self.col - 1, -1, -1):
            if board_state[self.row][col] is None:
                moves.append((self.row, col))
            elif board_state[self.row][col].is_red != self.is_red:
                moves.append((self.row, col))
                break
            else:
                break

        # right
        for col in range(self.col + 1, 9, 1):
            if board_state[self.row][col] is None:
                moves.append((self.row, col))
            elif board_state[self.row][col].is_red != self.is_red:
                moves.append((self.row, col))
                break
            else:
                break

        return moves


class Horse(ChessPiece):
    def __init__(self, name, is_red):
        super().__init__(name, is_red)

    def all_moves(self, board_state):
        def is_pos_open(new_pos):
            return (9 >= new_pos[0] >= 0 and 8 >= new_pos[1] >= 0) and \
                   (board_state[new_pos[0]][new_pos[1]] is None or
                    board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)

        moves = []
        # up
        if 9 >= self.row + 1 >= 0 and board_state[self.row + 1][self.col] is None:
            next_pos = [(self.row + 2, self.col - 1), (self.row + 2, self.col + 1)]
            for pos in next_pos:
                if is_pos_open(pos):
                    moves.append(pos)

        # down
        if 9 >= self.row - 1 >= 0 and board_state[self.row - 1][self.col] is None:
            next_pos = [(self.row - 2, self.col - 1), (self.row - 2, self.col + 1)]
            for pos in next_pos:
                if is_pos_open(pos):
                    moves.append(pos)

        # left
        if 8 >= self.col - 1 >= 0 and board_state[self.row][self.col - 1] is None:
            next_pos = [(self.row + 1, self.col - 2), (self.row - 1, self.col - 2)]
            for pos in next_pos:
                if is_pos_open(pos):
                    moves.append(pos)

        # right
        if 8 >= self.col + 1 >= 0 and board_state[self.row][self.col + 1] is None:
            next_pos = [(self.row + 1, self.col + 2), (self.row - 1, self.col + 2)]
            for pos in next_pos:
                if is_pos_open(pos):
                    moves.append(pos)

        return moves


class Cannon(ChessPiece):
    def __init__(self, name, is_red):
        super().__init__(name, is_red)

    def all_moves(self, board_state):
        moves = []
        # up
        for row in range(self.row + 1, 10, 1):
            if board_state[row][self.col] is None:
                moves.append((row, self.col))
            else:
                # meet first piece
                for jump_row in range(row + 1, 10, 1):
                    if board_state[jump_row][self.col] is not None:
                        if board_state[jump_row][self.col].is_red != self.is_red:
                            moves.append((jump_row, self.col))
                        break
                break

        # down
        for row in range(self.row - 1, -1, -1):
            if board_state[row][self.col] is None:
                moves.append((row, self.col))
            else:
                # meet first piece
                for jump_row in range(row - 1, -1, -1):
                    if board_state[jump_row][self.col] is not None:
                        if board_state[jump_row][self.col].is_red != self.is_red:
                            moves.append((jump_row, self.col))
                        break
                break

        # left
        for col in range(self.col - 1, -1, -1):
            if board_state[self.row][col] is None:
                moves.append((self.row, col))
            else:
                # meet first piece
                for jump_col in range(col - 1, -1, -1):
                    if board_state[self.row][jump_col] is not None:
                        if board_state[self.row][jump_col].is_red != self.is_red:
                            moves.append((self.row, jump_col))
                        break
                break

        # right
        for col in range(self.col + 1, 9, 1):
            if board_state[self.row][col] is None:
                moves.append((self.row, col))
            else:
                # meet first piece
                for jump_col in range(col + 1, 9, 1):
                    if board_state[self.row][jump_col] is not None:
                        if board_state[self.row][jump_col].is_red != self.is_red:
                            moves.append((self.row, jump_col))
                        break
                break

        return moves


class Elephant(ChessPiece):
    def __init__(self, name, is_red):
        super().__init__(name, is_red)

    def all_moves(self, board_state):
        def is_pos_open(new_pos):
            if self.is_red:
                return (4 >= new_pos[0] >= 0 and 8 >= new_pos[1] >= 0) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)
            else:
                return (9 >= new_pos[0] >= 5 and 8 >= new_pos[1] >= 0) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)

        moves = []
        # up-right
        if 9 >= self.row + 1 >= 0 and 8 >= self.col + 1 >= 0 and board_state[self.row + 1][self.col + 1] is None:
            next_pos = (self.row + 2, self.col + 2)
            if is_pos_open(next_pos):
                moves.append(next_pos)

        # up-left
        if 9 >= self.row + 1 >= 0 and 8 >= self.col - 1 >= 0 and board_state[self.row + 1][self.col - 1] is None:
            next_pos = (self.row + 2, self.col - 2)
            if is_pos_open(next_pos):
                moves.append(next_pos)

        # down-right
        if 9 >= self.row - 1 >= 0 and 8 >= self.col + 1 >= 0 and board_state[self.row - 1][self.col + 1] is None:
            next_pos = (self.row - 2, self.col + 2)
            if is_pos_open(next_pos):
                moves.append(next_pos)

        # down-left
        if 9 >= self.row - 1 >= 0 and 8 >= self.col - 1 >= 0 and board_state[self.row - 1][self.col - 1] is None:
            next_pos = (self.row - 2, self.col - 2)
            if is_pos_open(next_pos):
                moves.append(next_pos)

        return moves


class Advisor(ChessPiece):
    def __init__(self, name, is_red):
        super().__init__(name, is_red)

    def all_moves(self, board_state):
        def is_pos_open(new_pos):
            if self.is_red:
                return (2 >= new_pos[0] >= 0 and 5 >= new_pos[1] >= 3) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)
            else:
                return (9 >= new_pos[0] >= 7 and 5 >= new_pos[1] >= 3) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)

        # only 4 moves
        moves = [(self.row + 1, self.col - 1),
                 (self.row + 1, self.col + 1),
                 (self.row - 1, self.col + 1),
                 (self.row - 1, self.col - 1)
                 ]

        moves = [move for move in moves if is_pos_open(move)]

        return moves


class General(ChessPiece):
    def __init__(self, name, is_red):
        super().__init__(name, is_red)

    def all_moves(self, board_state):
        def is_pos_open(new_pos):
            if self.is_red:
                return (2 >= new_pos[0] >= 0 and 5 >= new_pos[1] >= 3) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)
            else:
                return (9 >= new_pos[0] >= 7 and 5 >= new_pos[1] >= 3) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)

        # only 4 moves
        moves = [(self.row + 1, self.col),
                 (self.row - 1, self.col),
                 (self.row, self.col - 1),
                 (self.row, self.col + 1)
                 ]

        moves = [move for move in moves if is_pos_open(move)]

        return moves


class Pawn(ChessPiece):
    def __init__(self, name, is_red):
        super().__init__(name, is_red)

    def all_moves(self, board_state):
        def is_pos_open(new_pos):
            if self.is_red:
                return (9 >= new_pos[0] >= 0 and 8 >= new_pos[1] >= 0) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)
            else:
                return (9 >= new_pos[0] >= 0 and 8 >= new_pos[1] >= 0) and \
                       (board_state[new_pos[0]][new_pos[1]] is None or
                        board_state[new_pos[0]][new_pos[1]].is_red != self.is_red)

        if self.is_red:
            if self.row <= 4:
                moves = [(self.row + 1, self.col)]
            else:
                moves = [(self.row + 1, self.col),
                         (self.row, self.col - 1),
                         (self.row, self.col + 1)
                         ]
        else:
            if self.row > 4:
                moves = [(self.row - 1, self.col)]
            else:
                moves = [(self.row - 1, self.col),
                         (self.row, self.col - 1),
                         (self.row, self.col + 1)
                         ]

        moves = [move for move in moves if is_pos_open(move)]

        return moves
