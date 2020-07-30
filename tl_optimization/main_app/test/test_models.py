from django.test import TestCase
from ..models import *


class NetworkModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Network.objects.create(network_name='Pretoria')

    def test_network_name_label(self):
        network = Network.objects.get(pk=1)
        field_label = network._meta.get_field('network_name').verbose_name
        self.assertEquals(field_label, 'network name')

    def test_network_name_max_length(self):
        network = Network.objects.get(pk=1)
        max_length = network._meta.get_field('network_name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_network_name(self):
        network = Network.objects.get(pk=1)
        expected_object_name = network.network_name
        self.assertEquals(expected_object_name, str(network))

    def test_get_absolute_url(self):
        network = Network.objects.get(pk=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(network.get_absolute_url(), '/network/1/')

# Old Test//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class IntersectionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        network = Network.objects.create(network_name="Hatfield")
        Intersection.objects.create( network_id=network ,intersection_name="street1-street2")

    # intersection_name ............
    def test_intersection_name_label(self):
        intersection = Intersection.objects.get(pk=1)
        field_label = intersection._meta.get_field('intersection_name').verbose_name
        self.assertEquals(field_label, 'intersection name')

    def test_intersection_name_max_length(self):
        intersection = Intersection.objects.get(pk=1)
        max_length = intersection._meta.get_field('intersection_name').max_length
        self.assertEquals(max_length, 50)

    # right_of_way ..................
    def test_right_of_way_name_label(self):
        intersection = Intersection.objects.get(pk=1)
        field_label = intersection._meta.get_field('right_of_way').verbose_name
        self.assertEquals(field_label, 'right of way')


    # configuration ............
    def test_intersection_name_label(self):
        intersection = Intersection.objects.get(pk=1)
        field_label = intersection._meta.get_field('configuration').verbose_name
        self.assertEquals(field_label, 'configuration')

    # Custom Methods ............
    def test_intersection_name_is_intersection_name(self):
        intersection = Intersection.objects.get(pk=1)
        expected_object_name = intersection.intersection_name
        self.assertEquals(expected_object_name, str(intersection))

    def test_get_absolute_url(self):
        intersection = Intersection.objects.get(pk=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(intersection.get_absolute_url(), '/network/1/1/')

# Test for the Road Model ............
class RoadTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        network = Network.objects.create(network_name="Sunnyside")
        Intersection.objects.create(network_id=network, intersection_name="hilder-south")
        Road.objects.create(network_id=network, road_name="r123")

    # Testing Road label.........
    def test_road_name_label(self):
        road = Road.objects.get(pk=1)
        field_label = road._meta.get_field('road_name').verbose_name
        self.assertEquals(field_label, 'road name')

    def test_road_name_max_length(self):
        road = Road.objects.get(pk=1)
        max_length = road._meta.get_field('road_name').max_length
        self.assertEquals(max_length, 50)

    # Testing Other non string label.........
    def test_network_name_label(self):
        road = Road.objects.get(pk=1)
        field_label = road._meta.get_field('network_id').verbose_name
        self.assertEquals(field_label, 'network id')

    def test_intersection_in_name_label(self):
        road = Road.objects.get(pk=1)
        field_label = road._meta.get_field('intersection_in').verbose_name
        self.assertEquals(field_label, 'intersection in')
    
    def test_intersection_out_name_label(self):
        road = Road.objects.get(pk=1)
        field_label = road._meta.get_field('intersection_out').verbose_name
        self.assertEquals(field_label, 'intersection out')

    def test_road_distance_name_label(self):
        road = Road.objects.get(pk=1)
        field_label = road._meta.get_field('road_distance').verbose_name
        self.assertEquals(field_label, 'road distance')

    def test_average_speed_name_label(self):
        road = Road.objects.get(pk=1)
        field_label = road._meta.get_field('average_speed').verbose_name
        self.assertEquals(field_label, 'average speed')

    # Testing custom methods ......
    def test_road_name_is_road_name(self):
        road = Road.objects.get(pk=1)
        expected_object_name = road.road_name
        self.assertEquals(expected_object_name, str(road))

    def test_get_absolute_url(self):
        road = Road.objects.get(pk=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(road.get_absolute_url(), '/network/1/1/')



# Test for the Road Model ............
class TrafficLightTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        network = Network.objects.create(network_name="Sunnyside")
        intersection = Intersection.objects.create(network_id=network, intersection_name="hilder-south")
        TrafficLight.objects.create(intersection_id=intersection)