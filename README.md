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

## 🔑 API RAWG (portadas de juegos)

Este proyecto utiliza la **API pública de RAWG** para obtener imágenes de portada de los juegos.

Por seguridad, la **API key no viene incluida en el repositorio** y debe configurarse como variable de entorno.

### Configurar la API key

#### Windows (PowerShell)
```powershell
setx RAWG_API_KEY "TU_API_KEY_AQUI"

## 📸 Créditos

Las imágenes y parte de los datos de juegos provienen de la API de  
[RAWG Video Games Database](https://rawg.io/)

