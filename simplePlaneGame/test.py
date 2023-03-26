import main

import unittest


class Testing(unittest.TestCase):
    def test_string(self):
        a = 'some'
        b = 'some'
        self.assertEqual(a, b)

    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)

    def test_get_score(self):
        score = main.get_score()
        self.assertEqual(score, 42)

if __name__ == '__main__':
    unittest.main()