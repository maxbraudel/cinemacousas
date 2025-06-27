#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cinemacousas - Version Administration uniquement
Interface d'administration pour la gestion du cinéma
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, Response
from flask_cors import CORS
import modele  # Import du module pour la gestion de la base de données
import importlib
from datetime import datetime, date
import time
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Forcer le rechargement du module modele
importlib.reload(modele)

app = Flask(__name__)
CORS(app)

# Configuration depuis les variables d'environnement
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_POSTER_SIZE_MB', 5)) * 1024 * 1024  # Taille max en bytes

# Configuration des uploads
ALLOWED_TYPES = set(os.getenv('ALLOWED_POSTER_TYPES', 'image/jpeg,image/png,image/svg+xml').split(','))
POSTER_CACHE_MAX_AGE = int(os.getenv('POSTER_CACHE_MAX_AGE', 3600))
POSTER_CACHE_SHORT_MAX_AGE = int(os.getenv('POSTER_CACHE_SHORT_MAX_AGE', 300))

# Configuration admin
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_REQUIRED = os.getenv('ADMIN_PASSWORD_REQUIRED', 'False').lower() == 'true'

# Cache timestamp pour le cache-busting des affiches
POSTER_CACHE_TIMESTAMP = str(int(time.time()))

def get_poster_url_with_cache_busting(movie_id):
    """Génère une URL d'affiche avec paramètre de cache-busting"""
    return url_for('movie_poster', movie_id=movie_id, v=POSTER_CACHE_TIMESTAMP)

# Rendre la fonction disponible dans les templates
@app.context_processor
def utility_processor():
    return dict(get_poster_url_with_cache_busting=get_poster_url_with_cache_busting)

# Ajouter des fonctions helper pour les templates
@app.template_global()
def chr_function(num):
    return chr(num)

# ===== ROUTES PRINCIPALES =====

@app.route('/')
def index():
    """Page d'accueil - Redirection vers admin"""
    return redirect(url_for('admin_dashboard'))

@app.route('/movie/<int:movie_id>/poster')
def movie_poster(movie_id):
    """Servir l'affiche d'un film en tant qu'image"""
    poster = modele.get_movie_poster(movie_id)
    
    if not poster:
        # Retourner une image par défaut ou une erreur 404
        return Response("Affiche non trouvée", status=404)
    
    # Vérifier si c'est une requête avec cache-busting
    version = request.args.get('v', '')
    
    # Cache plus court pour permettre les mises à jour
    cache_control = f'public, max-age={POSTER_CACHE_SHORT_MAX_AGE}'  # Cache configuré
    if version:
        # Si version spécifiée, cache plus long mais avec ETag
        cache_control = f'public, max-age={POSTER_CACHE_MAX_AGE}'  # Cache configuré
    
    return Response(
        poster['image'],
        mimetype=poster['mime_type'],
        headers={
            'Content-Disposition': f'inline; filename="{poster["name"]}"',
            'Cache-Control': cache_control,
            'ETag': f'"{movie_id}-{len(poster["image"])}"'  # ETag basé sur l'ID et la taille
        }
    )

# ===== ROUTES D'AUTHENTIFICATION SIMPLIFIÉE =====

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Formulaire de connexion et traitement"""
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST - traitement de la connexion
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash('Nom d\'utilisateur et mot de passe requis', 'error')
        return redirect(url_for('login_form'))
    
    # Connexion simplifiée pour admin
    if username == ADMIN_USERNAME and (not ADMIN_PASSWORD_REQUIRED or password):  # Configuration depuis .env
        session['user_id'] = 1
        session['username'] = username
        session['is_admin'] = True
        flash('Connexion administrateur réussie', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Accès administrateur requis', 'error')
        return redirect(url_for('login_form'))

@app.route('/logout')
def logout():
    """Déconnexion utilisateur"""
    session.clear()
    return redirect(url_for('index'))

# ===== ROUTES D'ADMINISTRATION =====

@app.route('/admin')
def admin_dashboard():
    """Tableau de bord administrateur"""
    if 'is_admin' not in session:
        flash('Accès administrateur requis', 'error')
        return redirect(url_for('login_form'))
    
    movies = modele.get_all_movies()
    rooms = modele.get_all_rooms()
    showings = modele.get_all_showings()
    bookings = modele.get_all_bookings()
    
    today = date.today()
    
    return render_template('admin.html', movies=movies, rooms=rooms, showings=showings, bookings=bookings, today=today)

@app.route('/admin/movie', methods=['POST'])
def add_movie():
    """Ajouter un film"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    name = request.form.get('name')
    duration = request.form.get('duration')
    director = request.form.get('director')
    cast = request.form.get('cast')
    synopsis = request.form.get('synopsis')
    
    if not name or not duration:
        flash('Nom et durée du film requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        duration = int(duration)
        success, message = modele.add_movie(name, duration, director, cast, synopsis)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('La durée doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/update', methods=['POST'])
def update_movie(movie_id):
    """Mettre à jour un film"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    name = request.form.get('name')
    duration = request.form.get('duration')
    director = request.form.get('director')
    cast = request.form.get('cast')
    synopsis = request.form.get('synopsis')
    
    if not name or not duration:
        flash('Nom et durée du film requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        duration = int(duration)
        success, message = modele.update_movie(movie_id, name, duration, director, cast, synopsis)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('La durée doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    """Supprimer un film"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    success, message = modele.delete_movie(movie_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/poster/upload', methods=['POST'])
def upload_movie_poster(movie_id):
    """Télécharger une affiche pour un film"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    try:
        if 'poster' not in request.files:
            flash('Aucun fichier sélectionné', 'error')
            return redirect(url_for('admin_dashboard'))
        
        file = request.files['poster']
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Vérifier le type de fichier
        if file.content_type not in ALLOWED_TYPES:
            allowed_types_str = ', '.join(ALLOWED_TYPES).replace('image/', '').upper()
            flash(f'Type de fichier non supporté. Utilisez {allowed_types_str}.', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Vérifier la taille (configurée dans .env)
        file.seek(0, 2)  # Se déplacer à la fin du fichier
        file_size = file.tell()
        file.seek(0)  # Revenir au début
        
        max_size = int(os.getenv('MAX_POSTER_SIZE_MB', 5)) * 1024 * 1024
        if file_size > max_size:
            max_mb = int(os.getenv('MAX_POSTER_SIZE_MB', 5))
            flash(f'Le fichier est trop volumineux (max {max_mb}MB)', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Lire le contenu du fichier
        file_content = file.read()
        
        # Sauvegarder l'affiche
        success, message = modele.save_movie_poster(movie_id, file.filename, file.content_type, file_content)
        
        # Mettre à jour le timestamp du cache pour forcer le rafraîchissement
        if success:
            global POSTER_CACHE_TIMESTAMP
            POSTER_CACHE_TIMESTAMP = str(int(time.time()))
        
        flash(message, 'success' if success else 'error')
        
    except Exception as e:
        flash(f'Erreur lors du téléchargement: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/poster/delete', methods=['POST'])
def delete_movie_poster_route(movie_id):
    """Supprimer l'affiche d'un film"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    success, message = modele.delete_movie_poster(movie_id)
    
    # Mettre à jour le timestamp du cache pour forcer le rafraîchissement
    if success:
        global POSTER_CACHE_TIMESTAMP
        POSTER_CACHE_TIMESTAMP = str(int(time.time()))
    
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/room', methods=['POST'])
def add_room():
    """Ajouter une salle"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    name = request.form.get('name')
    nb_rows = request.form.get('rows')
    nb_columns = request.form.get('columns')
    
    if not name or not nb_rows or not nb_columns:
        flash('Nom, nombre de rangées et colonnes requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        nb_rows = int(nb_rows)
        nb_columns = int(nb_columns)
        success, message = modele.add_room(name, nb_rows, nb_columns)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Le nombre de rangées et colonnes doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/room/<int:room_id>/update', methods=['POST'])
def update_room(room_id):
    """Mettre à jour une salle"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    name = request.form.get('name')
    nb_rows = request.form.get('rows')
    nb_columns = request.form.get('columns')
    
    if not name:
        flash('Nom de la salle requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Si les dimensions ne sont pas fournies, utiliser les valeurs actuelles
    if not nb_rows or not nb_columns:
        # Récupérer les dimensions actuelles
        rooms = modele.get_all_rooms()
        current_room = next((room for room in rooms if room['id'] == room_id), None)
        if current_room:
            nb_rows = current_room['nb_rows']
            nb_columns = current_room['nb_columns']
        else:
            flash('Salle non trouvée', 'error')
            return redirect(url_for('admin_dashboard'))
    
    try:
        nb_rows = int(nb_rows)
        nb_columns = int(nb_columns)
        success, message = modele.update_room(room_id, name, nb_rows, nb_columns)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Le nombre de rangées et colonnes doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/room/<int:room_id>/delete', methods=['POST'])
def delete_room(room_id):
    """Supprimer une salle"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    success, message = modele.delete_room(room_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/showing', methods=['POST'])
def add_showing():
    """Ajouter une séance"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    date = request.form.get('date')
    starttime = request.form.get('starttime')
    baseprice = request.form.get('baseprice')
    room_id = request.form.get('room_id')
    movie_id = request.form.get('movie_id')
    
    if not all([date, starttime, baseprice, room_id, movie_id]):
        flash('Tous les champs sont requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        baseprice = int(float(baseprice) * 100)  # Convertir euros en centimes
        room_id = int(room_id)
        movie_id = int(movie_id)
        
        success, message = modele.add_showing(date, starttime, baseprice, room_id, movie_id)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Données invalides', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/showing/<int:showing_id>/update', methods=['POST'])
def update_showing(showing_id):
    """Mettre à jour une séance"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    date = request.form.get('date')
    starttime = request.form.get('starttime')
    baseprice = request.form.get('baseprice')
    room_id = request.form.get('room_id')
    movie_id = request.form.get('movie_id')
    
    if not all([date, starttime, baseprice, room_id, movie_id]):
        flash('Tous les champs sont requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        baseprice = int(float(baseprice) * 100)  # Convertir euros en centimes
        room_id = int(room_id)
        movie_id = int(movie_id)
        
        success, message = modele.update_showing(showing_id, date, starttime, baseprice, room_id, movie_id)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Données invalides', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/showing/<int:showing_id>/delete', methods=['POST'])
def delete_showing(showing_id):
    """Supprimer une séance"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    success, message = modele.delete_showing(showing_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Annuler une réservation"""
    if 'is_admin' not in session:
        return redirect(url_for('login_form'))
    
    success, message = modele.cancel_booking(booking_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

# ===== APIs REST POUR L'ADMINISTRATION =====

@app.route('/api/room/<int:room_id>/seats')
def get_room_seats_grid(room_id):
    """API pour récupérer la grille des sièges d'une salle"""
    if 'is_admin' not in session:
        return jsonify({'error': 'Accès non autorisé'}), 401
    
    grid_data = modele.get_room_seats_grid(room_id)
    if grid_data is None:
        return jsonify({'error': 'Salle non trouvée'}), 404
    
    return jsonify(grid_data)

@app.route('/api/seat/<int:seat_id>/type', methods=['PUT'])
def update_seat_type(seat_id):
    """API pour mettre à jour le type d'un siège"""
    if 'is_admin' not in session:
        return jsonify({'error': 'Accès non autorisé'}), 401
    
    data = request.get_json()
    new_type = data.get('type')
    
    if new_type not in ['normal', 'pmr', 'stair', 'empty']:
        return jsonify({'success': False, 'message': 'Type de siège invalide'}), 400
    
    success, message = modele.update_seat_type(seat_id, new_type)
    return jsonify({'success': success, 'message': message})

# Point d'entrée du programme
if __name__ == "__main__":
    # Configuration depuis les variables d'environnement
    flask_port = int(os.getenv('FLASK_PORT', 5003))
    flask_debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("Démarrage du serveur Cinemacousas - Administration")
    print(f"Interface d'administration accessible à : http://localhost:{flask_port}")
    print(f"Connexion : username={ADMIN_USERNAME}, password={'requis' if ADMIN_PASSWORD_REQUIRED else 'n\'importe_quoi'}")
    print(f"Mode debug : {'Activé' if flask_debug else 'Désactivé'}")
    
    app.run(debug=flask_debug, port=flask_port)
