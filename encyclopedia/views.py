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
        print(entry_HTML)
        return render(request, "encyclopedia/entry.html", {"title": title, "entry": entry_HTML})
    else:
        return HttpResponse("Oops, could not find that entry!")

