from django.test import TestCase
from ..models import *
from ..forms import *

class TestRoadForm(TestCase):
    def test_same_intersection_in_and_out(self):
        """Animals that can speak are correctly identified"""
        