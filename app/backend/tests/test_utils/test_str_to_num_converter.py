import unittest

from utils.to_num_converter import ToNum


class TestToHashStorage(unittest.TestCase):
    def test_to_int(self):
        converter = ToNum()
        str_num = '1'
        int_num = converter.to_int(str_num)
        self.assertEqual(int_num, 1)

        str_num = '0'
        int_num = converter.to_int(str_num)
        self.assertEqual(int_num, 0)

        str_num = '01'
        int_num = converter.to_int(str_num)
        self.assertEqual(int_num, 1)

        str_num = '001'
        int_num = converter.to_int(str_num)
        self.assertEqual(int_num, 1)

    def test_to_float(self):
        converter = ToNum()
        str_num = '1'
        int_num = converter.to_float(str_num)
        self.assertEqual(int_num, 1.)

        str_num = '0'
        int_num = converter.to_float(str_num)
        self.assertEqual(int_num, 0.)

        str_num = '0.1'
        int_num = converter.to_float(str_num)
        self.assertEqual(int_num, .1)

        str_num = '00.01'
        int_num = converter.to_float(str_num)
        self.assertEqual(int_num, .01)

    def test_to_num(self):
        converter = ToNum()
        str_num = '1'
        int_num = converter.to_num(str_num)
        self.assertEqual(int_num, 1)

        str_num = '0'
        int_num = converter.to_num(str_num)
        self.assertEqual(int_num, 0)

        str_num = '0.1'
        int_num = converter.to_num(str_num)
        self.assertEqual(int_num, .1)

        str_num = '00.01'
        int_num = converter.to_num(str_num)
        self.assertEqual(int_num, .01)

    def test_to_num_with_none(self):
        converter = ToNum()
        str_num = None
        int_num = converter.to_num(str_num)
        self.assertEqual(int_num, None)
