import unittest

import sval


class TestSevenCardEval(unittest.TestCase):
    deuces = sval.encode_cards("2c2h2d2s")
    threes = sval.encode_cards("3s3h3d3c")
    tens = sval.encode_cards("ThTdTsTc")

    def test_binary_encoding(self):
        self.assertTrue(self.deuces == 15)
        self.assertTrue(self.threes == 240)
        self.assertTrue(self.tens == 64424509440)

    def test_cards_to_string(self):
        self.assertTrue(sval.cards_to_string(self.deuces) == "2s2h2d2c")
        self.assertTrue(sval.cards_to_string(self.threes) == "3s3h3d3c")
        self.assertTrue(sval.cards_to_string(self.tens) == "TsThTdTc")

    def test_binary_artithmetic(self):
        self.assertTrue((self.deuces | self.threes | self.tens)
                        == self.deuces + self.threes + self.tens)
        self.assertTrue((self.deuces & self.threes & self.tens) == 0)
        self.assertTrue(sval.encode_cards("2s2h") & sval.encode_cards("2hAs")
                        == sval.encode_cards("2h"))
        self.assertTrue(self.tens & self.tens == self.tens)

    def test_rank_lookup(self):
        hand_1 = sval.encode_cards("As5h")
        hand_2 = sval.encode_cards("Ad2d")
        board_1 = sval.encode_cards("Ah3d5hTsKd")
        value_1 = sval.calculate_index(hand_1 | board_1)
        value_2 = sval.calculate_index(hand_2 | board_1)
        self.assertTrue(value_1 == 189954)
        self.assertTrue(value_2 == 189955)


if __name__ == '__main__':
    unittest.main()
