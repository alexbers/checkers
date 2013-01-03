#!/usr/bin/env python
# author: Alexander Bersenev (bay)
# mail: bay@hackerdom.ru

import unittest
from checkers import Game


class calc_turns_tests(unittest.TestCase):
    def test_init_possible_moves(self):
        g = Game()
        g.turn = "B"
        moves = g.get_possible_moves()
        valid_moves = [
            [(3, 0), (4, 1)], [(3, 2), (4, 1)], [(3, 2), (4, 3)],
            [(3, 4), (4, 3)], [(3, 4), (4, 5)], [(3, 6), (4, 5)],
            [(3, 6), (4, 7)], [(3, 8), (4, 7)], [(3, 8), (4, 9)]]

        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

        g = Game()
        g.turn = "W"
        moves = g.get_possible_moves()
        valid_moves = [
            [(6, 1), (5, 2)], [(6, 1), (5, 0)], [(6, 3), (5, 4)],
            [(6, 3), (5, 2)], [(6, 5), (5, 6)], [(6, 5), (5, 4)],
            [(6, 7), (5, 8)], [(6, 7), (5, 6)], [(6, 9), (5, 8)]]

        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

    def test_king_moves(self):
        g = Game()
        g.board = [
            list(' . . . . .'),  # 0
            list('. . . . . '),  # 1
            list(' . . . . .'),  # 2
            list('. . . b . '),  # 3
            list(' . . b . .'),  # 4
            list('. . . . . '),  # 5
            list(' . W . . .'),  # 6
            list('. . . . . '),  # 7
            list(' b . . . .'),  # 8
            list('b . . b b ')   # 9
        ]
        moves = g.get_possible_moves()
        valid_moves = [
            [(6, 3), (7, 2)], [(6, 3), (5, 4)], [(6, 3), (5, 2)],
            [(6, 3), (4, 1)], [(6, 3), (3, 0)], [(6, 3), (7, 4)],
            [(6, 3), (8, 5)]]
        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

    def test_simple_capture(self):
        g = Game()
        g.board = [
            list(" b b b b b"),
            list('b b b b b '),
            list(' b b b b b'),
            list('b . b b b '),
            list(' . . . . .'),
            list('. b . . . '),
            list(' w w w w w'),
            list('w w w w w '),
            list(' w w w w w'),
            list('w w w w w ')
        ]
        moves = g.get_possible_moves()
        valid_moves = [[(6, 1), (5, 2), (4, 3)], [(6, 3), (5, 2), (4, 1)]]

        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

    def test_multi_capture(self):
        g = Game()
        g.board = [
            list(' b b b b b'),  # 0
            list('b b b . b '),  # 1
            list(' b b b . .'),  # 2
            list('b . . b b '),  # 3
            list(' . b b . .'),  # 4
            list('. . . b . '),  # 5
            list(' b w w w w'),  # 6
            list('w w w w w '),  # 7
            list(' w w w w w'),  # 8
            list('w w w w w ')   # 9
        ]
        moves = g.get_possible_moves()
        valid_moves = [[(7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5),
                        (1, 6)]]

        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

    def test_advanced_capture(self):
        g = Game()
        g.board = [
            list(' b b b b b'),  # 0
            list('b b b b b '),  # 1
            list(' b b b . .'),  # 2
            list('b . . b b '),  # 3
            list(' . b . . .'),  # 4
            list('. . . b b '),  # 5
            list(' b b w w .'),  # 6
            list('w w . w w '),  # 7
            list(' w w w w w'),  # 8
            list('w w w w w ')   # 9
        ]
        moves = g.get_possible_moves()
        valid_moves = [[(6, 7), (5, 8), (4, 9), (3, 8),
            (2, 7), (3, 6), (4, 5), (5, 6), (6, 7)],
            [(6, 7), (5, 6), (4, 5), (3, 6), (2, 7),
             (3, 8), (4, 9), (5, 8), (6, 7)]]

        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

    def test_more_advanced_capture(self):
        g = Game()
        g.board = [
            list(' . . b . b'),  # 0
            list('. b b b b '),  # 1
            list(' w b . . .'),  # 2
            list('. . . . . '),  # 3
            list(' . . . b .'),  # 4
            list('. . . . . '),  # 5
            list(' . . w w .'),  # 6
            list('w w . w w '),  # 7
            list(' w w w w w'),  # 8
            list('w w w w w ')   # 9
        ]
        moves = g.get_possible_moves()
        valid_moves = [[(2, 1), (1, 2), (0, 3), (1, 4),
            (2, 5), (1, 6), (0, 7), (1, 8), (2, 9)]]

        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

    def test_king_capture(self):
        g = Game()
        g.board = [
            list(' . . . . .'),  # 0
            list('. . . . . '),  # 1
            list(' . . . b .'),  # 2
            list('. . . . . '),  # 3
            list(' . . b . .'),  # 4
            list('. . . . . '),  # 5
            list(' . W . . .'),  # 6
            list('. . . . . '),  # 7
            list(' b . . . .'),  # 8
            list('b . . b b ')   # 9
        ]
        moves = g.get_possible_moves()
        valid_moves = [
            [(6, 3), (4, 5), (3, 6), (2, 7), (1, 8)],
            [(6, 3), (4, 5), (3, 6), (2, 7), (0, 9)]
        ]
        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)

    def test_king_multi_capture(self):
        g = Game()
        g.board = [
            list(' . . . . .'),  # 0
            list('. . . . . '),  # 1
            list(' . . . b .'),  # 2
            list('. . . . . '),  # 3
            list(' . . b . .'),  # 4
            list('. . . . . '),  # 5
            list(' . W . . .'),  # 6
            list('. . b b . '),  # 7
            list(' b . . . .'),  # 8
            list('b . . b b ')   # 9
        ]
        moves = g.get_possible_moves()
        valid_moves = [
            [(6, 3), (7, 4), (8, 5), (7, 6), (6, 7), (4, 5), (3, 4)],
            [(6, 3), (7, 4), (8, 5), (7, 6), (6, 7), (4, 5), (2, 3)],
            [(6, 3), (7, 4), (8, 5), (7, 6), (6, 7), (4, 5), (1, 2)],
            [(6, 3), (7, 4), (8, 5), (7, 6), (6, 7), (4, 5), (0, 1)],
            [(6, 3), (7, 4), (8, 5), (7, 6), (4, 9), (2, 7), (1, 6)],
            [(6, 3), (7, 4), (8, 5), (7, 6), (4, 9), (2, 7), (0, 5)]]
        self.assertEqual(len(moves), len(valid_moves))
        for move in moves:
            self.assertTrue(move in valid_moves)


class make_turns_tests(unittest.TestCase):
    def test_simple_move(self):
        g = Game()
        board = [
            list(' b b b b b'),
            list('b b b b b '),
            list(' b b b b b'),
            list('b b b b b '),
            list(' . . . . .'),
            list('. . . . . '),
            list(' w w w w w'),
            list('w w w w w '),
            list(' w w w w w'),
            list('w w w w w ')
        ]
        newboard = g.get_board_after_move(board, [(6, 1), (5, 2)])
        validboard = [
            list(' b b b b b'),
            list('b b b b b '),
            list(' b b b b b'),
            list('b b b b b '),
            list(' . . . . .'),
            list('. w . . . '),
            list(' . w w w w'),
            list('w w w w w '),
            list(' w w w w w'),
            list('w w w w w ')
        ]
        self.assertEqual(newboard, validboard)

    def test_simple_attack(self):
        g = Game()
        board = [
            list(' b b b b b'),
            list('b b b b b '),
            list(' b b b b b'),
            list('b b . b b '),
            list(' . . . . .'),
            list('. . b . . '),
            list(' w w w w w'),
            list('w w w w w '),
            list(' w w w w w'),
            list('w w w w w ')
        ]
        newboard = g.get_board_after_move(board, [(6, 3), (5, 4), (4, 5)])
        validboard = [
            list(' b b b b b'),
            list('b b b b b '),
            list(' b b b b b'),
            list('b b . b b '),
            list(' . . w . .'),
            list('. . . . . '),
            list(' w . w w w'),
            list('w w w w w '),
            list(' w w w w w'),
            list('w w w w w ')
        ]
        self.assertEqual(newboard, validboard)

    def test_few_moves(self):
        g = Game()
        g.board = [
            list(' b b b b b'),  # 0
            list('b b b b b '),  # 1
            list(' b b b b b'),  # 2
            list('b b b b b '),  # 3
            list(' . . . . .'),  # 4
            list('. . . . . '),  # 5
            list(' w w w w w'),  # 6
            list('w w w w w '),  # 7
            list(' w w w w w'),  # 8
            list('w w w w w ')   # 9
        ]

        self.assertFalse(g.makemove([(6, 2), (5, 0)]))  # impossible move
        self.assertTrue(g.makemove([(6, 1), (5, 0)]))   # valid move
        self.assertFalse(g.makemove([(6, 1), (5, 0)]))  # invalid, its
                                                        # opponent turn
        self.assertTrue(g.makemove([(3, 0), (4, 1)]))   # valid move
        self.assertTrue(g.makemove([(6, 3), (5, 2)]))   # valid move
        self.assertFalse(g.makemove([(2, 1), (3, 0)]))     # invalid, must kill
        self.assertTrue(g.makemove([(4, 1), (5, 2), (6, 3)]))    # killing
        self.assertTrue(g.makemove([(7, 2), (6, 3), (5, 4)]))    # killing
        self.assertTrue(g.makemove([(2, 1), (3, 0)]))    # valid now
        self.assertTrue(g.makemove([(7, 4), (6, 3)]))    # valid
        self.assertTrue(g.makemove([(3, 4), (4, 3)]))    # valid
        self.assertTrue(g.makemove([(6, 9), (5, 8)]))    # valid
        self.assertTrue(g.makemove([(3, 0), (4, 1)]))    # valid
        self.assertTrue(g.makemove([(6, 5), (5, 6)]))    # valid
        self.assertFalse(g.makemove([(4, 3), (5, 4), (6, 5), (5, 6), (4, 7)]))
        self.assertFalse(g.makemove([(4, 3), (5, 4), (6, 5), (5, 6), (4, 7),
                                     (5, 8)]))
        self.assertTrue(g.makemove([(4, 3), (5, 4), (6, 5), (5, 6), (4, 7),
                                    (5, 8), (6, 9)]))
        validboard = [
            list(' b b b b b'),  # 0
            list('b b b b b '),  # 1
            list(' . b b b b'),  # 2
            list('. b . b b '),  # 3
            list(' b . . . .'),  # 4
            list('w . . . . '),  # 5
            list(' . w . w b'),  # 6
            list('w . . w w '),  # 7
            list(' w w w w w'),  # 8
            list('w w w w w ')   # 9
        ]
        self.assertEqual(g.board, validboard)

    def test_kings_becoming(self):
        g = Game()
        g.board = [
            list(' . . . . .'),  # 0
            list('. w . . . '),  # 1
            list(' . . . . .'),  # 2
            list('. . . . . '),  # 3
            list(' . . . . .'),  # 4
            list('. . . . . '),  # 5
            list(' . . . . .'),  # 6
            list('. . . . . '),  # 7
            list(' b . . . .'),  # 8
            list('. . . . . ')   # 9
        ]
        self.assertTrue(g.makemove([(1, 2), (0, 1)]))    # valid
        self.assertTrue(g.makemove([(8, 1), (9, 0)]))    # valid
        validboard = [
            list(' W . . . .'),  # 0
            list('. . . . . '),  # 1
            list(' . . . . .'),  # 2
            list('. . . . . '),  # 3
            list(' . . . . .'),  # 4
            list('. . . . . '),  # 5
            list(' . . . . .'),  # 6
            list('. . . . . '),  # 7
            list(' . . . . .'),  # 8
            list('B . . . . ')   # 9
        ]
        self.assertEqual(g.board, validboard)

unittest.main()
#suite = unittest.TestLoader().loadTestsFromTestCase(calc_turns_tests)
#unittest.TextTestRunner(verbosity=0).run(suite)
