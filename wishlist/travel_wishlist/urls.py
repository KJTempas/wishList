from django.urls import path
from . import views

urlpatterns = [
    #a path of '' is to the home page; a path of 'visited' takes user to that page
    path('', views.place_list, name='place_list'),
    #(pathname, method called in views)
    path('visited', views.places_visited, name='places_visited'),
    #this path uses the primary key (variable name place_pk) to identify which place was visited
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited'),
    path('place/<int:place_pk>', views.place_detail, name='place_details'), #captures any pk
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),
    path('about', views.about, name='about')
]