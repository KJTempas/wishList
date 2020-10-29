from django import forms
from django.forms import FileInput, DateInput
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:  #this will create a form that django uses and links the Place model to the fields in the form
        model = Place
        fields = ('name', 'visited')

#create a custom date input field
class DateInput(forms.DateInput): #this will provide a date picker
    input_type = 'date' #to override the default input type, which is 'text'

class TripReviewForm(forms.ModelForm):
    class Meta: #new form 
        model = Place
        fields = {'notes', 'date_visited', 'photo'}
        widgets = {
            'date_visited': DateInput()
            #by default, Python displays dae inputs as plain text.  
            #the DateInput class overrides this and uses a HTML date element instead
        }