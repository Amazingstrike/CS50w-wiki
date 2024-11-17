from django.shortcuts import render, redirect
from . import util
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": [(entry, f"wiki/{entry}") for entry in util.list_entries()]
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html")

    content = markdown2.markdown(util.get_entry(title))    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

def search(request):
    query = str(request.GET.get("q"))
    if not query:
        return redirect("index")
    if util.get_entry(query):
        return redirect(f"wiki/{query}")
    return render(request, "encyclopedia/search.html", {
        "entries": [(entry, f"wiki/{entry}") for entry in util.list_entries() if query.lower() in entry.lower()] 
    })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    title = request.POST["title"]
    content = request.POST["content"]
    if util.get_entry(title):
        return render(request, "encyclopedia/alreadycreated.html")
    util.save_entry(title, content)
    return redirect(f"wiki/{title}")

def edit(request, title):
    content = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "content" : content,
            "title" : title
        })
    content = request.POST["content"]
    util.save_entry(title, content)
    return redirect(f"/wiki/{title}")

def random_entry():
    return redirect(f"wiki/{random.choice(util.list_entries())}")