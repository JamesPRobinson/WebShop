from django.urls import path
from .views import item_list, HomeView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', item_list, name='item_list')
]
