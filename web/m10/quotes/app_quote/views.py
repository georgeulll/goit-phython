from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Quotes, Tag, Author
from .forms import AuthorForm, QuotesForm, TagForm


def main(request):
    return render(request, 'app_quotes/index.html', context={'title': 'Quotes portal'})

@login_required
def upload_quotes(request):
    if request.method == 'POST':
        form = QuotesForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            return redirect(to='app_quotes:root')
        else:
            return render(request,'app_quotes/upload_quotes.html', context={'title': 'Quotes portal', 'form': form})
    return render(request, 'app_quotes/upload_quotes.html', context={'title': 'Quotes portal', 'form': QuotesForm()})


def quotes(request):
    tags_ = Tag.objects.all()
    quotes_ = Quotes.objects.all().order_by("-id")

    return render(request, 'app_quotes/quotes.html', context={'title': 'Quotes portal', 'quotes_': quotes_,
                                                              'tags_': tags_})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='app_quotes:root')
        else:
            return render(request, 'app_quotes/add_author.html', context={'title': 'Quotes portal', 'form': form})
    return render(request, 'app_quotes/add_author.html', context={'title': 'Quotes portal', 'form': AuthorForm()})


@login_required
def add_tags(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='app_quotes:root')
        else:
            return render(request, 'app_quotes/add_tag.html', context={'title': 'Quotes portal', 'form': form})
    return render(request, 'app_quotes/add_tags.html', context={'title': 'Quotes portal', 'form': TagForm()})


def author_detail(request, id):
    author = Author.objects.get(pk=id)
    return render(request, 'app_quotes/author.html', context={'title': 'Quotes portal', 'author': author})