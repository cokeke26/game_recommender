from django.urls import path
from .views import game_list, game_detail, toggle_favorite, toggle_like, my_favorites, my_likes, search_suggest, signup

urlpatterns = [
    path("", game_list, name="game_list"),
    path("game/<int:game_id>/", game_detail, name="game_detail"),

    path("game/<int:game_id>/favorite/", toggle_favorite, name="toggle_favorite"),
    path("game/<int:game_id>/like/", toggle_like, name="toggle_like"),

    path("me/favorites/", my_favorites, name="my_favorites"),
    path("me/likes/", my_likes, name="my_likes"),

    path("api/search-suggest/", search_suggest, name="search_suggest"),

    path("accounts/signup/", signup, name="signup"),
]
