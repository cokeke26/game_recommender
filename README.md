# 🎮 GameHub – Recomendador de Juegos

Aplicación web hecha con **Django** que permite:
- Explorar un catálogo de juegos
- Buscar y filtrar por plataforma y género
- Guardar ⭐ favoritos y ❤️ me gusta
- Obtener recomendaciones similares
- Registro y login de usuarios
- UI moderna 

## 🚀 Stack
- Python 3.11
- Django
- Tailwind (CDN)
- SQLite (dev)
- Scikit-learn (recomendaciones)

## ▶️ Ejecutar en local
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_games
python manage.py runserver
