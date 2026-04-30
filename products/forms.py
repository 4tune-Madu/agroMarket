from django import forms
from .models import Product

from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    new_category = forms.CharField(required=False)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'quantity',
            'unit',
            'image',
            'categories'
        ]