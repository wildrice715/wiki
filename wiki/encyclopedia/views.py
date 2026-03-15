from random import choice
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from markdown2 import markdown
from . import util


def index(request):
    """ Home Page, displays all available entries """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, title):
   
       entry_md = util.get_entry(title)

    if entry_md != None:
        # Title exists, convert md to HTML and return rendered template
        entry_HTML = Markdown().convert(entry_md)
        return render(request, "encyclopedia/entry.html", {
          "title": title,
          "entry": entry_HTML,
          "search_form": SearchForm(),
          })
    else:
        # Page does not exist, get links for similar titles:
        related_titles = util.related_titles(title)

        return render(request, "encyclopedia/error.html", {
          "title": title,
          "related_titles": related_titles,
          "search_form": SearchForm(),
          })



def search(request):
 # If search page reached by submitting search form:
    if request.method == "POST":
        form = SearchForm(request.POST)

        # If form is valid try to search for title:
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_md = util.get_entry(title)

            print('search request: ', title)

            if entry_md:
                # If entry exists, redirect to entry view
                return redirect(reverse('entry', args=[title]))
            else:
                # Otherwise display relevant search results
                related_titles = util.related_titles(title)

                return render(request, "encyclopedia/search.html", {
                "title": title,
                "related_titles": related_titles,
                "search_form": SearchForm()
                })

    # Otherwise form not posted or form not valid, return to index page:
    return redirect(reverse('index'))



def create(request):
    """ Lets users create a new page on the wiki """
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {"error": "Page already exists!"})
        elif title == "" or content == "":
            return render(request, "encyclopedia/create.html", {"error": "Title and content are required!"})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")



def edit(request, title):
    """ Lets users edit an existing page on the wiki """
    content = util.get_entry(title.strip())
    if content is None:
        return render(request, "encyclopedia/edit.html", {'error': "Page Not Found"})
    if request.method == "GET":
        content = request.GET.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html",
                          {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})



def random(request):
    """ Loads a random page from the wiki """
    entries = util.list_entries()

    titles = util.list_entries()
    title = random.choice(titles)

    return redirect("entry", title=choice(entries))