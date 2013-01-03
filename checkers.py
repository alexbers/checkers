#!/usr/bin/env python
# coding: utf-8
#
# Copyright © 2012 Alexander Bersenev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ‘Software’), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import copy
import random
from PyQt4 import QtCore, QtGui


class Game:
    def __init__(self):
        self.board = [
            list(' b b b b b'),
            list('b b b b b '),
            list(' b b b b b'),
            list('b b b b b '),
            list(' . . . . .'),
            list('. . . . . '),
            list(' w w w w w'),
            list('w w w w w '),
            list(' w w w w w'),
            list('w w w w w '),
        ]
        self.turn = 'W'

    def __repr__(self):
        text = 'Current move: %s\n' % ({'B': 'black', 'W': 'white'}[self.turn])
        text += "\n".join([" ".join(boardline) for boardline in self.board])
        return text

    def calc_attack(self, y, x, board, prev_moves):
        assert 0 <= y < 10 and 0 <= x < 10
        assert board[y][x].upper() == self.turn

        is_king = board[y][x].isupper()
        enemy = {'B': 'W', 'W': 'B'}[self.turn]

        moves = []

        directions = (1, -1), (1, 1), (-1, 1), (-1, -1)
        for dir_y, dir_x in directions:
            if is_king:
                dir_muls = range(1, 11)
            else:
                dir_muls = (1, 2)

            victim_y, victim_x = None, None
            for dir_mul in dir_muls:
                try_y, try_x = y + dir_y * dir_mul, x + dir_x * dir_mul

                if not(0 <= try_y < 10 and 0 <= try_x < 10):
                    break

                if board[try_y][try_x].upper() == self.turn:
                    break

                if victim_y is None and victim_x is None:
                    if board[try_y][try_x].upper() == enemy:
                        victim_y, victim_x = try_y, try_x
                else:
                    if not (board[try_y][try_x] == '.'):
                        break

                    new_prev_moves = prev_moves + [
                        (victim_y, victim_x), (try_y, try_x)]
                    new_board = self.get_board_after_move(board,
                        [(y, x), (victim_y, victim_x), (try_y, try_x)])
                    new_moves = self.calc_attack(try_y, try_x,
                        new_board, new_prev_moves)

                    moves.append(new_prev_moves)
                    moves += new_moves

        return moves

    def get_moves_for_piece(self, y, x):
        moves = []
        piece = self.board[y][x]
        is_king = piece.isupper()

        # non-attack moves
        if not is_king:
            if self.turn == "B":
                directions = (1, -1), (1, 1)
            if self.turn == "W":
                directions = (-1, 1), (-1, -1)

            for delta_y, delta_x in directions:
                if not (0 <= x + delta_x < 10 and 0 <= y + delta_y < 10):
                    continue
                if self.board[y + delta_y][x + delta_x] == '.':
                    moves.append([(y, x), (y + delta_y, x + delta_x)])
        else:
            directions = (1, -1), (1, 1), (-1, 1), (-1, -1)
            for dir_y, dir_x in directions:
                dir_muls = range(1, 10)
                for dir_mul in dir_muls:
                    try_y, try_x = y + dir_y * dir_mul, x + dir_x * dir_mul
                    if not (0 <= try_y < 10 and 0 <= try_x < 10):
                        break
                    if not (self.board[try_y][try_x] == '.'):
                        break
                    moves.append([(y, x), (try_y, try_x)])

        # attack moves
        moves += self.calc_attack(y, x, self.board, [(y, x)])

        return moves

    def get_possible_moves(self):
        possible_moves = []

        for y in range(10):
            for x in range(10):
                piece = self.board[y][x]

                if piece.upper() == self.turn:
                    possible_moves += self.get_moves_for_piece(y, x)

        if not possible_moves:
            # todo: check for game ending
            return []
        # get only longest moves
        maxlen = len(max(possible_moves, key=len))
        possible_moves = [move for move in possible_moves
                               if len(move) == maxlen]

        return possible_moves

    def get_board_after_move(self, board, move):
        assert len(move) > 0

        board_after_move = copy.deepcopy(board)
        y_from, x_from = move[0]
        y_to, x_to = move[-1]
        player = board[y_from][x_from].upper()
        enemy = {'B': 'W', 'W': 'B'}[player]

        # move checker for first pos to last pos
        board_after_move[y_from][x_from], board_after_move[y_to][x_to] = (
            board[y_to][x_to], board[y_from][x_from])

        for num, move_component in enumerate(move):
            y, x = move_component
            # kill an enemy
            if board[y][x].upper() == enemy:
                board_after_move[y][x] = '.'

        return board_after_move

    def make_kings(self):
        for x in range(10):
            if self.board[9][x] == "b":
                self.board[9][x] = "B"
            if self.board[0][x] == "w":
                self.board[0][x] = "W"

    def makemove(self, move):
        if move not in self.get_possible_moves():
            return False
        self.board = self.get_board_after_move(self.board, move)
        self.make_kings()
        self.turn = {'B': 'W', 'W': 'B'}[self.turn]
        return True


# === QT GUI ===
class MainWidget(QtGui.QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.board = Board(self)
        self.board.move(10, 10)
        self.board.resize(400, 400)

        self.initUI()

    def initUI(self):
        self.resize(420, 460)
        self.center()
        self.setWindowTitle('Checkers by BAY')
        self.setWindowIcon(QtGui.QIcon('black.bmp'))

        cb_black = QtGui.QCheckBox('Black is computer', self)
        cb_black.setGeometry(10, 420, 200, 20)
        cb_black.stateChanged.connect(self.black_check_box_toggled)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QtGui.QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    def black_check_box_toggled(self, state):
        self.board.is_black_computer = (state == QtCore.Qt.Checked)


class Board(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.is_black_computer = False

        self.game = Game()

        self.checker_to_pixmap = {
            "w": QtGui.QPixmap("white.bmp"),
            "b": QtGui.QPixmap("black.bmp"),
            "W": QtGui.QPixmap("whiteq.bmp"),
            "B": QtGui.QPixmap("blackq.bmp")
        }

        self.board_changed()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        for y in range(10):
            for x in range(10):
                left, top = x * 40, y * 40
                cellstate = self.game.board[y][x]
                if cellstate == " ":
                    painter.fillRect(left, top, 40, 40,
                                     QtGui.QColor("lightgray"))
                else:
                    painter.fillRect(left, top, 40, 40,
                                     QtGui.QColor(0xc2, 0xc2, 0xc2))

                if cellstate in self.checker_to_pixmap:
                    painter.drawPixmap(left + 2, top + 1,
                        self.checker_to_pixmap[cellstate])

                if (x, y) in self.suggestedcells:
                    painter.setPen(QtGui.QColor("yellow"))
                    painter.drawRect(left, top, 39, 39)
                    painter.drawRect(left + 1, top + 1, 37, 37)
                if (y, x) in self.myturn:
                    painter.setPen(QtGui.QColor("green"))
                    painter.drawRect(left, top, 39, 39)
                    painter.drawRect(left + 1, top + 1, 37, 37)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # convert local x and y to the board ones
            x, y = event.x() // 40, event.y() // 40
            if (x, y) not in self.suggestedcells:
                # todo: add animation here
                self.myturn = []
            else:
                self.myturn.append((y, x))
                # check if turn is complete
                if self.game.makemove(self.myturn):
                    self.board_changed()
                    if self.game.turn == "B" and self.is_black_computer:
                        possible_moves = self.game.get_possible_moves()
                        if possible_moves:
                            self.game.makemove(random.choice(possible_moves))
                            self.board_changed()
            self.update_suggested()
            self.repaint()

    def update_suggested(self):
        self.suggestedcells = set([])
        for move in self.possible_moves:
            if move[0:len(self.myturn)] == self.myturn:
                y, x = move[len(self.myturn)]
                self.suggestedcells.add((x, y))

        # a little hack here: auto making a click on enemy checker
        if len(self.suggestedcells) == 1:
            for x, y in self.suggestedcells:
                if(self.game.board[y][x].upper() ==
                   {'B': 'W', 'W': 'B'}[self.game.turn]):
                    self.myturn.append((y, x))
                    self.update_suggested()

    def board_changed(self):
        self.myturn = []
        self.possible_moves = self.game.get_possible_moves()
        if not self.possible_moves:
            if self.game.turn == "W":
                QtGui.QMessageBox.about(self, "Game over", "Black wins")
            else:
                QtGui.QMessageBox.about(self, "Game over", "White wins")
        self.suggestedcells = set([])
        self.update_suggested()

if __name__ == "__main__":
    app = QtGui.QApplication([])
    gui = MainWidget()
    app.exec_()
