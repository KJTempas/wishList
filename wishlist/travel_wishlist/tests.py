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
        

