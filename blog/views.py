from django.shortcuts import render

posts = [
    {

        'title': 'Traditional Culture',
        'content': 'First post content',
        'date_posted': 'may 27, 2020'
    },
    {

        'title': 'Dressing Culture',
        'content': 'Second post content',
        'date_posted': 'August 28, 2019'
    },
    {

        'title': 'food culture',
        'content': 'Third post content',
        'date_posted': 'june 18 , 2024'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})