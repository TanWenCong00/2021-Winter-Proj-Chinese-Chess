import pygame as p

HEIGHT = 800
WIDTH = 720
ROWS = 9
COLS = 8
SQ_SIZE = HEIGHT / ROWS + 1
PIECE_SIZE = 0.89 * SQ_SIZE
CIRCLE_SIZE = 0.1 * SQ_SIZE
MAX_FPS = 15


def load_image(chessboard):
    for piece in chessboard.pieces:
        piece.img = p.transform.scale(p.image.load("Images/" + piece.name[0] + piece.name[3:] + ".gif"),
                                      (PIECE_SIZE, PIECE_SIZE))


def gui_board(chessboard):
    p.init()
    load_image(chessboard)
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Chinese Chess')
    img = p.image.load("Images/boardchess.gif")
    screen.fill(p.Color("white"))
    screen.blit(img, (0, 0))

    return screen


def draw_piece(screen, board_state):
    for row in range(10):
        for col in range(9):
            piece = board_state[row][col]
            if piece is not None:
                screen.blit(piece.img, p.Rect(col * PIECE_SIZE, row * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))


def get_sq_selected():
    # (x, y) pos of mouse
    location = p.mouse.get_pos()
    row = int(location[1] // PIECE_SIZE)
    col = int(location[0] // PIECE_SIZE)

    return row, col


def is_legal_piece(sq_selected, chessboard):
    piece = chessboard.board_state[sq_selected[0]][sq_selected[1]]
    if piece is not None:
        return chessboard.is_red_turn == piece.is_red
    else:
        return False


def show_legal_moves(screen, sq_selected, chessboard):
    piece = chessboard.board_state[sq_selected[0]][sq_selected[1]]
    legal_moves = piece.legal_moves(chessboard)
    for move in legal_moves:
        p.draw.circle(screen, "green",
                      (move[1] * PIECE_SIZE + 0.5 * PIECE_SIZE, move[0] * PIECE_SIZE + 0.5 * PIECE_SIZE),
                      CIRCLE_SIZE)
        p.display.update()


def move_piece(start_pos, end_pos, chessboard):
    # TODO 2: update history here
    piece = chessboard.board_state[start_pos[0]][start_pos[1]]
    if piece is not None:
        legal_moves = piece.legal_moves(chessboard)
        if end_pos in legal_moves:
            chessboard.remove_from_board(piece.name)
            chessboard.add_to_board(piece, end_pos[0], end_pos[1])
            return True

    return False


def show_checkmate(screen, chessboard):
    winner = "BLACK" if chessboard.is_red_turn else "RED"

    font = p.font.Font('freesansbold.ttf', 50)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(f'CHECKMATE\n{winner} WINS', True, "black")

    # create a rectangular object for the
    # text surface object
    text_rect = text.get_rect()

    # set the center of the rectangular object.
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)
    p.display.update()
    return


def show_check(screen):
    font = p.font.Font('freesansbold.ttf', 50)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('CHECK', True, "black")

    # create a rectangular object for the
    # text surface object
    text_rect = text.get_rect()

    # set the center of the rectangular object.
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)
    p.display.update()
    return
