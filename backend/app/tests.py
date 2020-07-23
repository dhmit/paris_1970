"""
Tests for the main app.
"""

from django.test import TestCase


class MainTests(TestCase):
    """
    Backend TestCase
    """
    # def setUp(self):
    #     super().setUp()
    #     do any setup here

    def test_sample(self):
        """
        Remove me once we have real tests here.
        """
        two = 2
        another_two = 2
        self.assertEqual(two + another_two, 4)
