from django.shortcuts import render
from django.http import Http404, HttpResponse

from . import util


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
        if result != -1: # find returns -1 when string doesnt contains substring
            search_results.append(entry)

    return render(request, "encyclopedia/index.html", {"entries": search_results, "search_param": searchedTitle})
