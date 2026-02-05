# Makefile pour THOR
# Compatible: Linux, macOS, Windows (avec make installe)
# Usage: make [commande]

.PHONY: help docker-build docker-up docker-down docker-logs docker-cli docker-api docker-web clean

# Detecte l'OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    RM_CMD := del /s /q
    RMDIR_CMD := rmdir /s /q
else
    DETECTED_OS := $(shell uname -s)
    RM_CMD := rm -f
    RMDIR_CMD := rm -rf
endif

# Aide par defaut
help:
	@echo "========================================"
	@echo "  THOR - Commandes disponibles"
	@echo "  OS detecte: $(DETECTED_OS)"
	@echo "========================================"
	@echo ""
	@echo "Docker (recommande):"
	@echo "  make docker-build    - Construire les images Docker"
	@echo "  make docker-up       - Demarrer tous les services"
	@echo "  make docker-down     - Arreter tous les services"
	@echo "  make docker-logs     - Voir les logs"
	@echo "  make docker-api      - Demarrer uniquement l'API"
	@echo "  make docker-web      - Demarrer uniquement le frontend"
	@echo "  make docker-cli      - Lancer le CLI interactif"
	@echo "  make docker-restart  - Redemarrer les services"
	@echo ""
	@echo "Local (necessite Python + Node.js):"
	@echo "  make api             - Lancer l'API localement"
	@echo "  make web             - Lancer le frontend localement"
	@echo "  make install         - Installer les dependances"
	@echo "  make clean           - Nettoyer les fichiers temporaires"
	@echo ""
	@echo "Tests:"
	@echo "  make test-nlp        - Tester l'extraction NLP"
	@echo "  make test-pathfinding- Tester le pathfinding"
	@echo "  make test-api        - Tester l'API"

# ============== Docker ==============

docker-build:
	@echo "Construction des images Docker..."
	docker-compose build

docker-build-nocache:
	@echo "Reconstruction complete des images Docker..."
	docker-compose build --no-cache

docker-up:
	@echo "Demarrage des services..."
	docker-compose up -d
	@echo ""
	@echo "Services demarres!"
	@echo "  API:      http://localhost:8000"
	@echo "  Frontend: http://localhost:3000"

docker-down:
	@echo "Arret des services..."
	docker-compose down

docker-restart: docker-down docker-up

docker-logs:
	docker-compose logs -f

docker-api:
	docker-compose up -d api
	@echo "API disponible sur http://localhost:8000"

docker-web:
	docker-compose up -d web
	@echo "Frontend disponible sur http://localhost:3000"

docker-cli:
	docker-compose run --rm cli

docker-status:
	docker-compose ps

# ============== Local ==============

api:
	python api/app.py

web:
	cd web && npm run dev

install:
	pip install -e ".[nlp,stt,pathfinding]"
	cd web && npm install
	python -m spacy download fr_core_news_md

# ============== Clean ==============

clean:
ifeq ($(DETECTED_OS),Windows)
	@echo "Nettoyage Windows..."
	-for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
else
	@echo "Nettoyage Unix..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
endif

docker-clean:
	@echo "Nettoyage des images Docker..."
	docker-compose down --rmi local --volumes --remove-orphans

# ============== Tests ==============

test-nlp:
	docker-compose run --rm cli python -m src.cli.nlp extract --text "Je veux aller de Paris a Lyon"

test-pathfinding:
	docker-compose run --rm cli python -m src.cli.pathfinding find-route --origin Paris --destination Lyon

test-api:
ifeq ($(DETECTED_OS),Windows)
	@powershell -Command "Invoke-RestMethod -Uri http://localhost:8000/api/search -Method Post -ContentType 'application/json' -Body '{\"text\": \"Je veux aller de Paris a Lyon\"}'"
else
	curl -X POST http://localhost:8000/api/search \
		-H "Content-Type: application/json" \
		-d '{"text": "Je veux aller de Paris a Lyon"}'
endif
