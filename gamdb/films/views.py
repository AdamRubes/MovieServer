from django.shortcuts import render
from .models import Movie, Director, Actor, Genre, Comment
from django.db.models import Q
from .forms import CommentForm
from django.db.models import Avg
from django.shortcuts import redirect

def directors(request):
    context = {
        'directors': Director.objects.all()
    } 
    print(context)
    return render(request, 'directors.html', context)
 
def director(request, id):
    context = {
        "director": Director.objects.get(id=id)
    }
    return render(request, 'director.html', context)

def movies(request):
    movies_queryset = Movie.objects.all()
    genre = request.GET.get('genre')
    if genre:
        movies_queryset = movies_queryset.filter(genres__name=genre)
    search = request.GET.get('search')
    if search:
        movies_queryset = movies_queryset.filter(Q(name__icontains=search)|Q(description__icontains=search)) 

    context = {
        "movies": movies_queryset,
        "genres": Genre.objects.all().order_by('name'),
        "genre": genre,
        "search": search,
    }
    return render(request, 'movies.html', context)

def movie(request, id):
    m = Movie.objects.get(id=id)
    f = CommentForm()
    commentArray = Comment.objects.filter(movie=m).order_by('-created_at')

    #Bez jasného typu je to pain
    avgRating = commentArray.aggregate(Avg('rating'))['rating__avg'] or 0


    if request.POST:
        f = CommentForm(request.POST)
        if f.is_valid():
            # ulozit do DB
            c = Comment(
                movie=m,
                author=f.cleaned_data.get('author'),
                text=f.cleaned_data.get('text'),
                rating=f.cleaned_data.get('rating'),
            )
            if not c.author:
                c.author = 'Anonym'
            c.save()
            #přepočítat avg
            commentArray = Comment.objects.filter(movie=m).order_by('-created_at')
            avgRating = commentArray.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

            # nastavit prazdny form
            f = CommentForm()
            return redirect('movie', id=id)
            
    context = {
        "movie": m,
        "comments": commentArray,
        "averageRating": avgRating,
        "form": f
    }

    return render(request, 'movie.html', context)

def actors(request):
    context = {
        "actors": Actor.objects.all()
    }
    return render(request, 'actors.html', context)

def actor(request, id):
    context = {
        "actor": Actor.objects.get(id=id)
    }
    return render(request, 'actor.html', context)

def homepage(request):
    context = {
        # TODO use first 10 top rated
        "movies": Movie.objects.all(),
        "actors": Actor.objects.all(),
        "directors": Director.objects.all(),
        "genres": Genre.objects.all(),
    }
    return render(request, 'homepage.html', context)