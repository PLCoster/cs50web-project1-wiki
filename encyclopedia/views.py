from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """ Displays the requested entry page, if it exists """

    entry_md = util.get_entry(title)

    if entry_md:
        # Title exists, convert md to HTML and return rendered template
        entry_HTML = Markdown().convert(entry_md)
        return render(request, "encyclopedia/entry.html", {"title": title, "entry": entry_HTML})
    else:
        # Page does not exist, get links for similar titles:
        related_titles = []
        related = False
        for entry_name in util.list_entries():
            if title in entry_name or entry_name in title:
                related = True
                related_titles.append(entry_name)

        return render(request, "encyclopedia/error.html", {"title": title, "related": related, "related_titles" : related_titles})

