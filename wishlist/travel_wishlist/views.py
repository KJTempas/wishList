from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.
#view handles request to home
def place_list(request):
    
    """if this is a POST request, the user clicked the Add button
    in the form. Check if the new place is valid, if so, save a 
    new Place to the dbase, and redirect to this same page
    This creates a GET request to this same route
    """
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save() # create a new Place obj from the form
        if form.is_valid():  # check against DB constraints, for ex, are required fields present?
            place.save()    # save to dbase
            return redirect('place_list') #redirects to GET view with name place_list - which is this same view


    #if not a POST, or the form is not valid, render the page
    #with the form to add a newj place, and list of places
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() #new form object
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list')