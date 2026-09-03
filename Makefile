.PHONY: help build up down logs test shell restart clean

help:
	@echo "🐾 Palworld Bot - Commandes Docker"
	@echo ""
	@echo "  make build         Build l'image Docker"
	@echo "  make up            Démarre le bot"
	@echo "  make down          Arrête le bot"
	@echo "  make restart       Redémarre le bot"
	@echo "  make logs          Affiche les logs (Ctrl+C pour quitter)"
	@echo "  make test          Teste le parsing Pocketpair"
	@echo "  make shell         Entre dans le container (bash)"
	@echo "  make clean         Arrête et nettoie"
	@echo ""

build:
	@echo "🔨 Building Docker image..."
	docker-compose build

up:
	@echo "🚀 Démarrage du bot..."
	docker-compose up -d
	@echo "✅ Bot démarré!"
	@echo "   Voir les logs: make logs"

down:
	@echo "🛑 Arrêt du bot..."
	docker-compose down
	@echo "✅ Bot arrêté"

restart:
	@echo "🔄 Redémarrage du bot..."
	docker-compose restart
	@echo "✅ Bot redémarré"

logs:
	@echo "📋 Logs du bot (Ctrl+C pour quitter)..."
	docker-compose logs -f palworld-bot

test:
	@echo "🧪 Tests Pocketpair Parser..."
	docker-compose exec palworld-bot python bot/test_pocketpair.py

shell:
	@echo "🐚 Ouverture d'un shell dans le container..."
	docker-compose exec palworld-bot bash

clean:
	@echo "🧹 Nettoyage..."
	docker-compose down
	rm -rf ./data/*.db
	@echo "✅ Nettoyé"

install-env:
	@echo "📝 Création du fichier .env..."
	@if [ -f .env ]; then \
		echo "⚠️  .env existe déjà"; \
	else \
		cp .env.example .env; \
		echo "✅ .env créé (à partir de .env.example)"; \
		echo "   Éditer .env et ajouter vos valeurs:"; \
		echo "   nano .env"; \
	fi

status:
	@echo "📊 Statut du container..."
	docker-compose ps

version:
	@echo "📌 Versions installées:"
	docker-compose exec palworld-bot python --version
	docker-compose exec palworld-bot pip list | grep -E "discord|aiohttp|feedparser"
