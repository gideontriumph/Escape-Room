import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QSpacerItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TheSecretChamber(QWidget):
    def __init__(self):
        super().__init__()
        self.current_room = "start"
        self.attempts_remaining = 5
        self.initUI()

        # Initialize Tic-Tac-Toe game variables
        self.tic_tac_toe_board = [[None, None, None], [None, None, None], [None, None, None]]
        self.current_player = "X"
        self.games_won = 0
        self.games_lost = 0
        self.in_tic_tac_toe = False

    def initUI(self):
        self.setWindowTitle("The Secret Chamber")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.description_label = QLabel()
        self.puzzle_label = QLabel()
        self.answer_entry = QLineEdit()
        self.solve_button = QPushButton("Solve")

        self.solve_button.clicked.connect(self.solve_puzzle)
        self.answer_entry.returnPressed.connect(self.solve_button.click)

        layout.addWidget(self.description_label)
        layout.addWidget(self.puzzle_label)
        layout.addWidget(self.answer_entry)
        layout.addWidget(self.solve_button)

        # Add a Tic-Tac-Toe board to the UI
        self.tic_tac_toe_grid = QGridLayout()
        for row in range(3):
            for col in range(3):
                button = QPushButton()
                button.setFont(QFont("Arial", 18))
                button.setFixedSize(60, 60)
                button.clicked.connect(self.make_move)
                self.tic_tac_toe_grid.addWidget(button, row, col)
                button.hide()
        layout.addLayout(self.tic_tac_toe_grid)

        # Add some spacing to separate the Tic-Tac-Toe board from the other elements
        spacer = QSpacerItem(1, 10)
        layout.addItem(spacer)

        self.setLayout(layout)
        self.show_room()

    def show_room(self):
        room_data = rooms[self.current_room]
        self.description_label.setText(room_data["description"])
        if "puzzle" in room_data:
            self.puzzle_label.setText(f"Riddle: {room_data['puzzle']}")
            self.answer_entry.show()
            self.solve_button.show()
            self.answer_entry.clear()
            # Hide the Tic-Tac-Toe board for riddles
            self.hide_tic_tac_toe_board()
        else:
            self.puzzle_label.clear()
            self.answer_entry.hide()
            self.solve_button.hide()
            # Show the Tic-Tac-Toe board after escaping
            if self.in_tic_tac_toe:
                self.show_tic_tac_toe_board()

    def make_move(self):
        # Handle a Tic-Tac-Toe move
        button = self.sender()
        row, col = self.tic_tac_toe_grid.getItemPosition(self.tic_tac_toe_grid.indexOf(button))
        if self.tic_tac_toe_board[row][col] is None:
            self.tic_tac_toe_board[row][col] = self.current_player
            button.setText(self.current_player)
            button.setEnabled(False)
            if self.check_winner(row, col):
                self.games_won += 1
                if self.games_won >= 3:
                    self.show_congratulations()
                else:
                    self.reset_tic_tac_toe_board()
            else:
                self.current_player = "X" if self.current_player == "O" else "O"

    def check_winner(self, row, col):
        # Check if the current player has won the game
        player = self.current_player
        # Check row
        if all(self.tic_tac_toe_board[row][c] == player for c in range(3)):
            return True
        # Check column
        if all(self.tic_tac_toe_board[r][col] == player for r in range(3)):
            return True
        # Check diagonals
        if row == col and all(self.tic_tac_toe_board[i][i] == player for i in range(3)):
            return True
        if row + col == 2 and all(self.tic_tac_toe_board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def reset_tic_tac_toe_board(self):
        # Reset the Tic-Tac-Toe board for a new game
        for row in range(3):
            for col in range(3):
                self.tic_tac_toe_board[row][col] = None
                button = self.tic_tac_toe_grid.itemAtPosition(row, col).widget()
                button.setText("")
                button.setEnabled(True)
        self.current_player = "X"

    def hide_tic_tac_toe_board(self):
        for row in range(3):
            for col in range(3):
                button = self.tic_tac_toe_grid.itemAtPosition(row, col).widget()
                button.hide()

    def show_tic_tac_toe_board(self):
        for row in range(3):
            for col in range(3):
                button = self.tic_tac_toe_grid.itemAtPosition(row, col).widget()
                button.show()

    def solve_puzzle(self):
        user_answer = self.answer_entry.text().strip().lower()
        correct_answer = rooms[self.current_room]["answer"]
        if user_answer == correct_answer:
            self.current_room = rooms[self.current_room]["next_room"]
            if self.current_room == "exit":
                self.in_tic_tac_toe = True  # Enable Tic-Tac-Toe after escaping
                self.show_tic_tac_toe_board()
                self.reset_tic_tac_toe_board()
                self.attempts_remaining = 5
            else:
                self.attempts_remaining = 5
            self.show_room()
        else:
            self.attempts_remaining -= 1
            if self.attempts_remaining == 0:
                self.show_error("Oops! That's not the correct answer. You've run out of attempts.")
                self.current_room = "start"
                self.attempts_remaining = 5
            else:
                self.show_error(f"Oops! That's not the correct answer. {self.attempts_remaining} attempts remaining")

    def show_congratulations(self):
        QMessageBox.information(self, "Congratulations", "You've escaped from The Secret Chamber!")

    def show_error(self, message):
        QMessageBox.critical(self, "Incorrect", message)

if __name__ == '__main__':
    app = QApplication([])

    rooms = {
        "start": {
            "description": "You are in the starting room of The Secret Chamber. There is a locked door ahead.",
            "puzzle": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
            "answer": "an echo",
            "next_room": "room_1",
        },
        "room_1": {
            "description": "You enter the first room. Another locked door stands in your way.",
            "puzzle": "You see a boat filled with people. It has not sunk, but when you look again, you don’t see a single person on the boat. Why?",
            "answer": "all the people were married",
            "next_room": "room_2",
        },
        "room_2": {
            "description": "You are in the second room. A mysterious puzzle awaits.",
            "puzzle": "I am not alive, but I can grow. I don't have lungs, but I need air. I don't have a mouth, but water kills me. What am I?",
            "answer": "fire",
            "next_room": "room_3",
        },
        "room_3": {
            "description": "You enter the third room. Can you solve this one?",
            "puzzle": "The more you take, the more you leave behind. What am I?",
            "answer": "footsteps",
            "next_room": "room_4",
        },
        "room_4": {
            "description": "You are in the fourth room. The final riddle stands between you and the exit of The Secret Chamber.",
            "puzzle": "I'm tall when I'm young and short when I'm old. What am I?",
            "answer": "a candle",
            "next_room": "exit",
        },
        "exit": {
            "description": "Congratulations! You have successfully escaped from The Secret Chamber!",
        },
    }

    ex = TheSecretChamber()
    ex.show()
    sys.exit(app.exec_())