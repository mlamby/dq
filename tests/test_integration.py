import unittest
from dq import query

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.data = {
            'one': 1,
            'two': [1,2,3,4,5],
            'three': [
                {'name': 'john'},
                {'name': 'mary'},
                {'one': 'frank'}
            ]
        }

        self.array_data = [10,11,12,13]

    def query(self, v, result, data):
        self.assertEqual(query(v, data), result)

    def test_dict_key(self):
        self.query('.one', 1, self.data)
        self.query('.two', [1,2,3,4,5], self.data)

    def test_array_index(self):
        self.query('[0]', 10, self.array_data)
        self.query('[-2]', 12, self.array_data)
        self.query('.two[1]', 2, self.data)
        self.query('.three[1].name', 'mary', self.data)

    def test_star_index(self):
        self.query('[*]', [10,11,12,13], self.array_data)
        self.query('.two[*]', [1,2,3,4,5], self.data)
        self.query(
            '.three[*].name', ['john', 'mary'], self.data)

    def test_slice_array(self):
        self.query('[1:-1]', [11,12], self.array_data)
        self.query('.two[1:-2]', [2,3], self.data)
        self.query('.two[:4:2]', [1,3], self.data)

    def test_find_key(self):
        self.query('..name', ['john', 'mary'], self.data)
        self.query('..one', [1, 'frank'], self.data)


