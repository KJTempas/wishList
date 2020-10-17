from django.test import TestCase
from django.urls import reverse

from .models import Place
# Create your tests here.

class TestHomePageIsEmptyList(TestCase):

    def test_load_home_page_shows_empty_list(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertFalse(response.context['places']) 
        self.assertContains(response, 'You have no places in your wishlist')


class TestWishList(TestCase):
    #data will load from test_places.json fixture
    fixtures =['test_places']

    def test_view_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')


#test for no places visited message
class TestNoPlacesVisited(TestCase):
    def test_no_places_visited_displays_message(self):
        #with an empty database, there should be no places visited yet
        response = self.client.get(reverse('places_visited'))
        self.assertFalse(response.context['visited'])
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, "You have not visited any places yet.")


#testing that visited places, and only visited places are displayed
class TestVisitedList(TestCase):
    #load data from fixtures
    fixtures =['test_places']

    def test_view_visited_contains_only_visited(self):
        response = self.client.get(reverse('places_visited'))

        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')


class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place_to_wish_list(self):

        response = self.client.post(reverse('place_list'), { 'name': 'Tokyo', 'visited': False }, follow=True)

        #check that correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        #what data was used to populate the template?
        response_places = response.context['places']
        #should be 1 item
        self.assertEqual(len(response_places), 1)
        tokyo_response = response_places[0]

        #expect this data to be in the database. Use get() to get data with 
        #the values expected.  Will throw an exception if no data, or more than
        #one row, matches.  Remember throwing an exception will cause this test to fail
        tokyo_in_database = Place.objects.get(name='Tokyo', visited=False)

        #is the data used to render the template the same as the data in the database
        self.assertEqual(tokyo_response, tokyo_in_database)


class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):

        #visit place pk=2, New York (change NewYork to visited)
        response = self.client.post(reverse('place_was_visited', args=(2,) ), follow=True)
        #check that correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        #no New York in the response - so NY is not on the wishlist template anymore
        self.assertNotContains(response, "New York")

        #is New York visited?
        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)


    def test_visit_no_existent_place(self):

        #visit place w pk =200 does not exist
        response = self.client.post(reverse('place_was_visited', args=(200,) ), follow=True)
        self.assertEqual(response.status_code, 404) #not found