from django.test import TestCase
from django.urls import reverse

from ..models import *

class NetworkViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_networks = 13

        for network_id in range(number_of_networks):
            Network.objects.create(
                network_name=f'City {network_id}'
                #date_created=h,
                #date_updated=h
            )

class IntersectionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_networks = 13
        for network_id in range(number_of_networks):
            Network.objects.create(
                network_name=f'City {network_id}'
                #date_created=h,
                #date_updated=h
            )

class AllNetworksViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_networks = 13

        for network_id in range(number_of_networks):
            Network.objects.create(
                network_name=f'City {network_id}'
                #date_created=h,
                #date_updated=h
            )