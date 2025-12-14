from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index")
    path("<str:title>", views.entry, name="entry")
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    
]
