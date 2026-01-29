import os
import time
import requests

from django.core.management.base import BaseCommand
from django.db.models import Q

from games.models import Game

RAWG_BASE = "https://api.rawg.io/api"


class Command(BaseCommand):
    help = "Completa Game.cover_url usando RAWG (background_image) buscando por nombre."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=50, help="Cantidad máxima a procesar")
        parser.add_argument("--sleep", type=float, default=0.25, help="Pausa entre requests (segundos)")
        parser.add_argument("--overwrite", action="store_true", help="Sobrescribir aunque ya exista cover_url")

    def handle(self, *args, **opts):
        api_key = os.getenv("RAWG_API_KEY")
        if not api_key:
            self.stderr.write("Falta RAWG_API_KEY en variables de entorno.")
            return

        limit = opts["limit"]
        sleep_s = opts["sleep"]
        overwrite = opts["overwrite"]

        qs = Game.objects.all().order_by("id")
        if not overwrite:
            qs = qs.filter(Q(cover_url="") | Q(cover_url__isnull=True))

        games = list(qs[:limit])
        if not games:
            self.stdout.write("No hay juegos para actualizar.")
            return

        ok = 0
        miss = 0

        for game in games:
            name = (game.name or "").strip()
            if not name:
                continue

            params = {
                "key": api_key,
                "search": name,
                "search_precise": "true",
                "page_size": 5,
            }

            try:
                r = requests.get(f"{RAWG_BASE}/games", params=params, timeout=15)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                self.stderr.write(f"[ERROR] {name}: {e}")
                time.sleep(sleep_s)
                continue

            results = data.get("results") or []
            chosen = None

            # heurística simple: primer resultado cuyo nombre coincide (case-insensitive)
            for it in results:
                if (it.get("name") or "").strip().lower() == name.lower():
                    chosen = it
                    break
            if not chosen and results:
                chosen = results[0]

            if not chosen:
                miss += 1
                self.stdout.write(f"[MISS] {name}")
                time.sleep(sleep_s)
                continue

            img = (chosen.get("background_image") or "").strip()
            if not img:
                miss += 1
                self.stdout.write(f"[NOIMG] {name}")
                time.sleep(sleep_s)
                continue

            game.cover_url = img
            game.save(update_fields=["cover_url"])
            ok += 1
            self.stdout.write(f"[OK] {name} -> {img}")

            time.sleep(sleep_s)

        self.stdout.write(f"\nListo. OK={ok} | MISS/NOIMG={miss}")
