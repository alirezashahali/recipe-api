from django.test import TestCase

from .calc import add

class CalcTest(TestCase):

    def test_add_number(self):
        """test that tests two number are added together"""
        self.assertEqual(add(3, 8), 11)