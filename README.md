# 🐾 Palworld Discord Bot

Bot Discord communautaire pour Palworld - Actualités, encyclopédie Palworld, monitoring serveur, et plus.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Lancement](#-lancement)
- [Commandes](#-commandes)
- [Architecture](#-architecture)
- [Roadmap](#-roadmap)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Fonctionnalités

### Actuellement implémentées ✅

- 📰 **Actualités Palworld**
  - Récupération automatique Steam + Pocketpair
  - Catégorisation (patchs, événements, news)
  - Traduction française
  - Envoi Discord avec embeds

- 🤖 **Bot Discord**
  - Slash Commands modernes
  - Architecture modulaire (Cogs)
  - Vérification automatique (5 min)
  - Détection des grandes mises à jour

### En développement 🚧

Voir [Roadmap](#-roadmap) pour le planning complet.

---

## 🚀 Installation

### Prérequis

- Python 3.12+
- Docker & Docker Compose (optionnel)
- Discord Bot Token (créé sur https://discord.com/developers/applications)

### Sans Docker (Local)

```bash
# 1. Cloner le projet
git clone https://github.com/zaelos/palworld-bot.git
cd palworld-bot

# 2. Créer l'environnement virtuel
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs
nano .env

# 5. Lancer le bot
python bot/main.py
```

### Avec Docker (Recommandé) ⭐

**Avec Makefile (plus simple):**
```bash
make install-env    # Créer .env à partir de .env.example
# Éditer .env avec vos valeurs
nano .env

make build          # Builder l'image
make up             # Démarrer le bot
make logs           # Voir les logs
```

**Ou commandes Docker directes:**
```bash
# 1. Configurer .env
cp .env.example .env
nano .env  # Éditer avec vos valeurs

# 2. Builder l'image Docker
docker-compose build

# 3. Démarrer le bot en arrière-plan
docker-compose up -d

# 4. Vérifier les logs en direct
docker-compose logs -f palworld-bot

# 5. Arrêter le bot
docker-compose down

# 6. Redémarrer
docker-compose restart
```

### Tests dans Docker

```bash
# Voir les logs du bot
make logs
# ou: docker-compose logs -f palworld-bot

# Exécuter les tests Pocketpair DANS Docker
make test
# ou: docker-compose exec palworld-bot python bot/test_pocketpair.py

# Entrer dans le container (shell)
make shell
# ou: docker-compose exec palworld-bot bash

# Vérifier les versions
make version
# ou: docker-compose exec palworld-bot pip list | grep discord
```

---

## ⚙️ Configuration

### Variables d'environnement

Voir [.env.example](.env.example) pour la liste complète.

#### Essentielles

| Variable | Description | Exemple |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Token du bot Discord | `MTk4NjIyNDgzNTk...` |
| `DISCORD_GUILD_ID` | ID du serveur Discord | `123456789` |
| `NEWS_CHANNEL_ID` | Salon pour les actualités | `987654321` |

#### Optionnelles

| Variable | Description | Défaut |
|----------|-------------|--------|
| `PATCH_NOTES_CHANNEL_ID` | Salon pour les patchs | `NEWS_CHANNEL_ID` |
| `EVENTS_CHANNEL_ID` | Salon pour les événements | `NEWS_CHANNEL_ID` |
| `PALWORLD_ROLE_ID` | Rôle @mention pour grands patchs | Non configuré |
| `DEBUG_MODE` | Mode debug (logs détaillés) | `false` |

### Obtenir les IDs Discord

1. **Activer Mode Développeur**: Discord → Utilisateur → Paramètres → Avancés → Mode Développeur
2. **Guild ID**: Clic droit serveur → Copier l'ID serveur
3. **Channel ID**: Clic droit salon → Copier l'ID du canal
4. **Role ID**: Clic droit rôle → Copier l'ID du rôle

---

## 🎯 Lancement

### Mode Docker (RECOMMANDÉ) ⭐

```bash
docker-compose build
docker-compose up -d
docker-compose logs -f palworld-bot
```

Attendez le message:
```
[2026-08-18 15:30:45] INFO     | palworld_bot | ============================================================
[2026-08-18 15:30:45] INFO     | palworld_bot | 🤖 PALWORLD BOT DÉMARRÉ AVEC SUCCÈS
[2026-08-18 15:30:45] INFO     | palworld_bot | Connecté en tant que : PalworldBot#1234
[2026-08-18 15:30:45] INFO     | palworld_bot | Serveur Discord ID : 123456789
[2026-08-18 15:30:45] INFO     | palworld_bot | ============================================================
```

**Avantages Docker:**
- ✅ Environnement reproductible (Python 3.12 garanti)
- ✅ Isolation du système
- ✅ Compatible production (AWS, VPS, Heroku, etc)
- ✅ Logs centralisés
- ✅ Redémarrage automatique
- ✅ Volume persistant pour `/app/data`

### Mode local (Développement)

```bash
source venv/bin/activate
python bot/main.py
```

Attendez le message:
```
[2026-08-18 15:30:45] INFO     | palworld_bot | ============================================================
[2026-08-18 15:30:45] INFO     | palworld_bot | 🤖 PALWORLD BOT DÉMARRÉ AVEC SUCCÈS
```

---

## 🎮 Commandes

### Utilisateur

| Commande | Description |
|----------|-------------|
| `/ping` | Vérifier que le bot fonctionne |
| `/pals <nom>` | Rechercher un Pal (prochainement) |
| `/items <nom>` | Rechercher un objet (prochainement) |
| `/boss` | Liste des boss (prochainement) |
| `/server` | Statut du serveur Palworld (prochainement) |
| `/players` | Joueurs connectés (prochainement) |

### Admin

| Commande | Description |
|----------|-------------|
| `/admin config` | Configurer le bot (prochainement) |
| `/admin backup` | Statut sauvegarde (prochainement) |

---

## 🏗️ Architecture

### Structure du projet

```
bot/
├── main.py                  # Point d'entrée
├── cogs/
│   └── news.py             # Actualités (implémenté)
├── services/
│   ├── database.py         # Base de données SQLite
│   ├── news_service.py     # Agrégation news
│   └── pocketpair.py       # Web scraping Pocketpair
└── data/
    └── news.db             # Base de données (créée auto)
```

### Stack technique

- **Framework**: discord.py 2.x
- **Async**: aiohttp + asyncio
- **Base de données**: SQLite3
- **Traduction**: Google Translate (deep-translator)
- **Web scraping**: BeautifulSoup4 + feedparser

### Flux d'actualités

```
Steam RSS + Pocketpair Web Scraping
        ↓
   NewsService
        ↓
  Traduction FR
        ↓
  Base de données (deduplication)
        ↓
  Discord Embed
        ↓
  Envoi automatique (5 min)
```

---

## 🗺️ Roadmap

### PHASE 1: Stabilisation (EN COURS)
- ✅ Audit complet
- ✅ Correction bug résumé Pocketpair
- 🔧 Nettoyage doublons
- 📝 Documentation (.env.example, README)
- 🔧 Logging structuré
- **Durée**: 2-3 jours

### PHASE 2: Architecture modulaire
- Refactorisation config/logging
- Dataclasses pour modèles
- Tests unitaires
- **Durée**: 1-2 jours

### PHASE 3: News robustes
- Intégrer résumé + image Pocketpair
- Cache traduction
- Retry exponential
- **Durée**: 1 jour

### PHASE 4: Monitoring serveur
- `/server` command
- `/players` command
- Analytics uptime
- **Durée**: 2-3 jours

### PHASE 5+: Encyclopédie, Breeding, Admin
Voir l'audit complet pour détails.

**Estimation totale**: 15-20 jours pour toutes les phases

---

## 🛠️ Troubleshooting

### Erreurs Docker

#### Build échoue
```
ERROR: Service 'palworld-bot' failed to build
```

**Solution**: 
```bash
docker-compose build --no-cache
```

#### Le container ne démarre pas
```
docker-compose up -d
# Puis: docker-compose logs palworld-bot
```

Vérifier les erreurs dans les logs. Causes courantes:
- `.env` manquant ou mal configuré
- Port 8211 (Palworld API) déjà utilisé
- Permissions `/data/` problématiques

**Solution**:
```bash
# Vérifier que .env existe
ls -la .env

# Reconstruire
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Voir les logs
docker-compose logs -f palworld-bot
```

#### Permission denied on /app/data
```
PermissionError: [Errno 13] Permission denied: '/app/data/news.db'
```

**Solution**:
```bash
# Le volume ./data/ doit être accessible en écriture
sudo chown -R $USER:$USER ./data/
chmod -R 755 ./data/

# Puis redémarrer
docker-compose restart
```

#### Port déjà utilisé
```
ERROR: for palworld-bot Cannot start service palworld-bot: driver failed programming external connectivity
```

**Solution**:
```bash
# Arrêter les autres containers
docker-compose down

# Ou utiliser un port différent (voir docker-compose.yml)
```

### Erreurs d'exécution

#### Le bot ne démarre pas

```
[ERROR] RuntimeError: DISCORD_TOKEN n'est pas défini.
```

**Solution**: 
```bash
# Vérifier .env
cat .env | grep DISCORD_TOKEN

# Reconfigurer
cp .env.example .env
nano .env
docker-compose restart
```

#### Les actualités ne s'envoient pas

```
[WARNING] Aucun salon Discord configuré
```

**Solution**: Vérifier que `NEWS_CHANNEL_ID` est défini dans `.env` avec un ID numérique valide:
```bash
docker-compose exec palworld-bot python -c "import os; print(os.getenv('NEWS_CHANNEL_ID'))"
```

#### Web scraping Pocketpair échoue

```
[ERROR] Erreur lecture article Pocketpair: ...
```

**Cause**: Le site Pocketpair peut avoir changé son HTML/structure

**Solution**: 
```bash
# Tester directement dans Docker
docker-compose exec palworld-bot python bot/test_pocketpair.py

# Vérifier les sélecteurs CSS dans services/pocketpair.py
```

#### Google Translate échoue

```
[WARNING] Erreur traduction Steam: ...
```

**Cause**: Google Translate peut être surchargé ou inaccessible

**Solution**:
```bash
# Vérifier la connectivité internet du container
docker-compose exec palworld-bot curl https://translate.google.com

# Vérifier les logs détaillés
docker-compose logs -f palworld-bot | grep -i traduc
```

#### Erreur base de données

```
[ERROR] sqlite3.OperationalError: disk I/O error
```

**Solution**:
```bash
# Vérifier que le volume est accessible
docker-compose exec palworld-bot ls -la /app/data/

# Vérifier les permissions
docker-compose exec palworld-bot touch /app/data/test.txt && rm /app/data/test.txt

# Recréer la DB si besoin
docker-compose exec palworld-bot rm /app/data/news.db
docker-compose restart
```

### Debug

#### Voir les logs en temps réel
```bash
docker-compose logs -f palworld-bot
```

#### Déboguer dans le container
```bash
# Entrer dans le container
docker-compose exec palworld-bot bash

# À l'intérieur du container
python -c "from logger import logger; logger.info('Test')"
python bot/test_pocketpair.py
pip list
```

#### Vérifier les variables d'environnement
```bash
docker-compose exec palworld-bot env | grep -E 'DISCORD|PALWORLD'
```

#### Vérifier la connectivité réseau
```bash
docker-compose exec palworld-bot ping discord.com
docker-compose exec palworld-bot curl -I https://www.pocketpair.jp/
```

---

## 📚 Documentation complète

Pour plus de détails sur l'architecture et le développement, voir:
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) (prochainement)
- [CONTRIBUTING.md](./CONTRIBUTING.md) (prochainement)
- [Audit technique complet](./docs/AUDIT.md) (prochainement)

---

## 🤝 Contribution

Les contributions sont bienvenues! Voir [CONTRIBUTING.md](./CONTRIBUTING.md) pour les directives.

---

## 📄 Licence

À définir

---

## 🔗 Liens utiles

- [Discord Developer Portal](https://discord.com/developers/applications)
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Palworld Official Site](https://www.pocketpair.jp/en/)
- [Steam Palworld](https://store.steampowered.com/app/1623730/Palworld/)

---

**Dernière mise à jour**: 2026-08-18
**Statut**: 🚧 En développement (Phase 1)
