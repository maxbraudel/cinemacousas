# Structure du Projet - Cinemacousas Admin

## 📁 Organisation des fichiers

Après nettoyage et réorganisation, voici la structure optimisée du projet :

### 🎯 Fichiers principaux (Administration)
```
Cinemacousas/
├── server_admin.py          # ⭐ Serveur d'administration (PRINCIPAL)
├── modele.py               # 🗄️ Modèle de données et BDD
├── requirements.txt        # 📦 Dépendances Python
├── .env                    # ⚙️ Configuration (à créer/modifier)
├── .env.example           # 📋 Template de configuration
├── start_admin.sh         # 🚀 Script de démarrage rapide
└── README.md              # 📖 Documentation principale
```

### 🎨 Interface et ressources
```
├── templates/             # 🖼️ Templates HTML admin uniquement
│   ├── admin.html         #   Interface d'administration
│   ├── base.html          #   Template de base
│   └── login.html         #   Page de connexion
└── static/               # 🎨 Fichiers statiques (CSS, JS, images)
    ├── css/
    ├── js/
    └── img/
```

### 📂 Fonctionnalités utilisateur (archivées)
```
└── user/                 # 👥 Code utilisateur déplacé (référence)
    ├── server.py          #   Ancien serveur principal
    ├── server_full.py     #   Serveur complet (user + admin)
    ├── validate_cleanup.py #   Script de validation
    └── templates/         #   Templates utilisateur
        ├── home.html
        ├── movies.html
        ├── booking_*.html
        └── ...
```

### 📚 Documentation et conception
```
├── docs/                 # 📋 Documentation et conception
│   ├── V1.sql, V2.sql... #   Scripts SQL de création
│   ├── MCD.png           #   Modèle conceptuel
│   ├── *.pdf             #   Documentations techniques
│   └── *.mwb             #   Fichiers MySQL Workbench
└── old/                  # 🗂️ Anciens fichiers de développement
```

### ⚙️ Configuration et environnement
```
├── .vscode/              # 🔧 Configuration VS Code
├── cinemacousas_env/     # 🐍 Environnement Python
├── .gitignore           # 🚫 Fichiers ignorés par Git
└── ENV_IMPLEMENTATION.md # 📄 Doc configuration environnement
```

## 🔄 Changements effectués

### ✅ Fichiers déplacés
- `server.py` → `user/server.py` (ancien serveur principal)
- `validate_cleanup.py` → `user/validate_cleanup.py` (validation)
- `workspace/` → `docs/` (documentation et conception)

### ✅ Fichiers conservés à la racine
- `server_admin.py` : Serveur principal d'administration
- `modele.py` : Modèle de données (utilisé par l'admin)
- Configuration : `.env`, `requirements.txt`, `README.md`
- Interface : `templates/`, `static/`

### ✅ Avantages de cette organisation

1. **Racine propre** : Seuls les fichiers essentiels pour l'administration
2. **Séparation claire** : Admin vs Utilisateur vs Documentation
3. **Déploiement simple** : Copier la racine suffit pour l'admin
4. **Maintenance** : Structure logique et documentée

## 🚀 Utilisation

### Pour l'administration (usage principal)
```bash
# Depuis la racine du projet
./start_admin.sh
# ou
python server_admin.py
```

### Pour tester la version complète
```bash
cd user/
python server_full.py
```

### Pour la documentation
```bash
# Scripts SQL dans docs/
# Modèles de conception dans docs/
# PDFs explicatifs dans docs/
```

## 📊 Statistiques finales

- **Fichiers admin** : 7 fichiers essentiels à la racine
- **Fichiers utilisateur** : Archivés dans `user/` (4 fichiers)
- **Documentation** : Organisée dans `docs/` (12 fichiers)
- **Configuration** : Externalisée dans `.env`

**Résultat :** Structure professionnelle, maintenable et déployable ! ✨
