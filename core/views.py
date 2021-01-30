from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Item


# Listview as we are listing out the items
class HomeView(ListView):
    model = Item
    template_name = 'home.html'


def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home.html", context)
