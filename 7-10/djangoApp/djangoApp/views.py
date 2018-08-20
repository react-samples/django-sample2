from django.http import Http404
from django.shortcuts import render, redirect
from .models import Feed
from .forms import FeedForm

def index(request):
    feeds = Feed.objects.all()
    return render(request, 'index.html', {'feeds': feeds})

def form(request):
    form = FeedForm()
    return render(request, 'form.html', {'form': form})

def search(request):
    try:
        feed = Feed.objects.get(title=request.GET["q"])
        return render(request, 'result.html', {'feeds': [feed]})
    except Feed.DoesNotExist:
        raise Http404("フィードがありません")

def post(request):
    if request.method != 'POST':
        return redirect(to="/form")
    form = FeedForm(request.POST)
    if form.is_valid():
        feed = Feed.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            href=request.POST['href'])
        feed.save()
        return redirect(to="/")
    else:
        return redirect(to="/form")

def delete(request):
    if request.method == 'POST' and request.POST['id']:
        feed = Feed.objects.get(id=request.POST['id'])
        feed.delete()
        return redirect(to="/")
