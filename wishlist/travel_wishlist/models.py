from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Place(models.Model):
    #these will map to column in a table #cascade means delete all places if user is deleted
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)  #text field unlimited size(charfiels are limited)
    date_visited = models.DateField(blank=True, null=True)  #null = True means not required
                                            #new file; optional 
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)


    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes' #only first 100 characters of notes string
        return f'{self.name}, visited? {self.visited} on {self.date_visited}. Notes: {notes_str}\nPhoto {photo_str}'