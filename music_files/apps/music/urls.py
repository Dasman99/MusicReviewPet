from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('review/author/list', views.AuthorReviewListView.as_view(), name='reviews_author'),
    path('review/create/', views.ReviewCreateView.as_view(), name="review_create"),
    path('review/update/<int:pk>', views.ReviewUpdateView.as_view(), name="review_update"),
    path('review/delete/<int:pk>/', views.delete_review, name='review_delete'),
    path('playlists/', views.allplaylists_view,name='playlists'),
    path('user_playlist/', views.PlaylistView.as_view(), name='user_playlist'),
    path('favourite/', views.FavouriteListView.as_view(), name="favourite"),
    path('review/deactivate/<int:pk>/', views.deactivate_author_post, name="deactivate_review"),
    path('review/activate/<int:pk>/', views.activate_author_post, name="activate_review"),

    # list's
    path('review/list/', views.ReviewListView.as_view(), name='review_list'),
    path('genre/list/', views.GenreListView.as_view(), name='genre_list'),
    path('artist/list/', views.ArtistListView.as_view(), name='artist_list'),
    path('album/list/', views.AlbumListView.as_view(), name='album_list'),
    path('playlist/detail/<int:pk>', views.PlayListDetail.as_view(), name="playlist_detail"),
    path('playlist/list/', views.get_user_playlists),
    path('playlist/add/<int:id>/<int:song_pk>/', views.add_song_to_playlist),

    # detail's
    path('artist/list/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('album/list/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('genre/list/<int:pk>', views.GenreDetailView.as_view(), name='genre_detail'),
    path('review/list/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),

    # adds
    path('genre/add/', views.GenreCreate.as_view(), name='genre_add'),
    path('artist/add/', views.ArtistAdd.as_view(), name='artist_add'),
    path('add/comment/<int:pk>/', views.AddCommentView.as_view(), name="add_comment"),
    path('create/playlist/', views.PlaylistCreateView.as_view(), name='create_playlist')
]