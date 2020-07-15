from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from markdown2 import Markdown
from . import util

class SearchForm(forms.Form):
    """ Form Class for Search Bar """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Qwikipedia"}))


def index(request):
    """ Home Page on Site, displays all available entries """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm(),
    })

def entry(request, title):
    """ Displays the requested entry page, if it exists """

    entry_md = util.get_entry(title)

    if entry_md:
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
    """ Loads requested title page if it exists, else displays search results """

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


