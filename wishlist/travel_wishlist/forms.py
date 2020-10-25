from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:  #this will create a form that django uses and links the Place model to the fields in the form
        model = Place
        fields = ('name', 'visited')