#!/usr/bin/env python3
"""Pytest suite."""
import main


def test_horizontal_win():
    board = main.Board()
    board.drop_token(0)
    board.drop_token(1)
    board.drop_token(2)
    board.drop_token(3)
    board.print(clear_terminal=False)
    assert board.check_horizontal_win()


def test_vertical_win():
    board = main.Board()
    board.drop_token(0)
    board.drop_token(0)
    board.drop_token(0)
    assert not board.check_vertical_win()
    board.drop_token(0)
    assert board.check_vertical_win()


def test_northwest_vertical_win():
    board = main.Board()
    board.drop_token(0)
    board.drop_token(0)
    board.drop_token(0)
    board.drop_token(0)
    board.drop_token(1)
    board.drop_token(1)
    board.drop_token(1)
    board.drop_token(2)
    board.drop_token(2)
    assert not board.check_northwest_diagonal_win()
    board.drop_token(3)
    assert board.check_northwest_diagonal_win()


def test_northeast_vertical_win():
    board = main.Board()
    board.drop_token(0)
    board.drop_token(1)
    board.drop_token(1)
    board.drop_token(2)
    board.drop_token(2)
    board.drop_token(2)
    board.drop_token(3)
    board.drop_token(3)
    board.drop_token(3)
    assert not board.check_northeast_diagonal_win()
    board.drop_token(3)
    assert board.check_northeast_diagonal_win()
