import unittest
from dq import compiled

class CompileTest(unittest.TestCase):
    def test_compiled(self):
        c = compiled('[0]')
        self.assertEqual(c([1,2,3,4,5]), 1)
        self.assertEqual(c([5,4,3,2,1]), 5)
