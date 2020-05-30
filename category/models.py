from django.db import models

# Create your models here.


class Categories(models.Model):
    """a table to stor category with title, style, image and description
       and is_available field for show or not show category at registartion process

    Arguments:
        models {MODULE} -- a django built-in class to define tables

    Returns:
        STRING -- returns title of category
    """    
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(max_length=225, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='category/img/%Y-%m-%d')

    is_available = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
