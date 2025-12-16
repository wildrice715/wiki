from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:pagename>", views.page, name="page"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("create", views.create, name="create"),
    path("makePage", views.makePage, name="makePage"),
    path("wiki/<str:pagename>/edit", views.edit, name="edit"),
    path("wiki/<str:pagename>/editPage", views.editPage, name="editPage")
    path("wiki/<str:entry>", views.entry, name="entry"),
]
