from django.shortcuts import render, redirect
from django.http import HttpResponse
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
        return render(request, "encyclopedia/error.html", {
          "error_title": "Page Not Found",
          "error_message": f"The page '{title}' does not exist",
          "title": title,  
        })
    
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/error.html" {
        "title": title,
        "content": util.markdown_to_html(content),
    })



def edit(request, title):
    markdown_content = util.get_entry(title)
    if not markdown_content:
        return render(request, "encyclopedia/error.html", {
            "error_message": "The requested page was not found."
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": markdown_content
    })
                      