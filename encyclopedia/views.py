from django.shortcuts import redirect, render
from markdown2 import Markdown
from . import util
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def converter(entry):
    html = Markdown().convert(util.get_entry(entry)) if entry else None
    return html

def entrypage(request, entry):
    html = converter(entry)
    if html is None:
        return render(request, "encyclopedia/noenrty.html", {
            "entrytitle": entry
        })
    else:
        return render(request, "encyclopedia/entrypage.html", {
            "entry": html,
            "entrytitle": entry,
        })

def searchpage(request):
    query = request.GET.get('q','')
    entries = util.list_entries()
    html = converter(query)
    if (util.get_entry(query) is not None):
        return render(request, "encyclopedia/entrypage.html", {
            "entry": html
            })
    else:
        entry_list = []
        for entry in entries:
            if query.lower() in entry.lower():
                entry_list.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": entry_list,
            "search": True,
            "query": query,
        })

def newpage(request):
    return render(request, "encyclopedia/newpage.html")

def savepage(request):
    if request.method == "POST":
        title = request.POST['newpagetitle']
        text = "#"+title+"\n\n"+request.POST['newpagetext']
        if title in util.list_entries():
            return render(request, "encyclopedia/alreadyexists.html", {
                "query": title,
            })
        elif title == "":
            return render(request, "encyclopedia/newpage.html")
        else:
            util.save_entry(title, text)
            return redirect(entrypage, entry = title)

def editpage(request):
    if request.method == "POST":
        title = request.POST['title']
        text = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "entrytext": text,
            "entrytitle": title,
        })
        
def saveedit(request):
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']
        util.save_entry(title, text)
        html = converter(title)
        return redirect(entrypage, entry = title)

def randompage(request):
    if request.method == "GET":
        title = choice(util.list_entries())
        return redirect(entrypage, entry = title)
