from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Editor_Review
from .forms import Editors_Reviews_Form
from users.models import Editor
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from core.models import NoQuerySet, AuthorNotMatched


def index(request):
    try:
        first_review = Editor_Review.objects.first()
        if first_review is None:
            raise NoQuerySet
        review_list = Editor_Review.objects.all()[1:]
        if review_list is None:
            raise NoQuerySet
        editors = Editor.objects.all()
        if editors is None:
            raise NoQuerySet
        ctx = {
            'first_review': first_review,
            'review_list': review_list,
            'editors': editors,
        }
        return render(request, 'editor_reviews/editor_reviews_list.html', ctx)
    except NoQuerySet:
        return redirect(reverse('core:main'))


def detail(request, pk):
    review = get_object_or_404(Editor_Review, pk=pk)
    ctx = {
        'review': review,
    }
    return render(request, 'editor_reviews/editor_reviews_detail.html', ctx)
# Create your views here.


@login_required
def create(request):
    try:
        user = request.user.editor
    except ObjectDoesNotExist:
        return redirect(reverse('editors_pick:index'))

    if request.method == 'POST':
        form = Editors_Reviews_Form(request.POST, request.FILES)
        if form.is_valid():
            print("form validation 완료")
            editor_review = Editor_Review(**(form.cleaned_data))
            editor_review.author = user
            editor_review.save()
            return redirect(reverse('editors_pick:detail', args=[editor_review.pk]))
        else:
            print("form validation 실패")
            return redirect(reverse("core:main"))
    else:
        form = Editors_Reviews_Form()
        ctx = {
            'form': form,
        }
        return render(request, 'editor_reviews/editor_reviews_create.html', ctx)


@login_required
def update(request, pk):
    post = get_object_or_404(Editor_Review, pk=pk)

    try:
        user = request.user.editor
        if post.author != user:
            raise AuthorNotMatched
    except ObjectDoesNotExist:
        return redirect(reverse("core:main"))
    except AuthorNotMatched:
        return redirect(reverse("core:main"))

    if request.method == 'POST':
        form = Editors_Reviews_Form(request.POST, request.FILES)
        if form.is_valid():
            print("form validation 완료")
            editor_review = Editor_Review(**(form.cleaned_data))
            editor_review.save()
            return redirect('editors_pick:detail', pk)
        else:
            print("form validation 실패")
            return redirect(reverse("core:main"))
    else:
        form_data = {
            'title': post.title,
            'contents': post.contents,
            'main_image': post.main_image.url,
            'post_category': post.post_category,
            'product_category': post.product_category,
            'product': post.product,
        }
        form = Editors_Reviews_Form(form_data)
        ctx = {
            'form': form,
        }
        return render(request, 'editor_reviews/editor_reviews_create.html', ctx)


@login_required
def delete(request, pk):
    post = get_object_or_404(Editor_Review, pk=pk)

    try:
        user = request.user.editor
        if post.author != user:
            raise AuthorNotMatched
    except ObjectDoesNotExist:
        return redirect(reverse("core:main"))
    except AuthorNotMatched:
        return redirect(reverse("core:main"))

    post.delete()

    return redirect(reverse('core:main'))
