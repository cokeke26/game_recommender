from dataclasses import dataclass
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from games.models import Game

@dataclass
class RecommenderIndex:
    game_ids: List[int]
    tfidf_matrix: object
    vectorizer: TfidfVectorizer

_INDEX: RecommenderIndex | None = None
_LAST_COUNT: int = -1

def _game_text(game: Game) -> str:
    platforms = " ".join(p.name for p in game.platforms.all())
    genres = " ".join(g.name for g in game.genres.all())
    tags = " ".join(t.name for t in game.tags.all())
    return f"{game.name} {game.summary} {platforms} {genres} {tags}".strip()

def get_index() -> RecommenderIndex:
    global _INDEX, _LAST_COUNT

    # Rebuild simple cache if number of games changed
    count = Game.objects.count()
    if _INDEX is not None and _LAST_COUNT == count:
        return _INDEX

    games = list(Game.objects.all().prefetch_related("platforms", "genres", "tags"))
    texts = [_game_text(g) for g in games]
    ids = [g.id for g in games]

    vectorizer = TfidfVectorizer(stop_words=None, max_features=8000)
    tfidf = vectorizer.fit_transform(texts)

    _INDEX = RecommenderIndex(game_ids=ids, tfidf_matrix=tfidf, vectorizer=vectorizer)
    _LAST_COUNT = count
    return _INDEX

def similar_games(game_id: int, top_k: int = 10) -> List[Tuple[int, float]]:
    idx = get_index()
    if game_id not in idx.game_ids:
        return []

    i = idx.game_ids.index(game_id)
    sims = cosine_similarity(idx.tfidf_matrix[i], idx.tfidf_matrix).flatten()

    # ordenar por similitud desc, saltando el mismo juego
    scored = [(idx.game_ids[j], float(sims[j])) for j in range(len(idx.game_ids)) if idx.game_ids[j] != game_id]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
