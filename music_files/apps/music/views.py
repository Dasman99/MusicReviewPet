from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
    FormView,
    UpdateView, CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import *


class IndexPage(ListView):
    template_name = 'index.html'
    # queryset = Playlist
    # model = Playlist
    # context_object_name = 'playlists'

    def get_queryset(self):
        return Review.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['review'] = Review.objects.all()
        context['playlists'] = Playlist.objects.all()
        context['favourite'] = Favourite.objects.all()
        return context


class ReviewListView(ListView):
    template_name = "review/review.html"
    model = Review
    queryset = Review.objects.filter(is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Review.objects.filter(is_draft=False).order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:4]

        context["review/genres"] = Genre.objects.all()

        return context


class GenreListView(ListView):
    template_name = "genre.html"
    model = Genre
    queryset = Genre.objects.all()


class GenreDetailView(DetailView):
    template_name = "genre_detail.html"
    model = Genre


class GenreCreate(CreateView):
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy("review_create.html")
    template_name = "genre_add.html"


class ArtistListView(ListView):
    template_name = "artist.html"
    model = Artist
    queryset = Artist.objects.all()


class ArtistAdd(FormView):
    model = Artist

    def get(self, request):
        form = ArtistForm
        return render(request, 'artist_add.html', context={'form': form})

    def post(self, request):
        form = ArtistForm(data=request.POST)
        if form.is_valid():
            new_add = form.save()
            return redirect(new_add)
        return render(request, 'artist_add.html', {'form': form})


class ArtistDetailView(DetailView):
    template_name = "artist_detail.html"
    model = Artist


class AlbumListView(ListView):
    template_name = "albums/albums.html"
    model = Album


class AlbumDetailView(DetailView):
    template_name = "albums/album_detail.html"
    model = Album


class ReviewDetailView(DetailView):
    template_name = "review/review_detail.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentCreateForm()
        context["comments"] = Comment.objects.filter(review=self.get_object())
        return context


class AddCommentView(LoginRequiredMixin, CreateView):

    def post(self, request, pk, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        user = request.user
        review = Review.objects.get(id=pk)
        if form.is_valid():
            Comment.objects.update_or_create(
                author=user,
                review=review,
                text=request.POST.get('text')
            )
            return redirect(f'/review/list/{review.id}/')
        return redirect(f'/review/list/{review.id}/')


class ReviewCreateView(LoginRequiredMixin, FormView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('reviews_author')
    login_url = reverse_lazy('login')
    template_name = "review/review_create.html"

    def form_valid(self, form):
        review = form.save(commit=False)
        review.author = self.request.user
        review.save()
        song_titles = form.cleaned_data['title']
        song = Song.objects.filter(title__in=song_titles)
        review.song.set(song)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('reviews_author')


class AuthorReviewListView(LoginRequiredMixin, ListView):
    template_name = "review/reviews_author.html"
    model = Review

    def get_queryset(self):
        qs = Review.objects.filter(author=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Review.objects.filter().order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:4]

        context["review/genres"] = Genre.objects.all()

        return context


def delete_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return redirect(reverse_lazy("reviews_author"))


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ReviewForm
    model = Review
    success_url = reverse_lazy("reviews_author")
    template_name = "review/review_create.html"


def deactivate_author_post(request, pk):
    post = get_object_or_404(Review, id=pk)
    post.is_draft = True
    post.save(update_fields=["is_draft"])
    return redirect(reverse_lazy("reviews_author"))


def activate_author_post(request, pk):
    post = get_object_or_404(Review, id=pk)
    post.is_draft = False
    post.save(update_fields=["is_draft"])
    return redirect(reverse_lazy("reviews_author"))


def allplaylists_view(request):
    playlists = Playlist.objects.all()
    return render(request, 'playlist/playlists.html',{'playlists':playlists,})


class PlaylistView(LoginRequiredMixin, ListView):
    template_name = "playlist/user_playlist.html"
    model = Playlist
    context_object_name = 'playlists'

    def get_queryset(self):
        qs = Playlist.objects.filter(user=self.request.user)
        return qs


class PlayListDetail(DetailView):
    template_name = "playlist/play_list.html"
    model = Playlist


class PlaylistCreateView(LoginRequiredMixin, FormView):
    # model = Playlist
    # form_class = PlaylistCreateForm
    # success_url = "user_playlist.html"
    model = Playlist
    form_class = PlaylistCreateForm
    template_name = "playlist/user_playlist.html"
    success_url = reverse_lazy("user_playlist.html")

    # def post(self, request):
    #     form = PlaylistCreateForm(data=request.POST)
    #     if form.is_valid():
    #         new_add = form.save()
    #         return redirect(new_add)
    #     return render(request, 'user_playlist.html', {'form': form})


class FavouriteListView(ListView):
    model = Favourite
    context_object_name = 'favourite'
    template_name = "favourite.html"


# class FavouriteSongsView(DetailView):
#     template_name = "favourite.html"
#     model = Favourite

from django.http.response import  JsonResponse

def add_song_to_playlist(request,id , song_pk,):
    song = get_object_or_404(Song,id=song_pk)
    playlist = get_object_or_404(Playlist , id=id)
    playlist.song.add(song)
    playlist.save()
    return JsonResponse({"status":"ok", "message":"Музыка успешно добавлена в плейлист"})


from django.core import serializers

def get_user_playlists(request):
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)
        serialized_queryset = serializers.serialize('json', playlists)
        print(serialized_queryset)
        return JsonResponse(data=serialized_queryset, safe=False)
    else:
        return JsonResponse(data={"message":"Войдите на аккаунт"})