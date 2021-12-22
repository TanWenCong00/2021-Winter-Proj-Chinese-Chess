from Chesspiece import *


class ChessBoard:
    def __init__(self, name):
        self.name = name
        self.board_state = [([None] * 9) for _ in range(10)]
        self.is_red_turn = True
        self.is_game_over = False
        self.winner = None
        self.pieces = []

    def start_game(self):
        r_l_rook = Rook("r_l_rook", True)
        self.add_to_board(r_l_rook, 0, 0)
        r_r_rook = Rook("r_r_rook", True)
        self.add_to_board(r_r_rook, 0, 8)
        r_l_horse = Horse("r_l_horse", True)
        self.add_to_board(r_l_horse, 0, 1)
        r_r_horse = Horse("r_r_horse", True)
        self.add_to_board(r_r_horse, 0, 7)
        r_l_cannon = Cannon("r_l_cannon", True)
        self.add_to_board(r_l_cannon, 2, 1)
        r_r_cannon = Cannon("r_r_cannon", True)
        self.add_to_board(r_r_cannon, 2, 7)
        r_l_elephant = Elephant("r_l_elephant", True)
        self.add_to_board(r_l_elephant, 0, 2)
        r_r_elephant = Elephant("r_r_elephant", True)
        self.add_to_board(r_r_elephant, 0, 6)
        r_l_advisor = Advisor("r_l_advisor", True)
        self.add_to_board(r_l_advisor, 0, 3)
        r_r_advisor = Advisor("r_r_advisor", True)
        self.add_to_board(r_r_advisor, 0, 5)
        r_general = General("r_1_general", True)
        self.add_to_board(r_general, 0, 4)
        r_1_pawn = Pawn("r_1_pawn", True)
        self.add_to_board(r_1_pawn, 3, 0)
        r_2_pawn = Pawn("r_2_pawn", True)
        self.add_to_board(r_2_pawn, 3, 2)
        r_3_pawn = Pawn("r_3_pawn", True)
        self.add_to_board(r_3_pawn, 3, 4)
        r_4_pawn = Pawn("r_4_pawn", True)
        self.add_to_board(r_4_pawn, 3, 6)
        r_5_pawn = Pawn("r_5_pawn", True)
        self.add_to_board(r_5_pawn, 3, 8)

        b_l_rook = Rook("b_l_rook", False)
        self.add_to_board(b_l_rook, 9, 0)
        b_r_rook = Rook("b_r_rook", False)
        self.add_to_board(b_r_rook, 9, 8)
        b_l_horse = Horse("b_l_horse", False)
        self.add_to_board(b_l_horse, 9, 1)
        b_r_horse = Horse("b_r_horse", False)
        self.add_to_board(b_r_horse, 9, 7)
        b_l_cannon = Cannon("b_l_cannon", False)
        self.add_to_board(b_l_cannon, 7, 1)
        b_r_cannon = Cannon("b_r_cannon", False)
        self.add_to_board(b_r_cannon, 7, 7)
        b_l_elephant = Elephant("b_l_elephant", False)
        self.add_to_board(b_l_elephant, 9, 2)
        b_r_elephant = Elephant("b_r_elephant", False)
        self.add_to_board(b_r_elephant, 9, 6)
        b_l_advisor = Advisor("b_l_advisor", False)
        self.add_to_board(b_l_advisor, 9, 3)
        b_r_advisor = Advisor("b_r_advisor", False)
        self.add_to_board(b_r_advisor, 9, 5)
        b_general = General("b_1_general", False)
        self.add_to_board(b_general, 9, 4)
        b_1_pawn = Pawn("b_1_pawn", False)
        self.add_to_board(b_1_pawn, 6, 0)
        b_2_pawn = Pawn("b_2_pawn", False)
        self.add_to_board(b_2_pawn, 6, 2)
        b_3_pawn = Pawn("b_3_pawn", False)
        self.add_to_board(b_3_pawn, 6, 4)
        b_4_pawn = Pawn("b_4_pawn", False)
        self.add_to_board(b_4_pawn, 6, 6)
        b_5_pawn = Pawn("b_5_pawn", False)
        self.add_to_board(b_5_pawn, 6, 8)

        return

    def add_to_board(self, piece, row, col):
        curr_piece = self.board_state[row][col]
        if curr_piece is not None:
            curr_piece.is_alive = False
        self.board_state[row][col] = piece
        # updates the attributes of the pieces to help with calculating moves
        piece.row = row
        piece.col = col
        piece.is_alive = True
        self.pieces.append(piece)
        return

    def lookup_piece_coord_by_name(self, name):
        for row in range(10):
            for col in range(9):
                piece = self.board_state[row][col]
                if piece is not None:
                    if piece.name == name:
                        return row, col

    def remove_from_board(self, name):
        coord = self.lookup_piece_coord_by_name(name)
        self.board_state[coord[0]][coord[1]] = None
        return

    def is_under_check(self):
        r_general_coord = self.lookup_piece_coord_by_name("r_1_general")
        b_general_coord = self.lookup_piece_coord_by_name("b_1_general")

        general_check = True
        # check if 飞将
        if r_general_coord[1] == b_general_coord[1]:
            for i in range(r_general_coord[0] + 1, b_general_coord[0], 1):
                if self.board_state[i][r_general_coord[1]] is not None:
                    general_check = False
            if general_check:
                return True

        # check if other pieces checking general
        def is_red_under_check():
            for row in range(10):
                for col in range(9):
                    piece = self.board_state[row][col]
                    if piece is not None:
                        if not piece.is_red:
                            if r_general_coord in piece.all_moves(self.board_state):
                                return True
            return False

        def is_black_under_check():
            for row in range(10):
                for col in range(9):
                    piece = self.board_state[row][col]
                    if piece is not None:
                        if piece.is_red:
                            if b_general_coord in piece.all_moves(self.board_state):
                                return True
            return False

        return is_red_under_check() if self.is_red_turn else is_black_under_check()

    def is_checkmate(self):
        legal_moves = []
        if self.is_red_turn:
            for row in range(10):
                for col in range(9):
                    piece = self.board_state[row][col]
                    if piece is not None:
                        if piece.is_red:
                            if piece.legal_moves(self):    # don't append if empty list of legal_moves
                                legal_moves.append(piece.legal_moves(self))
                                break                       # stop once there are legal moves
        else:
            for row in range(10):
                for col in range(9):
                    piece = self.board_state[row][col]
                    if piece is not None:
                        if not piece.is_red:
                            if piece.legal_moves(self):    # don't append if empty list of legal_moves
                                legal_moves.append(piece.legal_moves(self))
                                break                       # stop once there are legal moves

        if self.is_under_check() and legal_moves == []:
            self.winner = "Black" if self.is_red_turn else "Red"
            return True
        elif not legal_moves:
            # TODO 1: How to register a stalemate?
            print("This is a stalemate")
            return True
        else:
            return False
