import unittest

import re

from utils.id_generator import IdGenerator


class IdGeneratorTestCase(unittest.TestCase):
    def test_generate_id(self):
        generator = IdGenerator()
        self.assertIsNotNone(generator.next_id())
        self.assertTrue(re.match(r'\w', generator.next_id()))

if __name__ == '__main__':
    unittest.main()
