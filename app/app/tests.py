from django.test import TestCase

from .calc import add, subtract

class CalcTest(TestCase):

    def test_add_number(self):
        """test that tests two number are added together"""
        self.assertEqual(add(3, 8), 11)


    def test_subtract_number(self):
        """test subtracting one item from another"""
        self.assertEqual(subtract(5, 11), 6)