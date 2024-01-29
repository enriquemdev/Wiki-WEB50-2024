from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseBadRequest

from . import util

import random

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def show_entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        raise Http404()

    return render(
        request,
        "encyclopedia/entry.html",
        {
            "title": title,
            "content": entry,
        },
    )


def search(request):
    searchedTitle = request.GET.get("q")
    entry = util.get_entry(searchedTitle)

    if entry != None:
        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": searchedTitle,
                "content": entry,
            },
        )

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

        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": title,
                "content": util.get_entry(title),
            },
        )

    # If it is a GET request
    return render(request, "encyclopedia/new_page.html")


# currently building
def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("page_content")

        util.save_entry(title, content)

        return render(
            request,
            "encyclopedia/entry.html",
            {
                "title": title,
                "content": util.get_entry(title),
            },
        )

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
    return render(
        request, "encyclopedia/entry.html",
        {
            "title": random_page,
            "content": util.get_entry(random_page),
        }
    )