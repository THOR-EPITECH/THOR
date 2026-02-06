# Docker - THOR

Guide pour utiliser Docker avec le projet THOR.

**Compatible avec:** Linux, macOS (Intel + Apple Silicon M1/M2/M3), Windows

## Prerequis

- Docker >= 20.10
- Docker Compose >= 2.0
- ~10 GB d'espace disque (pour les modeles)

### Installation de Docker

**Windows:**
```
Installer Docker Desktop depuis https://www.docker.com/products/docker-desktop
Activer WSL2 si demande
```

**macOS:**
```bash
# Installer Docker Desktop depuis https://www.docker.com/products/docker-desktop
# Ou via Homebrew:
brew install --cask docker
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Redemarrer la session
```

## Demarrage rapide

```bash
# Build et lancement (premiere fois)
docker-compose up -d --build

# Lancement normal
docker-compose up -d

# Arreter
docker-compose down
```

**Services disponibles :**
- Frontend : http://localhost:3000
- API : http://localhost:8000

## Modeles pre-installes

Les images Docker contiennent les modeles suivants pre-telecharges :

### API (Dockerfile.api)

| Modele | Type | Taille | Usage |
|--------|------|--------|-------|
| `fr_core_news_md` | spaCy | ~50 MB | NLP - Extraction entites |
| `whisper-small` | OpenAI | ~500 MB | STT - Transcription |

### CLI (Dockerfile.cli)

| Modele | Type | Taille | Usage |
|--------|------|--------|-------|
| `fr_core_news_md` | spaCy | ~50 MB | NLP - Extraction entites |
| `fr_core_news_sm` | spaCy | ~15 MB | NLP - Version legere |
| `whisper-small` | OpenAI | ~500 MB | STT - Transcription |
| `whisper-tiny` | OpenAI | ~75 MB | STT - Tests rapides |
| `camembert-ner` | HuggingFace | ~450 MB | NLP - NER Transformers |

## Commandes

### Gestion des services

```bash
# Lancer tous les services (API + Frontend)
docker-compose up -d

# Lancer uniquement l'API
docker-compose up -d api

# Lancer uniquement le frontend
docker-compose up -d web

# Voir les logs
docker-compose logs -f

# Logs d'un service specifique
docker-compose logs -f api

# Arreter les services
docker-compose down

# Reconstruire les images
docker-compose build --no-cache
```

### Utiliser le CLI

```bash
# Lancer un shell interactif
docker-compose run --rm cli

# Extraire des entites d'un texte
docker-compose run --rm cli python -m src.cli.nlp extract --text "Je veux aller de Paris a Lyon"

# Evaluer un modele STT
docker-compose run --rm cli python -m src.cli.stt evaluate --dataset data/splits/test/test.jsonl --model whisper

# Evaluer un modele NLP
docker-compose run --rm cli python -m src.cli.nlp evaluate --dataset data/splits/test/test_nlp.jsonl --model spacy

# Trouver un itineraire
docker-compose run --rm cli python -m src.cli.pathfinding find-route --origin Paris --destination Lyon

# Pipeline complet (audio -> route)
docker-compose run --rm cli python -m src.cli.pipeline --audio data/raw/audio/sample.wav --pathfinding-model dijkstra
```

### Build individuel des images

```bash
# API
docker build -f docker/Dockerfile.api -t thor-api .

# Frontend
docker build -f docker/Dockerfile.web -t thor-web .

# CLI
docker build -f docker/Dockerfile.cli -t thor-cli .
```

## Architecture

```
                    +------------------+
                    |    Frontend      |
                    |   (Next.js)      |
                    |   port: 3000     |
                    +--------+---------+
                             |
                             | HTTP (docker network)
                             v
                    +--------+---------+
                    |      API         |
                    |    (Flask)       |
                    |   port: 8000     |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
         +--------+    +--------+    +----------+
         |  STT   |    |  NLP   |    |Pathfinder|
         |Whisper |    | spaCy  |    | Dijkstra |
         +--------+    +--------+    +----------+
```

## Volumes

Les volumes suivants sont montes pour le CLI :

| Host | Container | Description |
|------|-----------|-------------|
| `./data` | `/app/data` | Donnees d'entrainement et de test |
| `./results` | `/app/results` | Resultats des evaluations |
| `./models` | `/app/models` | Modeles entraines |
| `./configs` | `/app/configs` | Fichiers de configuration |

## Variables d'environnement

### API

| Variable | Description | Valeur par defaut |
|----------|-------------|-------------------|
| `FLASK_ENV` | Environment Flask | `production` |
| `PYTHONPATH` | Chemin Python | `/app` |

### Frontend

| Variable | Description | Valeur par defaut |
|----------|-------------|-------------------|
| `PYTHON_BACKEND_URL` | URL interne de l'API | `http://api:8000` |
| `NEXT_PUBLIC_API_URL` | URL publique de l'API | `http://localhost:8000` |

## Endpoints API

| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Page d'accueil avec liste des endpoints |
| GET | `/api/health` | Health check |
| POST | `/api/search` | Analyser un texte et trouver un itineraire |
| POST | `/api/route` | Trouver un itineraire entre deux villes |
| POST | `/api/transcribe` | Transcrire un audio en texte |
| POST | `/api/pipeline` | Pipeline complet (audio -> route) |
| GET | `/api/stations` | Liste des gares disponibles |
| POST | `/api/preload` | Precharger les modeles |

## Troubleshooting

### Port deja utilise

```bash
# Trouver le processus qui utilise le port (Windows PowerShell)
Get-NetTCPConnection -LocalPort 3000 | Select-Object OwningProcess
taskkill /F /PID <PID>

# Linux/macOS
lsof -i :3000
kill -9 <PID>
```

### Le frontend ne peut pas contacter l'API

```bash
# Verifier que l'API est demarree
docker-compose ps
curl http://localhost:8000/api/health
```

### Erreur de memoire avec les modeles

Augmentez la memoire allouee a Docker :
- Docker Desktop > Settings > Resources > Memory (recommande: 8 GB)

### Les modifications du code ne sont pas prises en compte

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Erreur de connexion ECONNREFUSED

Assurez-vous que le frontend utilise `http://api:8000` (nom du service Docker) pour les appels internes, pas `localhost`.
