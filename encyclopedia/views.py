from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseBadRequest
from django.urls import reverse

from . import util
import random

### CHOOSE A MARKDOWN PARSER

# puaj
from markdown2 import Markdown
markdowner = Markdown()

# Homemade
from mdparser import MarkdownParser
mdparser = MarkdownParser()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def show_entry(request, title):
    content = util.get_entry(title)

    if content == None:
        raise Http404()

    return render(
        request,
        "encyclopedia/entry.html",
        {
            "title": title,
            "content": mdparser.htmlify(content),
        },
    )


def search(request):
    searchedTitle = request.GET.get("q")
    content = util.get_entry(searchedTitle)

    if content != None:
        return redirect(reverse('show_entry', args=[searchedTitle]))

    # If entry doesnt exist, search for entries containing searchedTitle
    entries = util.list_entries()

    # Filter results
    search_results = []
    for entry in entries:
        result = entry.lower().find(searchedTitle.lower())
        if result != -1:  # find returns -1 when string doesnt contains substring
            search_results.append(entry)

    return render(
        request,
        "encyclopedia/index.html",
        {"entries": search_results, "search_param": searchedTitle},
    )


def new_page(request):
    if request.method == "POST":
        title = request.POST.get("page_title")
        content = request.POST.get("page_content")

        if util.get_entry(title) != None:
            return HttpResponseBadRequest(
                "400 ERROR: There is already a page with this title, try again with another one"
            )

        util.save_entry(title, content)

        return redirect(reverse('show_entry', args=[title]))

    # If it is a GET request
    return render(request, "encyclopedia/new_page.html")


# currently building
def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("page_content")

        util.save_entry(title, content)

        return redirect(reverse('show_entry', args=[title]))

    # If it is a GET request
    return render(
        request, "encyclopedia/edit_page.html",
        {
            "title": title,
            "content": util.get_entry(title),
        }
    )


def random_page(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    return redirect(reverse('show_entry', args=[random_page]))