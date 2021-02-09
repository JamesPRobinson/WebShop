from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import GraphChoices

# iterable
GRAPH_CHOICES = (
    ("1", "Location"),
    ("2", "Avg. Price"),
    ("3", "Category"),
    ("4", "Discount Ratio"),
    ("5", "Items Bought"),
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        }))
    post_code = forms.CharField()
    set_default_address = forms.BooleanField(required=False)
    use_default_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(
        widget=forms.CheckboxInput(), required=False)


class GraphChoiceForm(forms.Form):
    x_field = forms.ChoiceField(choices=GRAPH_CHOICES)
    y_field = forms.ChoiceField(choices=GRAPH_CHOICES, initial="2")
