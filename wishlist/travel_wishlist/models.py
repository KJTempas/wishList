from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Create your models here.
class CatFact(models.Model):
    fact = models.CharField(max_length=500)

    def __str__(self):
        return self.fact


class Place(models.Model):
    #these will map to column in a table #cascade means delete all places if user is deleted
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)  #text field unlimited size(charfiels are limited)
    date_visited = models.DateField(blank=True, null=True)  #null = True means not required
                                            #new file; optional 
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    #this overrides the save method of the model
    #to delete photo file when a photo is replaced for a Place
    def save(self, *args, **kwargs):
        #get reference to previous version of this Place
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            #if there is a previous Place, and that Place has a photo
            #it that old places photo is not the same as the photo
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        #call to the super class method (Django's save method)
        super().save(*args, **kwargs)

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo) #calling method above
        #call through to django super function to do the actual delete
        super().delete(*args, **kwargs)


    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes' #only first 100 characters of notes string
        return f'{self.name}, visited? {self.visited} on {self.date_visited}. Notes: {notes_str}\nPhoto {photo_str}'