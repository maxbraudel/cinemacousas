# Cinemacousas - Interface d'Administration de Cinéma

## ⚡ Démarrage ultra-rapide

```bash
# Option 1: Script automatique (recommandé)
./start_admin.sh

# Option 2: Manuel
source cinemacousas_env/bin/activate
python server_admin.py
```

**Interface :** http://localhost:5003 | **Login :** admin / n'importe quoi

## 🔧 Configuration

Le projet utilise un fichier `.env` pour la configuration. Copiez `.env.example` vers `.env` et modifiez selon vos besoins :

```bash
cp .env.example .env
# Éditez .env avec vos paramètres
```

### Variables principales :
- `FLASK_PORT` : Port du serveur (défaut: 5003)
- `FLASK_DEBUG` : Mode debug (défaut: True)
- `ADMIN_USERNAME` : Nom d'utilisateur admin (défaut: admin)
- `ADMIN_PASSWORD_REQUIRED` : Mot de passe requis (défaut: False)
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` : Configuration base de données
- `MAX_POSTER_SIZE_MB` : Taille max des affiches (défaut: 5MB)

---

## 🚀 Démarrage rapide

```bash
# 1. Activer l'environnement virtuel (déjà configuré)
source cinemacousas_env/bin/activate

# 2. Lancer l'interface d'administration
python3 server_admin.py
```

L'interface d'administration sera accessible à : `http://localhost:5003`

**Connexion administrateur :** `admin` / `n'importe quel mot de passe`

**Important :** Utilisez toujours l'environnement virtuel `cinemacousas_env` et non `.venv` pour éviter les problèmes de dépendances.

## Description
Interface d'administration Flask pour la gestion des films, salles, séances et réservations de cinéma.

**Note :** Cette version contient uniquement les fonctionnalités d'administration. Les fonctionnalités utilisateur (réservation publique, navigation des films) ont été déplacées dans le dossier `user/` pour garder une interface d'administration propre et autonome.

## Prérequis
- Python 3.8 ou supérieur
- MySQL/MariaDB server
- Un navigateur web moderne

## Installation

### 1. Cloner ou télécharger le projet
```bash
cd /chemin/vers/votre/dossier
# Le projet est déjà présent dans ce répertoire
```

### 2. Utiliser l'environnement virtuel

**L'environnement virtuel `cinemacousas_env` est déjà créé et configuré.**

Pour l'activer :
```bash
# Sur macOS/Linux
source cinemacousas_env/bin/activate

# Sur Windows
cinemacousas_env\Scripts\activate
```

Si vous devez recréer l'environnement virtuel :
```bash
python3 -m venv cinemacousas_env
source cinemacousas_env/bin/activate  # Sur macOS/Linux
pip install -r requirements.txt
```

### 3. Installer les dépendances (si nécessaire)

**Les dépendances sont déjà installées dans `cinemacousas_env`.**

Si vous devez les réinstaller :
```bash
# Assurez-vous que l'environnement virtuel est activé
source cinemacousas_env/bin/activate
pip install -r requirements.txt
```

## Dépendances utilisées

### Dépendances principales (requises)
- **Flask==3.0.0** - Framework web principal pour l'interface utilisateur
- **Flask-CORS==4.0.0** - Gestion des requêtes CORS pour l'API
- **mysql-connector-python==8.2.0** - Connecteur pour la base de données MySQL

### Dépendances automatiques (installées avec Flask)
Ces dépendances sont installées automatiquement avec Flask :
- `Werkzeug` - Serveur WSGI et utilitaires
- `Jinja2` - Moteur de templates pour le rendu HTML
- `MarkupSafe` - Échappement sécurisé pour les templates
- `itsdangerous` - Signature sécurisée des sessions
- `click` - Interface en ligne de commande
- `blinker` - Système de signaux

### Dépendances automatiques (installées avec mysql-connector)
- `protobuf` - Sérialisation des données pour MySQL

## Configuration de la base de données

### Paramètres de connexion
Les paramètres de connexion MySQL sont définis dans `modele.py` :
```python
DB_CONFIG = {
    "host": "82.66.24.184",
    "port": 3305,
    "user": "cinemacousas",
    "password": "password", 
    "database": "Cinemacousas"
}
```

### Scripts SQL
Les scripts de création de la base de données sont disponibles dans le dossier `workspace/` :
- `V1.sql` - Structure initiale
- `V2.sql` - Améliorations 
- `V3.sql` - Ajouts de fonctionnalités
- `V4.sql` - Version finale

## Lancement de l'application

### Interface d'administration (recommandée)
```bash
# Activer l'environnement virtuel
source cinemacousas_env/bin/activate

# Lancer l'interface d'administration
python3 server_admin.py
```

L'interface d'administration sera accessible à : `http://localhost:5003`

### Application complète (utilisateur + admin)
Si vous voulez tester la version complète avec les fonctionnalités utilisateur :
```bash
# Activer l'environnement virtuel
source cinemacousas_env/bin/activate

# Aller dans le dossier user
cd user/

# Lancer le serveur complet
python3 server_full.py
```

L'application complète sera accessible à : `http://localhost:5002`

## Structure du projet

```
Cinemacousas/
├── server_admin.py         # Serveur d'administration (PRINCIPAL)
├── modele.py              # Modèle de données et fonctions BDD
├── requirements.txt       # Dépendances Python
├── .env                   # Configuration (à créer/modifier)
├── .env.example          # Template de configuration
├── start_admin.sh        # Script de démarrage rapide
├── templates/            # Templates HTML d'administration
│   ├── admin.html        # Interface d'administration principale
│   ├── base.html         # Template de base
│   └── login.html        # Page de connexion admin
├── static/              # Fichiers statiques (CSS, JS, images)
├── user/                # Fonctionnalités utilisateur (archivées)
│   ├── server.py        # Ancien serveur principal
│   ├── server_full.py   # Serveur complet (user + admin)
│   └── templates/       # Templates utilisateur
└── docs/                # Documentation et conception (anciennement workspace/)
    ├── V1.sql, V2.sql...# Scripts SQL
    └── *.pdf, *.mwb     # Documents techniques
```
│   ├── server_full.py   # Serveur complet (user + admin)
│   └── templates/       # Templates utilisateur
│       ├── booking_spectators.html
│       ├── booking_tickets.html
│       ├── home.html
│       ├── movie_detail.html
│       ├── movies.html
│       ├── my_bookings.html
│       ├── showing_seats.html
│       └── showings_today.html
├── workspace/           # Scripts SQL et documentation
├── old/                # Archives et code de nettoyage
└── cinemacousas_env/   # Environnement virtuel
```

## Fonctionnalités principales

### Interface d'administration (server_admin.py)
- **Gestion des films** : Ajout, modification, suppression des films
- **Gestion des affiches** : Upload et suppression des posters
- **Gestion des salles** : Configuration des salles et des sièges
- **Gestion des séances** : Programmation des séances
- **Gestion des réservations** : Consultation et annulation des réservations
- **Authentification admin** : Accès sécurisé aux fonctionnalités

### Fonctionnalités utilisateur (dans user/server_full.py)
- **Consultation des films** : Affichage des films et séances
- **Réservation de places** : Sélection de sièges et informations spectateurs
- **Gestion des réservations** : Visualisation des réservations personnelles
- **Système de tarification** : Tarifs différenciés selon l'âge

## Validation et tests

Pour vérifier que l'installation fonctionne :
```bash
source cinemacousas_env/bin/activate
python3 validate_cleanup.py
```

## Support

Ce projet utilise uniquement des dépendances stables et bien maintenues. En cas de problème :

1. Vérifiez que Python 3.8+ est installé : `python3 --version`
2. Vérifiez la connexion à la base de données MySQL
3. Assurez-vous que l'environnement virtuel est activé
4. Réinstallez les dépendances : `pip install -r requirements.txt --force-reinstall`

## Architecture

Le projet suit une architecture MVC (Modèle-Vue-Contrôleur) :
- **Modèle** : `modele.py` - Gestion de la base de données et logique métier
- **Vue** : `templates/` - Interface utilisateur en HTML/Jinja2
- **Contrôleur** : `server_admin.py` - Routes et logique de contrôle

## Endpoints d'administration

### Pages principales
- `GET /` - Redirection vers le dashboard admin
- `GET /admin` - Dashboard d'administration principal
- `GET /admin/login` - Page de connexion admin
- `GET /admin/logout` - Déconnexion admin

### API de gestion
- `POST /admin/movie` - Ajouter un film
- `POST /admin/movie/<id>/update` - Modifier un film
- `POST /admin/movie/<id>/delete` - Supprimer un film
- `POST /admin/movie/<id>/poster/upload` - Upload affiche
- `POST /admin/room` - Ajouter une salle
- `POST /admin/showing` - Ajouter une séance
- `POST /admin/booking/<id>/cancel` - Annuler une réservation

### API utilitaires
- `GET /movie/<id>/poster` - Servir les affiches
- `GET /api/room/<id>/seats` - Récupérer la grille des sièges
- `PUT /api/seat/<id>/type` - Modifier le type d'un siège

## Dernière mise à jour
Projet nettoyé et restructuré le 27 juin 2025.
**Version actuelle :** Interface d'administration autonome.
