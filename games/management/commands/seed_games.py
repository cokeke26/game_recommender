import csv
from django.core.management.base import BaseCommand
from games.models import Game, Platform, Genre, Tag

SEP = "|"

class Command(BaseCommand):
    help = "Importa juegos desde games/data/games_mvp.csv"

    def handle(self, *args, **options):
        path = "games/data/games_mvp.csv"

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                game, _ = Game.objects.get_or_create(
                    name=row["name"].strip(),
                    defaults={
                        "summary": (row.get("summary") or "").strip(),
                        "release_year": int(row["release_year"]) if row.get("release_year") else None,
                        "rating": float(row["rating"]) if row.get("rating") else None,
                        "cover_url": (row.get("cover_url") or "").strip(),
                    }
                )

                # Si ya existía, actualiza campos básicos
                game.summary = (row.get("summary") or "").strip()
                game.release_year = int(row["release_year"]) if row.get("release_year") else None
                game.rating = float(row["rating"]) if row.get("rating") else None
                game.cover_url = (row.get("cover_url") or "").strip()
                game.save()

                # Many-to-many: platforms, genres, tags
                platforms = [p.strip() for p in row.get("platforms", "").split(SEP) if p.strip()]
                genres = [g.strip() for g in row.get("genres", "").split(SEP) if g.strip()]
                tags = [t.strip() for t in row.get("tags", "").split(SEP) if t.strip()]

                for p in platforms:
                    obj, _ = Platform.objects.get_or_create(name=p)
                    game.platforms.add(obj)

                for g in genres:
                    obj, _ = Genre.objects.get_or_create(name=g)
                    game.genres.add(obj)

                for t in tags:
                    obj, _ = Tag.objects.get_or_create(name=t)
                    game.tags.add(obj)

                count += 1

        self.stdout.write(self.style.SUCCESS(f"Importados/actualizados: {count} juegos"))
