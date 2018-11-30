import unittest

import re

from backend.utils.id_generator import IdGenerator


class IdGeneratorTestCase(unittest.TestCase):
    def test_generate_id(self):
        generator = IdGenerator()
        received_id = generator.next_id()
        self.assertIsNotNone(received_id)
        self.assertTrue(re.match(r'\w+', str(received_id)))
