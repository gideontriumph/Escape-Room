import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSpacerItem
)
from PyQt5.QtGui import QFont

class TheSecretChamber(QWidget):
    def __init__(self):
        super().__init__()
        self.current_room = "start"
        self.attempts_remaining = 5
        self.initUI()

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

        # Add spacing to separate the puzzle elements
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
        else:
            self.puzzle_label.clear()
            self.answer_entry.hide()
            self.solve_button.hide()

    def solve_puzzle(self):
        user_answer = self.answer_entry.text().strip().lower()
        correct_answer = rooms[self.current_room]["answer"]

        if user_answer == correct_answer:
            self.current_room = rooms[self.current_room]["next_room"]
            if self.current_room == "exit":
                self.attempts_remaining = 5  # Reset attempts for a new game
            self.show_room()
        else:
            self.attempts_remaining -= 1
            if self.attempts_remaining == 0:
                self.show_error("Oops! That's not the correct answer. You've run out of attempts.")
                self.current_room = "start"
                self.attempts_remaining = 5
            else:
                self.show_error(f"Oops! That's not the correct answer. {self.attempts_remaining} attempts remaining")

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
    