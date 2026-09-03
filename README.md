# 🐾 Palworld Discord Bot

Bot Discord communautaire pour Palworld - Actualités, encyclopédie Palworld, monitoring serveur, et plus.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Lancement](#-lancement)
- [Commandes](#-commandes)
- [Architecture](#-architecture)
- [Palworld Data Engine](#-palworld-data-engine)
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

> **Principe de données** : les données de gameplay de l'encyclopédie ne seront
> activées qu'après extraction, validation et traçabilité depuis les fichiers
> locaux du serveur Palworld. Les wikis, APIs communautaires et données inventées
> ne sont pas des sources autorisées.

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
| `/pals <nom>` | Rechercher un Pal dans l'encyclopédie locale |
| `/breeding <parent1> <parent2>` | Calculer les résultats possibles de breeding |
| `/items <nom>` | Rechercher un objet dans le catalogue local |
| `/boss <nom>` | Rechercher un boss dans le catalogue local |
| `/server` | Statut, version, joueurs et uptime du serveur Palworld |
| `/players` | Joueurs actuellement connectés |

### Admin

| Commande | Description |
|----------|-------------|
| `/admin config` | Afficher la configuration non sensible |
| `/admin backup` | Créer une sauvegarde de la base SQLite |

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
│   ├── pocketpair.py       # Web scraping Pocketpair
│   └── server_monitor.py   # Monitoring A2S du serveur
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

### PALWORLD DATA ENGINE — ÉTUDE VALIDÉE

L'étude de faisabilité est terminée. L'implémentation démarrera après validation
du prototype d'extraction décrit dans la section suivante.

## 🧬 Palworld Data Engine

Cette architecture fera de la base de données du jeu la source de vérité de
l'encyclopédie Discord. Le projet n'embarque aucun fichier propriétaire du jeu.

### 1. Fichiers Palworld disponibles

Le serveur local contient actuellement :

- `Pal/Content/Paks/Pal-LinuxServer.pak` (environ 4,8 Go) ;
- `steamapps/appmanifest_2394010.acf` ;
- `Manifest_UFSFiles_Linux.txt` ;
- le binaire `PalServer-Linux-Shipping` ;
- les configurations `PalWorldSettings.ini` ;
- des sauvegardes `.sav`.

Les DataTables, DataAssets et fichiers JSON ne sont pas encore exportés hors du
PAK. Les sauvegardes représentent l'état d'une partie, pas les données statiques
complètes du jeu.

### 2. Version / Build détecté

Le build Steam installé est `24575149`. La version REST annoncée par le serveur
est `v1.0.3.101283`. Le PAK doit aussi être identifié par son hash SHA-256 lors
de chaque extraction.

### 3. Méthode d'extraction recommandée

```text
PAK en lecture seule
      ↓
Extraction Unreal
      ↓
data/raw/<game_build>/
      ↓
Normalisation
      ↓
Validation
      ↓
PostgreSQL staging
      ↓
Tests, comparaison et activation
```

L'extracteur travaillera toujours sur une copie ou un volume monté en lecture
seule, jamais sur les fichiers originaux du serveur.

### 4. Outil d'extraction recommandé

`PalDataKit` est retenu comme outil de normalisation et de vérification, pas comme
extracteur primaire. Sa documentation indique qu'il consomme déjà un dossier
`PalworldDB/data/raw`.

L'extracteur primaire reste à sélectionner après test sur le PAK local :

- `UnrealPak` correspondant à la version Unreal ;
- `repak` si compatible ;
- un extracteur Unreal capable de produire les `.uasset`.

### 5. Pourquoi cette méthode

Elle garantit que les valeurs viennent du build réellement installé :

```text
Fichiers du serveur → extraction locale → données brutes → données validées
```

PalDataKit pourra ensuite résoudre les identifiants et produire des datasets
dérivés, mais ses datasets publiés ne seront jamais utilisés comme source
primaire.

### 6. Données réellement disponibles

À ce stade, seules la version, le build, les hashes, la configuration et les
interfaces runtime sont accessibles directement. Les données suivantes doivent
être recherchées dans les exports du PAK :

- **Pals** : paramètres, types, statistiques, travail, skills, passifs, drops ;
- **Items** : paramètres, catégories, descriptions et références ;
- **Skills / passifs** : puissance, élément, cooldowns et effets ;
- **Boss** : paramètres, niveaux, récompenses et références de zones ;
- **Recipes / technology** : matériaux, stations et déblocages ;
- **Drops** : loot tables et références d'items ;
- **Locations / spawns** : zones, positions et règles d'apparition ;
- **Breeding** : rangs, combinaisons, exceptions et règles spéciales.

Une donnée non présente dans le build sera déclarée indisponible, jamais estimée.

### 7. Données directement extraites

Le premier prototype devra produire les exports bruts et un manifest contenant
les tables, lignes, fichiers sources et hashes. Aucun gameplay ne sera importé
avant cette étape.

### 8. Données dérivables

Les index de recherche, relations Pal/type, statistiques par niveau, résultats de
breeding, graphes `/breed-to` et changelogs pourront être calculés à partir des
données validées. Ils porteront la provenance `DERIVED_FROM_GAME_DATA` ou
`CALCULATED_FROM_GAME_DATA`.

### 9. Données impossibles à obtenir depuis les fichiers

Certaines formules ou logiques peuvent rester indisponibles : capture complète,
comportements natifs, valeurs dynamiques, assets chiffrés ou logique uniquement
exécutée par le moteur. Le bot affichera alors :

```text
Donnée non disponible dans les fichiers du jeu analysés.
```

### 10. Architecture de la pipeline

```text
palworld
      ↓ volume lecture seule
palworld-data-updater
      ↓
raw → normalized → validated
      ↓
PostgreSQL staging → tests → PostgreSQL active
```

L'extraction, la normalisation et l'import ne doivent jamais bloquer le bot
Discord.

### 11. Architecture PostgreSQL

Le futur schéma sera relationnel et versionné, avec notamment :

`game_versions`, `data_sources`, `localizations`, `pals`, `pal_stats`,
`pal_work_suitabilities`, `skills`, `passive_skills`, `items`, `recipes`,
`technology`, `drops`, `spawn_locations`, `bosses`, `breeding_combinations`,
`breeding_rules` et `data_changes`.

Les commandes ne connaîtront jamais les tables SQL : elles passeront par des
repositories puis des services métier.

### 12. Architecture Docker

L'architecture cible est :

```text
palworld ──(lecture seule)──> palworld-data-updater
                                                   ↓
                                            palworld-db
                                                   ↑
                                            palworld-bot
```

Un conteneur d'extraction séparé est recommandé pour isoler les traitements
lourds et protéger le serveur de jeu.

### 13. Versioning

Chaque extraction conservera :

```text
game_version, game_build, extraction_date, extractor_version,
dataset_hash, source_pak_hash, status
```

Les anciennes versions resteront disponibles et la version active ne sera jamais
écrasée directement.

### 14. Détection des mises à jour

La détection utilisera d'abord le `buildid` Steam, puis le hash du PAK. La version
REST et le binaire seront des informations secondaires. Aucun build inchangé ne
sera réimporté inutilement.

### 15. Validation des nouvelles données

Les contrôles porteront sur les identifiants, doublons, types, références
étrangères, recettes, drops, breeding, localisations, tables attendues et
provenance. Un échec provoquera `IMPORT REFUSÉ` et conservera l'ancienne version.

### 16. Rollback

Chaque migration commencera par une sauvegarde. La nouvelle version sera importée
en staging et activée uniquement après les tests. Un échec laissera la version
active précédente inchangée.

### 17. Calculateur de breeding

Le calculateur actuel basé sur `breeding_power` est provisoire. Le calculateur
final reposera exclusivement sur les règles extraites du jeu, notamment les
combinaisons uniques, exceptions, genres et Pals spéciaux.

### 18. Commandes Discord rendues possibles

```text
/pal  /pals  /breed  /breed-to  /items  /boss
/passives  /skill  /recipe  /drops  /locations
/stats  /partnerskill  /work
```

Chaque réponse affichera le build et la provenance des données lorsque ces
informations seront disponibles.

### 19. Sécurité / propriété des fichiers

Le dépôt ne contiendra jamais de `.pak`, `.uasset`, archives du jeu ou dataset
propriétaire brut. Les fichiers du serveur seront montés en lecture seule et les
seuls artefacts versionnés seront le code, les schémas, les scripts, les tests,
les manifests et les hashes.

### 20. Risques techniques

- compatibilité du PAK Linux avec l'extracteur choisi ;
- chiffrement ou compression des assets ;
- tables absentes du build dédié ;
- changements de structure entre builds ;
- volume et durée d'une extraction complète ;
- données de breeding ou logique native non exportables ;
- migration PostgreSQL encore à construire.

### 21. Plan d'implémentation

1. Prototype d'ouverture et d'extraction du PAK.
2. Conservation des données brutes et manifest de provenance.
3. Normalisation et validation indépendante.
4. Schéma PostgreSQL et import staging.
5. Comparaison, changelog et rollback.
6. Repositories et services métier.
7. Breeding basé sur les règles extraites.
8. Updater Docker et notification Discord après activation.

### 22. Première implémentation recommandée

La prochaine étape est un prototype non destructif qui tente d'ouvrir le PAK,
identifie les tables disponibles et produit uniquement `data/raw/<build>/` ainsi
qu'un rapport. Aucune commande Discord ni base active ne sera reliée aux données
tant que l'extraction et la validation ne sont pas démontrées.

Le prototype est documenté dans
[docs/palworld-data/extraction.md](docs/palworld-data/extraction.md).

### PHASE 1: Stabilisation (TERMINÉE)
- ✅ Audit complet
- ✅ Correction bug résumé Pocketpair
- 🔧 Nettoyage doublons
- 📝 Documentation (.env.example, README)
- 🔧 Logging structuré
- **Durée**: 2-3 jours

### PHASE 2: Architecture modulaire (TERMINÉE)
- ✅ Refactorisation config/logging
- ✅ Dataclasses pour modèles
- ✅ Tests unitaires
- **Durée**: 1-2 jours

### PHASE 3: News robustes (TERMINÉE)
- ✅ Intégrer résumé + image Pocketpair
- ✅ Cache traduction
- ✅ Retry exponentiel
- **Durée**: 1 jour

### PHASE 4: Monitoring serveur (TERMINÉE)
- ✅ `/server` command
- ✅ `/players` command
- ✅ Analytics uptime
- **Durée**: 2-3 jours

### PHASE 5: Encyclopédie, Breeding, Admin (EN COURS)
- ✅ Recherche locale `/pals`
- ✅ Catalogue local `/items` et `/boss`
- ✅ Calculateur provisoire `/breeding`
- ✅ Commandes `/admin config` et `/admin backup`
- ⏳ Extraction depuis les fichiers réels du serveur
- ⏳ Remplacement des données provisoires par les données validées

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

**Dernière mise à jour**: 2026-09-03
**Statut**: 🚧 En développement (étude Data Engine terminée, prototype d'extraction à valider)
