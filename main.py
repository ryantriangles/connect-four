#!/usr/bin/env python3
"""
A quick and simple terminal-based implementation of Connect Four for
two players sharing a keyboard.

The board is represented as a two-dimensional array in which a 0
represents an empty slot and a 1 or a 2 represents a player token.
"""
from typing import Generator, Tuple, List

Position = Tuple[int, int]
PositionGenerator = Generator[Position, None, None]


class Board:
    def __init__(self):
        self.board: List[List[int]] = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
        self.game_over = False
        self.current_player = 1
        self.COLUMN_LENGTH = len(self.board)
        self.ROW_LENGTH = len(self.board[0])
        self.MAX_COLUMN = self.ROW_LENGTH - 1
        self.CHECKS = [self.check_horizontal_win,
                       self.check_vertical_win,
                       self.check_northwest_diagonal_win,
                       self.check_northeast_diagonal_win]

    def swap_players(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def check_horizontal_win(self) -> bool:
        score = 1
        # Check right
        stop = min(self.last_placed_x + 4, self.ROW_LENGTH)
        for x_ in range(self.last_placed_x + 1, stop):
            if self.board[self.last_placed_y][x_] != self.current_player:
                break
            score += 1
        # Check left
        stop = max(self.last_placed_x - 4, -1)
        for x_ in range(self.last_placed_x - 1, stop, -1):
            if self.board[self.last_placed_y][x_] != self.current_player:
                break
            score += 1
        return score > 3

    def check_vertical_win(self) -> bool:
        score = 1
        stop = min(self.last_placed_y + 4, self.COLUMN_LENGTH)
        for y_ in range(self.last_placed_y + 1, stop):
            if self.board[y_][self.last_placed_x] != self.current_player:
                break
            score += 1
        return score > 3

    def check_northwest_diagonal_win(self) -> bool:
        score = 1
        for (y_, x_) in self.__northwest_diagonals():
            if self.board[y_][x_] != self.current_player:
                break
            score += 1
        for (y_, x_) in self.__southeast_diagonals():
            if self.board[y_][x_] != self.current_player:
                break
            score += 1
        return score > 3

    def check_northeast_diagonal_win(self) -> bool:
        score = 1
        for (y_, x_) in self.__northeast_diagonals():
            if self.board[y_][x_] != self.current_player:
                break
            score += 1
        for (y_, x_) in self.__southwest_diagonals():
            if self.board[y_][x_] != self.current_player:
                break
            score += 1
        return score > 3

    def check_win(self) -> bool:
        for check in self.CHECKS:
            if check():
                self.game_over = True
                return True
        return False

    def drop_token(self, column: int):
        for row in range(7, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.last_placed_x = column
                self.last_placed_y = row
                return

    def print(self, clear_terminal=True):
        if clear_terminal:
            print(chr(27) + "[2J")
        print(f"Current player: {self.current_player}\n")
        for n in range(self.ROW_LENGTH):  # Header
            print(n, end="  ")
        print("\n-----------------------")
        for row in self.board:
            for cell in row:
                print(cell, end="  ")
            print()
        print("\n")

    def prompt(self) -> int:
        """Prompt the user to select a column."""
        while True:
            selected_column = input("Select a column: ")
            try:
                selected_column = int(selected_column)
            except ValueError:
                print(f"Please select a column from 0 to {self.MAX_COLUMN}.")
                continue
            if selected_column >= self.ROW_LENGTH or selected_column < 0:
                print(f"Please select a column from 0 to {self.MAX_COLUMN}.")
            elif not self.__column_has_space(selected_column):
                print("Column is already full.")
            else:
                return selected_column

    def __column_has_space(self, column: int) -> bool:
        """Check if a column has an available space in it."""
        for _ in range(self.ROW_LENGTH):
            if self.board[0][column] == 0:
                return True
        return False

    def __northeast_diagonals(self) -> PositionGenerator:
        y = self.last_placed_y
        x = self.last_placed_x
        while (x := x + 1) < self.ROW_LENGTH and (y := y - 1) >= 0:
            yield (y, x)

    def __southeast_diagonals(self) -> PositionGenerator:
        y = self.last_placed_y
        x = self.last_placed_x
        while (x := x + 1) < self.ROW_LENGTH and \
              (y := y + 1) < self.COLUMN_LENGTH:
            yield (y, x)

    def __southwest_diagonals(self) -> PositionGenerator:
        y = self.last_placed_y
        x = self.last_placed_x
        while (x := x - 1) >= 0 and (y := y + 1) < self.COLUMN_LENGTH:
            yield (y, x)

    def __northwest_diagonals(self) -> PositionGenerator:
        y = self.last_placed_y
        x = self.last_placed_x
        while (x := x - 1) >= 0 and (y := y - 1) >= 0:
            yield (y, x)


if __name__ == "__main__":
    board = Board()
    while not board.game_over:
        board.print()
        selected_column = board.prompt()
        board.drop_token(selected_column)
        if board.check_win():
            board.print()
            print(f"Player {board.current_player} wins!")
        board.swap_players()
