from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import os
import random
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/error.html', {
          "error_title": "Page Not Found",
          "message": f"The page does not exist",
          "title": title,  
        })
    
    return render(request, 'encyclopedia/entry.html', {
        "title": title,
        "content": markdown2.markdown(content),
    })



def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist."
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })               