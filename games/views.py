from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q

from .models import Game, Platform, Genre, Favorite, Like
from .services.recommender import similar_games

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from django.contrib.auth import login
from .forms import SignUpForm

def game_list(request):
    q = request.GET.get("q", "").strip()
    platform = request.GET.get("platform", "").strip()
    genre = request.GET.get("genre", "").strip()

    games = Game.objects.all().prefetch_related("platforms", "genres", "tags")

    if q:
        games = games.filter(Q(name__icontains=q) | Q(summary__icontains=q))

    if platform:
        games = games.filter(platforms__name=platform)

    if genre:
        games = games.filter(genres__name=genre)

    games = games.distinct().order_by("-rating", "-release_year", "name")[:50]

    context = {
        "games": games,
        "q": q,
        "platforms": Platform.objects.order_by("name"),
        "genres": Genre.objects.order_by("name"),
        "platform_selected": platform,
        "genre_selected": genre,
    }
    return render(request, "games/game_list.html", context)

def game_detail(request, game_id: int):
    game = get_object_or_404(
        Game.objects.prefetch_related("platforms", "genres", "tags"),
        id=game_id
    )

    is_fav = False
    is_like = False
    if request.user.is_authenticated:
        is_fav = Favorite.objects.filter(user=request.user, game=game).exists()
        is_like = Like.objects.filter(user=request.user, game=game).exists()

    similar = similar_games(game.id, top_k=8)
    similar_ids = [gid for gid, _ in similar]
    similar_map = {g.id: g for g in Game.objects.filter(id__in=similar_ids).prefetch_related("platforms", "genres")}
    similar_games_list = [similar_map[gid] for gid in similar_ids if gid in similar_map]

    return render(request, "games/game_detail.html", {
        "game": game,
        "is_fav": is_fav,
        "is_like": is_like,
        "similar_games": similar_games_list,
    })

@login_required
def toggle_favorite(request, game_id: int):
    game = get_object_or_404(Game, id=game_id)
    fav = Favorite.objects.filter(user=request.user, game=game)
    if fav.exists():
        fav.delete()
    else:
        Favorite.objects.create(user=request.user, game=game)
    return redirect("game_detail", game_id=game.id)

@login_required
def toggle_like(request, game_id: int):
    game = get_object_or_404(Game, id=game_id)
    lk = Like.objects.filter(user=request.user, game=game)
    if lk.exists():
        lk.delete()
    else:
        Like.objects.create(user=request.user, game=game)
    return redirect("game_detail", game_id=game.id)

@login_required
def my_favorites(request):
    games = Game.objects.filter(favorited_by__user=request.user).distinct().order_by("-rating", "name")
    return render(request, "games/my_list.html", {"title": "⭐ Mis favoritos", "games": games})

@login_required
def my_likes(request):
    games = Game.objects.filter(liked_by__user=request.user).distinct().order_by("-rating", "name")
    return render(request, "games/my_list.html", {"title": "❤️ Mis me gusta", "games": games})

@require_GET
def search_suggest(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"items": []})

    games = (
        Game.objects.filter(Q(name__icontains=q) | Q(summary__icontains=q))
        .prefetch_related("platforms")
        .distinct()
        .order_by("-rating", "name")[:8]
    )

    items = []
    for g in games:
        items.append({
            "id": g.id,
            "name": g.name,
            "release_year": g.release_year,
            "rating": g.rating,
            "platforms": ", ".join(p.name for p in g.platforms.all()[:3]),
            "cover_url": g.cover_url,
            "url": reverse("game_detail", args=[g.id]),
        })

    return JsonResponse({"items": items})

def signup(request):
    if request.user.is_authenticated:
        return redirect("game_list")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # deja al usuario logueado al registrarse
            return redirect("game_list")
    else:
        form = SignUpForm()

    return render(request, "auth/signup.html", {"form": form})
