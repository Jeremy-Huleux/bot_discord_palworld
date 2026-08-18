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

### Avec Docker

```bash
# 1. Configurer .env
cp .env.example .env
nano .env

# 2. Lancer avec docker-compose
docker-compose up -d

# 3. Vérifier les logs
docker-compose logs -f palworld-bot
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

### Mode local

```bash
source venv/bin/activate
python bot/main.py
```

Attendez le message:
```
==================================================
🤖 Palworld Bot démarré
Connecté en tant que : PalworldBot#1234
Serveur Discord ID : 123456789
==================================================
```

### Mode Docker

```bash
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f palworld-bot

# Arrêter
docker-compose down
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

### Le bot ne démarre pas

```
RuntimeError: DISCORD_TOKEN n'est pas défini
```

**Solution**: Vérifier que `.env` existe et contient `DISCORD_TOKEN`

### Les actualités ne s'envoient pas

```
⚠️ Aucun salon Discord configuré
```

**Solution**: Vérifier que `NEWS_CHANNEL_ID` est défini dans `.env`

### Web scraping Pocketpair échoue

```
❌ Erreur lecture article Pocketpair
```

**Solution**: Le site Pocketpair peut avoir changé son HTML. Vérifier les sélecteurs CSS dans `services/pocketpair.py`

### Google Translate échoue

```
⚠️ Erreur traduction
```

**Solution**: Google Translate peut être surchargé. Vérifier la connexion internet.

### Erreur base de données

```
sqlite3.OperationalError: disk I/O error
```

**Solution**: Vérifier que `/app/data/` est accessible en écriture (Docker) ou que `./data/` existe (local)

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
