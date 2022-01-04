from Chessboard import *
from GUI import *


def main():
    def update_screen():
        new_screen = gui_board(cbd)
        draw_piece(new_screen, cbd.board_state)
        p.display.update()

    cbd = ChessBoard("test")
    cbd.start_game()
    update_screen()

    sq_selected = ()  # no square selected, keep track of last click of user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(0, 0), (0, 1)]

    while not cbd.is_game_over:
        screen = gui_board(cbd)
        clock = p.time.Clock()

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()
            elif e.type == p.MOUSEBUTTONDOWN:  # player input
                update_screen()

                if len(player_clicks) == 0:
                    sq_selected = get_sq_selected()
                    if is_legal_piece(sq_selected, cbd):
                        show_legal_moves(screen, sq_selected, cbd)
                        player_clicks.append(sq_selected)
                elif len(player_clicks) == 1:
                    if sq_selected == get_sq_selected():
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = get_sq_selected()
                        player_clicks.append(sq_selected)

                        piece_moved = move_piece(player_clicks[0], player_clicks[1], cbd)

                        update_screen()

                        sq_selected = ()
                        player_clicks = []

                        if piece_moved:
                            cbd.is_red_turn = not cbd.is_red_turn
                            if cbd.is_checkmate():
                                show_checkmate(screen, cbd)
                                # add restart game
                            elif cbd.is_under_check():
                                show_check(screen)

            clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
