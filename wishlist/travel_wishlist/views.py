from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# Create your views here.
#view handles request to home


@login_required #this will require login before accessing this method
def place_list(request):
    
    """if this is a POST request, the user clicked the Add button
    in the form. Check if the new place is valid, if so, save a 
    new Place to the dbase, and redirect to this same page
    This creates a GET request to this same route
    """
    if request.method == 'POST': #creating from data in the request
        form = NewPlaceForm(request.POST) #create form from data 
        place = form.save(commit=False) # get data but don't save yet. create a new Place obj from the form
        place.user = request.user
        if form.is_valid():  # check against DB constraints, for ex, are required fields present?
            place.save()    # save to Place dbase
            #reload home page
            return redirect('place_list') #redirects to GET view with name place_list - which is this same view

    #if not a POST, or the form is not valid, render the page
    #with the form to add a newj place, and list of places
    #this is like a dbase query. get all Place objects where visited in false, and order alphabetically
    #filter by user=requests.user will show only places related that the user that is signed in
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    #this makes a new Place Form (model in forms.py); the form's fields will align with Place table columns
    new_place_form = NewPlaceForm() #new form object - empty
    #render means write to the template; template name is wishlist.html, write places (see in template)
    #django will combine places and input from the new_place_form to generate the html page
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

def about(request):
    author = 'Kathryn'
    about = 'About website to create a list of places to visit'
           #render  (what, where - the html page, {data} to render)
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
        #render visited.html page with {this data}
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
                 # pk is column name,  place_pk is variable
        #earlier version before adding 404 was 
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user: #make sure user has input this place
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden
    return redirect('place_list') #place_list is the name of the path in urls.py

@login_required
def place_detail(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'travel_wishlist/place_detail.html',{'place': place} )

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:#make sure this user is authorized  - user attached to place should be same as this user
        place.delete()
        #need to return a response - a redirect is another get request to this new url(place_list)
        return redirect('place_list')
    else:
        return HttpResponseForbidden()