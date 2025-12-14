from django.shortcuts import render

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
    
    html_content = markdown.markdown(content)
    return render(request, "encyclopedia/error.html" {
        "title": title,
        "content": util.markdown_to_html(content),
    })
                      