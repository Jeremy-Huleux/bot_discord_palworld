# Prototype d'extraction Palworld

Ce prototype lit les fichiers locaux du serveur Palworld sans les modifier et
produit un manifest de provenance. Les assets extraits restent hors du dépôt.

## Prérequis

- serveur Palworld installé localement ;
- PAK du serveur accessible en lecture ;
- binaire `repak` Linux v0.2.3 ou version compatible.

## Probe sans extraction

```bash
python tools/palworld_data_probe.py \
  --pak /srv/palworld/palworld/Pal/Content/Paks/Pal-LinuxServer.pak \
  --repak /chemin/vers/repak \
  --steam-manifest /srv/palworld/palworld/steamapps/appmanifest_2394010.acf \
  --output /tmp/palworld-data/raw
```

## Extraction ciblee

Ajouter `--extract` a la commande precedente. Le prototype extrait uniquement
les familles Character, Item, PassiveSkill, PartnerSkill, Technology, Text et
RaidBoss, ainsi que les textes EN et FR.

```text
/tmp/palworld-data/raw/<build>/
├── manifest.json
└── pak/
    └── Pal/Content/...
```

Le fichier `manifest.json` conserve le build, la date, la version de l'extracteur,
le hash SHA-256 du PAK, la taille du fichier, les informations PAK et la liste des
entrees selectionnees.

## Limites actuelles

`repak` extrait les assets Unreal `.uasset` et `.uexp`. Le projet utilise ensuite
UAssetAPI 1.1.0 pour décoder les DataTables avec `EngineVersion.VER_UE5_1` et
produire les JSON normalisables. Les données générées restent hors du dépôt.

## Résultat du prototype

Le PAK du serveur a été lu avec `repak v0.2.3` :

- format PAK `V11` ;
- index non chiffré ;
- compression Oodle ;
- build Steam `24575149` ;
- 372 entrées candidates dans les familles sélectionnées ;
- 356 fichiers extraits dans le staging ;
- environ 49 Mo extraits.

Les familles suivantes sont présentes dans le PAK :

- `DT_PalMonsterParameter` ;
- `DT_PalCombiUnique` ;
- `DT_PalDropItem` ;
- `DT_ItemDataTable` ;
- `DT_ItemRecipeDataTable` ;
- `DT_PassiveSkill_Main` ;
- `DT_PartnerSkill` ;
- `DT_PalRaidBoss` ;
- tables de textes EN et FR.

Ces résultats prouvent que l'extraction primaire est faisable. Ils ne prouvent
pas que toutes les propriétés possibles seront disponibles dans chaque build ;
le prototype actuel décode toutefois les DataTables ciblées sans fichier `.usmap`.

## Résultat du décodage

Sur le build `24575149`, le convertisseur a produit 101 JSON à partir des assets
extraits, sans échec. Les tables prioritaires contiennent notamment :

| Table | Lignes |
| --- | ---: |
| `DT_PalMonsterParameter` | 737 |
| `DT_PalCombiUnique` | 259 |
| `DT_PalDropItem` | 1046 |
| `DT_PassiveSkill_Main` | 574 |
| `DT_PartnerSkillParameter` | 667 |
| `DT_ItemRecipeDataTable` | 1 table décodée |
| `DT_TechnologyRecipeUnlock` | 548 |

Le projet .NET du convertisseur est dans `tools/uasset_exporter/`. Il ne doit
jamais recevoir un PAK en écriture et ses sorties doivent rester dans un staging
externe tel que `/tmp/palworld-data/`.

## Normalisation et validation des Pals

Le script `tools/normalize_pal_data.py` transforme la table brute exportée en un
dataset `pals.json` sans compléter les champs absents. Chaque ligne conserve son
identifiant interne, son build, son asset source et la provenance `GAME_DATA`.

```bash
python tools/normalize_pal_data.py \
  --input-root /tmp/palworld-data/normalized/24575149 \
  --output /tmp/palworld-data/normalized/24575149/pals.json \
  --build 24575149

python tools/validate_pal_data.py \
  /tmp/palworld-data/normalized/24575149/pals.json
```

Sur le build `24575149`, la normalisation produit 735 Pals et la validation
réussit. Les types sont ceux présents dans le dataset (`Normal`, `Fire`, `Water`,
`Ice`, `Leaf`, `Earth`, `Electricity`, `Dark`, `Dragon`).

Ne jamais copier le PAK, les assets extraits ou les donnees proprietaires dans le
depot Git.
