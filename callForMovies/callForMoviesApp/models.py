from django.db import models
from django.urls import reverse
# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, help_text='Movie description')
    image = models.URLField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.id)])

class Comment(models.Model):
    movie= models.ForeignKey(Movie,related_name="comments",on_delete=models.CASCADE)
    record=models.FileField(upload_to='documents/')
    name= models.CharField(max_length=255)
    text= models.TextField(default="not converted", blank=True, null=True)
    text_french= models.TextField(default="not translated", blank=True, null=True)
    text_spanish= models.TextField(default="not translated", blank=True, null=True)
    text_german= models.TextField(default="not translated", blank=True, null=True)
    date_added= models.DateTimeField(auto_now_add=True, blank=True, null=True)
    valid = models.BooleanField(default=False)




