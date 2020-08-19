from django.test import TestCase
from django.urls import reverse

from ..models import *

class NetworkViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_networks = 13

        for network_id in range(number_of_networks):
            Network.objects.create( network_name=f'City {network_id}' )

    def test_all_networks_view_url_exists_at_desired_location(self):
        response = self.client.get('/network/')
        self.assertEqual(response.status_code, 200)
           
    def test_all_networks_view_url_accessible_by_name(self):
        response = self.client.get(reverse('all_networks'))
        self.assertEqual(response.status_code, 200)
        
    def test_all_networks_view_uses_correct_template(self):
        response = self.client.get(reverse('all_networks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/all_networks.html')
        
    def test_all_networks_list_all_networks(self):
        response = self.client.get(reverse('all_networks'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('network_list' in response.context)
        self.assertTrue(len(response.context['network_list']) == 13)

    def test_all_networks_add_network_form(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('all_networks'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('network_form' in response.context)
        self.assertTrue(len(response.context['network_list']) == 13)


class IntersectionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        network = Network.objects.create( network_name='City 101' )
        # Create 13 intersections for network tests
        number_of_networks = 13
        for intersection_id in range(number_of_networks):
            Intersection.objects.create( network_id=network, intersection_name=f'intersection {intersection_id}' )

    def test_road_networks_view_url_exists_at_desired_location(self):
        response = self.client.get('/network/1/')
        self.assertEqual(response.status_code, 200)
           
    def test_road_networks_view_url_accessible_by_name(self):
        response = self.client.get(reverse('road_network', args=(1,)))
        self.assertEqual(response.status_code, 200)
        
    def test_road_networks_view_uses_correct_template(self):
        response = self.client.get(reverse('road_network', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/road_network.html')
    
    def test_road_networks_lists_all_intersections(self):
        response = self.client.get(reverse('road_network', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('network_info' in response.context)
        
    def test_road_networks_lists_all_intersections(self):
        response = self.client.get(reverse('road_network', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('intersection_list' in response.context)
        self.assertTrue(len(response.context['intersection_list']) == 13)

    def test_road_networks_add_intersection_form(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('road_network', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('intersection_form' in response.context)
        

class AllNetworksViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_networks = 13

        for network_id in range(number_of_networks):
            Network.objects.create( network_name=f'City {network_id}' )