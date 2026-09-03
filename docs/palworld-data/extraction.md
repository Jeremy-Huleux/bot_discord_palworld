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

`repak` extrait les assets Unreal `.uasset` et `.uexp`, mais ne les convertit pas
encore en JSON DataTables. La prochaine etape est d'evaluer un lecteur Unreal
compatible avec ces assets, puis de produire `normalized/` et `validated/`.

Ne jamais copier le PAK, les assets extraits ou les donnees proprietaires dans le
depot Git.
