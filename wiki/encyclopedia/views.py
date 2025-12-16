from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
from random import choice
import os


markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, pagename):
    try:
        return render(request, "encyclopedia/page.html", {
            "entry": markdowner.convert(util.get_entry(pagename)),
            "page_name": pagename
            })
    except TypeError:
        return render(request, "encyclopedia/error.html")
    
def search(request):
    search_name = request.GET.get('q')
    try:
        return render(request, "encyclopedia/page.html", {
            "entry": markdowner.convert(util.get_entry(search_name)),
            "page_name": search_name
            })
    except TypeError:
        return render(request, "encyclopedia/search.html", {
            "entries": util.list_entries(),
            "search_name": search_name
        })
    

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return redirect(f"wiki/{entry}")


def create(request):
    return render(request, "encyclopedia/create.html")


def makePage(request):
    new_title = request.GET.get('titleCreation')
    new_entry = request.GET.get('entryCreation')
    filepath = os.path.join("entries", f"{new_title}.md")
    if os.path.exists(filepath):
        return render(request, "encyclopedia/error.html")
    with open(filepath, "w") as file:
        file.write(new_entry)
    return redirect(f"wiki/{new_title}")


def edit(request, pagename):
    filepath = os.path.join("entries", f"{pagename}.md")
    with open(filepath, "r") as file:
        return render(request, "encyclopedia/edit.html", {
            "page_name": pagename,
            "file": file.read()
        })

def editPage(request, pagename):
    filepath = os.path.join("entries", f"{pagename}.md")
    entry = request.GET.get('entryEdit')
    with(open(filepath, "w")) as file:
        file.write(entry)
    return redirect(f"/wiki/{pagename}")

def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/error.html",{
            "entry": markdowner.convert(entryPage),
            "entryTitle": entry
        })