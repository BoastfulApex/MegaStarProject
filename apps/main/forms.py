from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    groupname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Slider nomi uz",
                "class": "form-control",
                'readonly': 'readonly'
            }
        ))

    number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Slider nomi ru",
                "class": "form-control",
                'readonly': 'readonly',
    }
        ))
    image = forms.ImageField(
      widget=forms.FileInput()
    )

    class Meta:
        model = Category
        fields = "__all__"


class SubCategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Slider nomi uz",
                "class": "form-control",
                'readonly': 'readonly'
            }
        ))

    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'readonly': 'readonly',
            }
        ))

    category = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control",
                'readonly': 'readonly'
            }
        ),
        queryset=Category.objects.all())

    image = forms.ImageField(
      widget=forms.FileInput()
    )

    class Meta:
        model = SubCategory
        fields = "__all__"


class ManufacturerForm(forms.ModelForm):
    manufacturer_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'readonly': 'readonly'
            }
        ))

    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'readonly': 'readonly',
            }
        ))
    image = forms.ImageField(
      widget=forms.FileInput()
    )

    class Meta:
        model = Category
        fields = "__all__"


class ProductForm(forms.ModelForm):
    itemname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))
    itemcode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Maxsulot izohi",
                "class": "form-control",
            }
        ))
    price = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Maxsulot narxi",
                "class": "form-control",
            }
        ))
    image = forms.ImageField(
      widget=forms.FileInput()
    )

    class Meta:
        model = Product
        fields = ["itemname", "itemcode", "description", "price", "image"]


class CashbackForm(forms.ModelForm):
    PERIOD_TYPES = (
        (MONTH, MONTH),
        (SEASON, SEASON),
        (YEAR, YEAR)
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ))
    period = forms.ChoiceField(
        choices=PERIOD_TYPES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                'readonly': 'readonly'
            }
        ))
    summa = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Summa",
                "class": "form-control",
            }
        ))
    persent = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Summa",
                "class": "form-control",
            }
        ))

    class Meta:
        model = Product
        fields = ["name", "summa", "period", "persent"]
