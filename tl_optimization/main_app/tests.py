from django.test import TestCase
from main_app.models import Road
from main_app.models import Intersection

# Create your tests here.
class RoadTestCase(TestCase):

    def setUp(self):
        Intersection.objects.create(name="hilder-south")
        Road.objects.create(name="r123")
    

    def test_duplicate_intersection(self):
        """Animals that can speak are correctly identified"""
        junction = Intersection.objects.get(name="hilder-south")
        r1 = Road.objects.get(name="r123")
        r1.intersection_in = junction
        r1.intersection_out = junction
        r1.save()
        self.assertEqual(r1.intersection_in, r1.intersection_in)

    def test_road_capacity_vs_number_of_artefacts(self):
        results = False
        self.assertTrue(results)


class IntersectionTestCase(TestCase):

    def setUp(self):
        rules = {
            "flow": {
                "r101": {
                    "r102": {
                        "blocking": ["r103"]
                    },
                    "r103": {
                        "blocking": ["r102"]
                    }
                }
            }
        }
        Intersection.objects.create(name="street1-street2", right_of_way=rules)

    def test_right_of_way_rules(self):
        """Animals that can speak are correctly identified"""
        #lion = Animal.objects.get(name="lion")
        #cat = Animal.objects.get(name="cat")
        #self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual("", "")

    def test_right_of_way_violation(self):
        """ Check that the configuration set does not allow violation of the right of way rules """
        results = False
        self.assertTrue(results)
