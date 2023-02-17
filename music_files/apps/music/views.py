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


# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import *


class IndexPage(TemplateView):
    template_name = 'index.html'


class ReviewListView(ListView):
    template_name = "review.html"
    model = Review
    queryset = Review.objects.filter(is_draft=False)


class GenreListView(ListView):
    template_name = "genre.html"
    model = Genre
    queryset = Genre.objects.all()


class GenreDetailView(DetailView):
    template_name = "genre_detail.html"
    model = Genre


class GenreCreate(View):

    def get(self, request):
        form = GenreForm
        return render(request, 'genre_add.html', context={'form': form})

    def post(self, request):
        bound_form = GenreForm()
        if bound_form.is_valid():
            new_add = bound_form.save()
            return redirect(new_add)
        return render(request, 'genre.html', context={'form': bound_form})


class ArtistListView(ListView):
    template_name = "artist.html"
    model = Artist
    queryset = Artist.objects.all()


class ArtistAdd(View):

    def get(self, request):
        form = ArtistForm
        return render(request, 'artist_add.html', context={'form': form})

    def post(self, request):
        bound_form = ArtistForm()
        if bound_form.is_valid():
            new_add = bound_form.save()
            return redirect(new_add)
        return render(request, 'artist_add.html', context={'form': bound_form})


class AlbumListView(ListView):
    template_name = "albums.html"
    model = Album
    queryset = Album.objects.filter(is_draft=False)


class AlbumDetailView(DetailView):
    template_name = "album_detail.html"
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Album.objects.filter(is_draft=False).order_by("-release")
        if len(latest_posts) < 4:
            context["latest_albums"] = latest_posts
        else:
            context["latest_albums"] = latest_posts[:4]

        return context


# class UploadView(FormView):
#     template_name = 'form.html'
#     form_class = UploadForm
#     success_url = '/done/'
#
#     def form_valid(self, form):
#         for each in form.cleaned_data['attachments']:
#             Attachment.objects.create(file=each)
#         return super(UploadView, self).form_valid(form)


class ArtistDetailView(DetailView):
    template_name = "artist_detail.html"
    model = Artist


class ReviewDetailView(DetailView):
    template_name = "review_detail.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super(ReviewDetailView,self).get_context_data(**kwargs)
        comments = Comment.objects.filter(review=self.get_object())
        context['comments'] = comments
        context['form'] = CommentCreateForm
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
    form_class = UploadForm
    success_url = reverse_lazy('review_detail')
    login_url = reverse_lazy('login')
    template_name = "review_create.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class AuthorReviewListView(LoginRequiredMixin, ListView):
    template_name = "reviews_author.html"
    model = Review

    def get_queryset(self):
        qs = Review.objects.filter(author=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Review.objects.filter(is_draft=False).order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:4]

        context["genres"] = Genre.objects.all()

        return context


def delete_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return redirect(reverse_lazy("reviews_author"))


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UploadForm
    model = Review
    success_url = reverse_lazy("reviews_author")
    template_name = "review_create.html"

