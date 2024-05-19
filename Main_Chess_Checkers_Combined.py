import tkinter as tk
from tkinter import messagebox
import random

class GameSelection:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Selection")
        self.label = tk.Label(master, text="Select a game:", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.chess_button = tk.Button(master, text="Chess", font=("Helvetica", 14), command=self.start_chess_game)
        self.chess_button.pack(pady=10)
        self.checkers_button = tk.Button(master, text="Checkers", font=("Helvetica", 14), command=self.start_checkers_game)
        self.checkers_button.pack(pady=10)

    def start_chess_game(self):
        self.master.destroy()  # Close game selection window
        root = tk.Tk()
        gui = DifficultySelection(root)
        root.mainloop()

    def start_checkers_game(self):
        self.master.destroy()  # Close game selection window
        from Checkers_run import main
        root = tk.Tk()
        game = main()
        root.mainloop()
class DifficultySelection:
    def __init__(self, master):
        self.master = master
        self.master.title("Select Difficulty")
        self.label = tk.Label(master, text="Select Difficulty:", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.easy_button = tk.Button(master, text="Easy", font=("Helvetica", 14), command=self.select_easy)
        self.easy_button.pack(pady=10)
        self.medium_button = tk.Button(master, text="Medium", font=("Helvetica", 14), command=self.select_medium)
        self.medium_button.pack(pady=10)
        self.hard_button = tk.Button(master, text="Hard", font=("Helvetica", 14), command=self.select_hard)
        self.hard_button.pack(pady=10)

    def select_easy(self):
        self.start_game("easy")

    def select_medium(self):
        self.start_game("medium")

    def select_hard(self):
        self.start_game("hard")

    def start_game(self, difficulty):
        self.master.destroy()  # Close difficulty selection window
        root = tk.Tk()
        gui = ChessGUI(root, difficulty)
        root.mainloop()


class ChessGUI:
    def __init__(self, master, difficulty):
        self.master = master
        self.master.title("Chess Game")
        self.canvas = tk.Canvas(master, width=640, height=640)
        self.canvas.pack()
        self.board = ChessGame()
        self.draw_board()
        self.selected_piece = None
        self.valid_moves = []
        self.canvas.bind("<Button-1>", self.click_handler)
        self.difficulty = difficulty

    def get_piece_symbol(self, piece):
        """
        Get Unicode chess piece symbol based on the character piece.

        Args:
            piece (str): Character representing the chess piece.

        Returns:
            str: Unicode symbol representing the chess piece.
        """
        if piece == 'P':
            return '♟'  # White pawn
        elif piece == 'N':
            return '♞'  # White knight
        elif piece == 'B':
            return '♝'  # White bishop
        elif piece == 'R':
            return '♜'  # White rook
        elif piece == 'Q':
            return '♛'  # White queen
        elif piece == 'K':
            return '♚'  # White king
        elif piece == 'p':
            return '♙'  # Black pawn
        elif piece == 'n':
            return '♘'  # Black knight
        elif piece == 'b':
            return '♗'  # Black bishop
        elif piece == 'r':
            return '♖'  # Black rook
        elif piece == 'q':
            return '♕'  # Black queen
        elif piece == 'k':
            return '♔'  # Black king
        else:
            return ''

    def draw_board(self):
        self.canvas.delete("all")  # Clear previous drawings
        for i in range(8):
            for j in range(8):
                color = "#FFCE9E" if (i + j) % 2 == 0 else "#D18B47"
                self.canvas.create_rectangle(j * 80, i * 80, (j + 1) * 80, (i + 1) * 80, fill=color)
                piece = self.board.board[i][j]
                if piece != '.':
                    self.canvas.create_text(j * 80 + 40, i * 80 + 40, text=self.get_piece_symbol(piece), font=("Helvetica", 32))

    def highlight_square(self, row, col, color="#00FF00"):
        x0, y0 = col * 80, row * 80
        x1, y1 = (col + 1) * 80, (row + 1) * 80
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=4)

    def click_handler(self, event):
        col = event.x // 80
        row = event.y // 80
        if self.selected_piece is None:
            self.selected_piece = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            self.highlight_selected_piece()
            self.highlight_valid_moves()
        else:
            start = self.selected_piece
            end = (row, col)
            if end in self.valid_moves:
                piece = self.board.board[start[0]][start[1]]
                self.board.board[start[0]][start[1]] = '.'
                self.board.board[end[0]][end[1]] = piece
                if self.board.is_in_check("player"):
                    self.board.board[end[0]][end[1]] = '.'
                    self.board.board[start[0]][start[1]] = piece
                    messagebox.showinfo("Illegal Move", "You cannot remain in check!")
                else:
                    if piece.lower() == 'p' and (end[0] == 0 or end[0] == 7):
                        # If pawn reaches the end, prompt user to choose promotion
                        promotion_choice = messagebox.askquestion("Pawn Promotion",
                                                                  "Pawn reached the end. Promote to Queen?")
                        if promotion_choice == 'yes':
                            self.board.board[end[0]][end[1]] = 'Q' if piece.isupper() else 'q'
                        else:
                            self.board.board[end[0]][end[1]] = piece
                    self.draw_board()  # Redraw the board
                    if self.board.is_checkmate():
                        messagebox.showinfo("Game Over", "Checkmate! Player wins!")
                    elif self.board.is_stalemate():
                        messagebox.showinfo("Game Over", "Stalemate! It's a draw.")
                    else:
                        self.board.current_player = "ai"
                        self.ai_move()
            self.clear_highlights()
            self.selected_piece = None
            self.valid_moves = []

    def highlight_selected_piece(self):
        if self.selected_piece:
            row, col = self.selected_piece
            self.highlight_square(row, col, color="blue")

    def highlight_valid_moves(self):
        for move in self.valid_moves:
            self.highlight_square(move[0], move[1], color="green")

    def clear_highlights(self):
        self.canvas.delete("highlight")

    def get_valid_moves(self, row, col):
        piece = self.board.board[row][col]
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.board.is_valid_move((row, col), (i, j)):
                    valid_moves.append((i, j))
        return valid_moves

    def ai_move(self):
        if self.difficulty == "easy":
            start, end = self.board.ai_move_easy()
        elif self.difficulty == "medium":
            start, end = self.board.ai_move_medium()
        else:
            start, end = self.board.ai_move_hard()

        piece = self.board.board[start[0]][start[1]]
        self.board.board[start[0]][start[1]] = '.'
        self.board.board[end[0]][end[1]] = piece

        if self.board.is_in_check("computer"):
            self.board.board[end[0]][end[1]] = '.'
            self.board.board[start[0]][start[1]] = piece
            messagebox.showinfo("Illegal Move", "AI cannot remain in check!")
        else:
            if piece.lower() == 'p' and (end[0] == 0 or end[0] == 7):
                # Automatically promote AI player's pawn to queen
                self.board.board[end[0]][end[1]] = 'Q' if piece.isupper() else 'q'
            self.draw_board()  # Redraw the board after AI's move

            if self.board.is_checkmate():
                messagebox.showinfo("Game Over", "Checkmate! AI wins!")
            elif self.board.is_stalemate():
                messagebox.showinfo("Game Over", "Stalemate! It's a draw.")
            else:
                self.board.current_player = "player"

    def promote_pawn(self, end):
        promote_window = tk.Toplevel(self.master)
        promote_window.title("Pawn Promotion")
        promote_window.geometry("200x200")

        promote_label = tk.Label(promote_window, text="Choose promotion piece:")
        promote_label.pack(pady=10)

        promote_pieces = ["Queen", "Rook", "Knight", "Bishop"]
        for piece in promote_pieces:
            button = tk.Button(promote_window, text=piece, command=lambda p=piece: self.handle_promotion(end, p))
            button.pack()

    def handle_promotion(self, end, piece):
        self.board.board[end[0]][end[1]] = piece[0].upper()  # Set the chosen piece on the board
        self.draw_board()  # Redraw the board to reflect the promotion


class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = "player"
        self.piece_names = {"P": "Pawn", "N": "Knight", "B": "Bishop", "R": "Rook", "Q": "Queen", "K": "King"}

    def create_board(self):
        board = []
        for _ in range(8):
            board.append(['.'] * 8)
        board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        board[1] = ['p'] * 8
        board[6] = ['P'] * 8
        board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        return board

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def is_valid_move(self, start, end, board=None):
        if board is None:
            board = self.board

        if start == end:
            return False
        if not (0 <= start[0] < 8 and 0 <= start[1] < 8 and 0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        piece = board[start[0]][start[1]]
        target_piece = board[end[0]][end[1]]

        if piece == '.':
            return False
        if (piece.islower() and self.current_player == "ai") or (piece.isupper() and self.current_player == "player"):
            return False
        if target_piece != '.' and (
                (target_piece.islower() and piece.islower()) or (target_piece.isupper() and piece.isupper())):
            return False
        # Disallow capturing the king
        if target_piece.lower() == 'k':
            return False

        # Check piece-specific rules
        if piece.lower() == 'p':
            return self.is_valid_pawn_move(start, end, piece, target_piece, board)
        elif piece.lower() == 'n':
            return self.is_valid_knight_move(start, end, piece)
        elif piece.lower() == 'b':
            return self.is_valid_bishop_move(start, end, piece, board)
        elif piece.lower() == 'r':
            return self.is_valid_rook_move(start, end, piece, board)
        elif piece.lower() == 'q':
            return self.is_valid_queen_move(start, end, piece, board)
        elif piece.lower() == 'k':
            return self.is_valid_king_move(start, end, piece)

        return False

    def is_valid_move_check(self, start, end, board=None):
        if board is None:
            board = self.board

        if start == end:
            return False
        if not (0 <= start[0] < 8 and 0 <= start[1] < 8 and 0 <= end[0] < 8 and 0 <= end[1] < 8):
            return False

        piece = board[start[0]][start[1]]
        target_piece = board[end[0]][end[1]]

        if piece == '.':
            return False
        if (piece.islower() and self.current_player == "ai") or (piece.isupper() and self.current_player == "player"):
            return False
        if target_piece != '.' and (
                (target_piece.islower() and piece.islower()) or (target_piece.isupper() and piece.isupper())):
            return False

        # Check piece-specific rules
        if piece.lower() == 'p':
            return self.is_valid_pawn_move(start, end, piece, target_piece, board)
        elif piece.lower() == 'n':
            return self.is_valid_knight_move(start, end, piece)
        elif piece.lower() == 'b':
            return self.is_valid_bishop_move(start, end, piece, board)
        elif piece.lower() == 'r':
            return self.is_valid_rook_move(start, end, piece, board)
        elif piece.lower() == 'q':
            return self.is_valid_queen_move(start, end, piece, board)
        elif piece.lower() == 'k':
            return self.is_valid_king_move(start, end, piece)

        return False

    def is_valid_pawn_move(self, start, end, piece, target_piece, board):
        if start[1] == end[1]:
            if target_piece != '.':
                return False
            if piece.isupper() and start[0] - end[0] == 1:
                return True
            elif piece.islower() and end[0] - start[0] == 1:
                return True
            elif piece.isupper() and start[0] == 6 and end[0] == 4 and board[5][start[1]] == '.':
                return True
            elif piece.islower() and start[0] == 1 and end[0] == 3 and board[2][start[1]] == '.':
                return True
        elif abs(start[1] - end[1]) == 1:
            if target_piece == '.':
                return False
            if piece.isupper() and start[0] - end[0] == 1:
                return True
            elif piece.islower() and end[0] - start[0] == 1:
                return True
        return False

    def is_valid_knight_move(self, start, end, piece):
        x, y = abs(start[0] - end[0]), abs(start[1] - end[1])
        return (x, y) in [(1, 2), (2, 1)]

    def is_valid_bishop_move(self, start, end, piece, board):
        x, y = abs(start[0] - end[0]), abs(start[1] - end[1])
        if x != y:
            return False
        dx = 1 if end[0] > start[0] else -1
        dy = 1 if end[1] > start[1] else -1
        i, j = start[0] + dx, start[1] + dy
        while (i, j) != end:
            if board[i][j] != '.':
                return False
            i += dx
            j += dy
        return True

    def is_valid_rook_move(self, start, end, piece, board):
        if start[0] == end[0]:
            step = 1 if end[1] > start[1] else -1
            for j in range(start[1] + step, end[1], step):
                if board[start[0]][j] != '.':
                    return False
            return True
        elif start[1] == end[1]:
            step = 1 if end[0] > start[0] else -1
            for i in range(start[0] + step, end[0], step):
                if board[i][start[1]] != '.':
                    return False
            return True
        return False

    def is_valid_queen_move(self, start, end, piece, board):
        return self.is_valid_bishop_move(start, end, piece, board) or self.is_valid_rook_move(start, end, piece, board)

    def is_valid_king_move(self, start, end, piece):
        x, y = abs(start[0] - end[0]), abs(start[1] - end[1])
        return x <= 1 and y <= 1

    def player_move(self):
        while True:
            try:
                move = input("Enter your move (e.g., e2e4): ")
                start, end = (int(move[1]) - 1, ord(move[0]) - ord('a')), (int(move[3]) - 1, ord(move[2]) - ord('a'))
                if self.is_valid_move(start, end) and not self.leaves_player_in_check(start, end):
                    return start, end
                else:
                    print("Invalid move! Please try again.")
            except ValueError:
                print("Invalid move format! Please enter a move like e2e4.")

    def ai_move_easy(self):
        unprotected_pieces = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].islower() and self.current_player == "ai":
                    for x in range(8):
                        for y in range(8):
                            if self.is_valid_move((i, j), (x, y)) and self.board[x][y].isupper():
                                unprotected_pieces.append(((i, j), (x, y)))

        if unprotected_pieces:
            unprotected_pieces.sort(key=lambda x: abs(x[0][0] - x[1][0]) + abs(x[0][1] - x[1][1]))
            return unprotected_pieces[0]

        return self.rand_move()

    def rand_move(self):
        while True:
            start = (random.randint(0, 7), random.randint(0, 7))
            end = (random.randint(0, 7), random.randint(0, 7))
            if self.is_valid_move(start, end) and not self.leaves_player_in_check(start, end):
                return start, end

    def ai_move_medium(self):
        _, move = self.minimax(self.board, 2, float('-inf'), float('inf'), True)
        return move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for start_x in range(8):
                for start_y in range(8):
                    for end_x in range(8):
                        for end_y in range(8):
                            if self.is_valid_move((start_x, start_y), (end_x, end_y), board=board):
                                temp_board = [row[:] for row in board]
                                piece = temp_board[start_x][start_y]
                                temp_board[start_x][start_y] = '.'
                                temp_board[end_x][end_y] = piece
                                eval, _ = self.minimax(temp_board, depth - 1, alpha, beta, False)
                                if eval > max_eval:
                                    max_eval = eval
                                    best_move = ((start_x, start_y), (end_x, end_y))
                                alpha = max(alpha, eval)
                                if beta <= alpha:
                                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for start_x in range(8):
                for start_y in range(8):
                    for end_x in range(8):
                        for end_y in range(8):
                            if self.is_valid_move((start_x, start_y), (end_x, end_y), board=board):
                                temp_board = [row[:] for row in board]
                                piece = temp_board[start_x][start_y]
                                temp_board[start_x][start_y] = '.'
                                temp_board[end_x][end_y] = piece
                                eval, _ = self.minimax(temp_board, depth - 1, alpha, beta, True)
                                if eval < min_eval:
                                    min_eval = eval
                                    best_move = ((start_x, start_y), (end_x, end_y))
                                beta = min(beta, eval)
                                if beta <= alpha:
                                    break
            return min_eval, best_move

    def ai_move_hard(self):
        current_depth = 0
        best_move = None
        best_value = -float('inf')
        for _ in range(500):  # number of iterations
            move = self.get_random_move()
            value = self.monte_carlo_tree_search(move, current_depth)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move

    def get_random_move(self):
        while True:
            start = (random.randint(0, 7), random.randint(0, 7))
            end = (random.randint(0, 7), random.randint(0, 7))
            if self.is_valid_move(start, end):
                return start, end

    def monte_carlo_tree_search(self, move, current_depth):
        if current_depth == 0:
            return self.rollout(move)
        else:
            value = 0
            for _ in range(10):  # number of child nodes
                child_move = self.get_random_move()
                value += self.monte_carlo_tree_search(child_move, current_depth - 1)
            return value / 10  # average value

    def rollout(self, move):
        temp_board = [row[:] for row in self.board]  # Create a copy of the board
        temp_board[move[1][0]][move[1][1]] = temp_board[move[0][0]][move[0][1]]
        temp_board[move[0][0]][move[0][1]] = '.'

        if self.is_in_check("player", temp_board):
            return 1
        elif self.is_in_check("computer", temp_board):
            return -1
        else:
            return 0

    def leaves_player_in_check(self, start, end):
        temp_board = [row[:] for row in self.board]  # Create a copy of the board
        temp_board[end[0]][end[1]] = temp_board[start[0]][start[1]]
        temp_board[start[0]][start[1]] = '.'

        return self.is_in_check("player" if self.current_player == "player" else "computer", temp_board)

    def is_in_check(self, color, board=None):
        if board is None:
            board = self.board

        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if (color == "player" and piece.isupper()) or (color == "computer" and piece.islower()):
                    if piece.lower() == 'p':
                        if color == "player":
                            if self.is_valid_pawn_move((i, j), (i - 1, j + 1), piece, '.', board=board):
                                return True
                            if self.is_valid_pawn_move((i, j), (i - 1, j - 1), piece, '.', board=board):
                                return True
                        else:
                            if self.is_valid_pawn_move((i, j), (i + 1, j + 1), piece, '.', board=board):
                                return True
                            if self.is_valid_pawn_move((i, j), (i + 1, j - 1), piece, '.', board=board):
                                return True
                    else:
                        for x in range(8):
                            for y in range(8):
                                if self.is_valid_move_check((i, j), (x, y), board=board) and board[x][y].lower() == 'k':
                                    return True
        return False

    def is_stalemate(self):
        # Check if the current player has no legal moves
        for i in range(8):
            for j in range(8):
                if (self.current_player == "player" and self.board[i][j].islower()) or (
                        self.current_player == "ai" and self.board[i][j].isupper()):
                    for x in range(8):
                        for y in range(8):
                            if self.is_valid_move((i, j), (x, y)) and not self.leaves_player_in_check((i, j), (x, y)):
                                return False
        return True

    def evaluate(self, board):
        # Simple evaluation function, counts the material balance
        score = 0
        for row in board:
            for piece in row:
                if piece == 'P':
                    score += 1
                elif piece == 'N':
                    score += 3
                elif piece == 'B':
                    score += 3
                elif piece == 'R':
                    score += 5
                elif piece == 'Q':
                    score += 9
                elif piece == 'p':
                    score -= 1
                elif piece == 'n':
                    score -= 3
                elif piece == 'b':
                    score -= 3
                elif piece == 'r':
                    score -= 5
                elif piece == 'q':
                    score -= 9
        return score

    def is_checkmate(self):
        # Check if the current player is in checkmate
        for i in range(8):
            for j in range(8):
                if (self.current_player == "player" and self.board[i][j].islower()) or (
                        self.current_player == "ai" and self.board[i][j].isupper()):
                    for x in range(8):
                        for y in range(8):
                            if self.is_valid_move((i, j), (x, y)) and not self.leaves_player_in_check((i, j), (x, y)):
                                return False
        return True

    def play(self):
        print("Welcome to the Python Chess Game!")
        difficulty = input("Select difficulty (easy, medium, hard): ").lower()
        while difficulty not in ["easy", "medium", "hard"]:
            print("Invalid difficulty level. Please select again.")
            difficulty = input("Select difficulty (easy, medium, hard): ").lower()
        self.print_board()

        while True:
            if self.current_player == "player":
                start, end = self.player_move()
            else:
                if difficulty == "easy":
                    start, end = self.ai_move_easy()
                elif difficulty == "medium":
                    start, end = self.ai_move_medium()
                else:
                    start, end = self.ai_move_hard()

            piece = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = '.'
            self.board[end[0]][end[1]] = piece



            # Check for pawn promotion
            if piece.lower() == 'p' and (end[0] == 0 or end[0] == 7):
                promotion_piece = 'Q' if piece.isupper() else 'q'  # Default to queen
                while promotion_piece not in ['Q', 'R', 'N', 'B']:
                    promotion_piece = input("Choose promotion piece (Q, R, N, B): ").upper()
                self.board[end[0]][end[1]] = promotion_piece

            self.print_board()

            if self.is_in_check("player"):
                print("Human player is in Check!")
                if self.is_checkmate():
                    print("Checkmate! AI wins!")
                    break
                if self.is_stalemate():
                    print("Stalemate! It's a draw.")
                    break
            if self.is_in_check("computer"):
                print("AI player is in Check!")
                if self.is_checkmate():
                    print("Checkmate! Human player wins!")
                    break
                if self.is_stalemate():
                    print("Stalemate! It's a draw.")
                    break

            if self.current_player == "player":
                self.current_player = "ai"
            else:
                self.current_player = "player"

            if self.is_in_check("player"):
                print("Human player is in Check!")
            if self.is_in_check("computer"):
                print("AI player is in Check!")

            if self.is_stalemate():
                print("Stalemate! It's a draw.")
                break


if __name__ == "__main__":
    root = tk.Tk()
    game_selection = GameSelection(root)
    root.mainloop()