from django.shortcuts import render, get_object_or_404, redirect
from .models import Editor_Reviews
from .forms import PostForm


def index(request):
    review_list = Editor_Reviews.object.all()
    ctx = {
        'review_list': review_list
    }

    return render(request, 'editors_pick/index.html', ctx)


def detail(request, pk):
    review = get_object_or_404(Editor_Reviews, pk=pk)
    ctx = {
        'review': review,
    }
    return render(request, 'editors_pick/details.html', ctx)
# Create your views here.


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')

        else:
            form = PostForm()
        return render(request, 'editors_pick/create.html', {'form': form})
        

def update(request, pk):
    post = get_object_or_404(Editor_Reviews, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detail', pk)

    else:
        form = PostForm(instance=post)
    
    return render(request, 'editors_pick/update.html', {'forms': form})
    

def delete(request, pk):

    post = Editor_Reviews.object.get(pk=pk)
    post.delete()
    
    return redirect('index')