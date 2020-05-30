from django import forms
from category.models import Categories

class CategoryForm(forms.ModelForm):
    """a model form for Categoires model with all fields

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = Categories
        fields = '__all__'
