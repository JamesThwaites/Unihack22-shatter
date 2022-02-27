# urls.py
#
# Facilitates database interaction

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
