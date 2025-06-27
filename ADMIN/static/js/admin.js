// JavaScript pour la page d'administration
document.addEventListener('DOMContentLoaded', function() {
    const roomSelect = document.getElementById('room-select');
    const seatsGridContainer = document.getElementById('seats-grid-container');
    const selectedRoomTitle = document.getElementById('selected-room-title');
    const seatsGrid = document.getElementById('seats-grid');
    
    roomSelect.addEventListener('change', function() {
        const roomId = this.value;
        if (!roomId) {
            seatsGridContainer.style.display = 'none';
            return;
        }
        
        const selectedOption = this.options[this.selectedIndex];
        const roomName = selectedOption.text;
        selectedRoomTitle.textContent = `Configuration des sièges - ${roomName}`;
        
        loadRoomSeats(roomId);
    });
    
    async function loadRoomSeats(roomId) {
        try {
            const response = await fetch(`/api/room/${roomId}/seats`);
            const data = await response.json();
            
            if (data.error) {
                alert('Erreur: ' + data.error);
                return;
            }
            
            generateSeatsGrid(data);
            seatsGridContainer.style.display = 'block';
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors du chargement des sièges');
        }
    }
    
    function generateSeatsGrid(data) {
        console.log('Données des sièges:', data);
        const { room, grid } = data;
        seatsGrid.innerHTML = '';
        
        // Ajouter la ligne d'en-têtes de colonnes
        const headerRow = document.createElement('div');
        headerRow.className = 'column-headers-row';
        
        // Spacer pour aligner avec les labels de rangées
        const headerSpacer = document.createElement('div');
        headerSpacer.className = 'column-headers-spacer';
        headerRow.appendChild(headerSpacer);
        
        // En-têtes de colonnes (1, 2, 3, ...)
        for (let colIndex = 1; colIndex <= room.nb_columns; colIndex++) {
            const headerDiv = document.createElement('div');
            headerDiv.className = 'column-header';
            headerDiv.textContent = colIndex;
            headerRow.appendChild(headerDiv);
        }
        
        seatsGrid.appendChild(headerRow);
        
        // Générer les rangées (A, B, C, ...)
        for (let rowIndex = 1; rowIndex <= room.nb_rows; rowIndex++) {
            const rowLetter = String.fromCharCode(64 + rowIndex);
            const rowDiv = document.createElement('div');
            rowDiv.className = 'seats-row';
            
            // Label de la rangée
            const rowLabel = document.createElement('div');
            rowLabel.className = 'row-label';
            rowLabel.textContent = rowLetter;
            rowDiv.appendChild(rowLabel);
            
            // Sièges de la rangée
            for (let colIndex = 1; colIndex <= room.nb_columns; colIndex++) {
                const seatDiv = document.createElement('div');
                seatDiv.className = 'seat-admin';
                // Supprimer l'affichage du numéro
                // seatDiv.textContent = colIndex;
                
                // Récupérer les données du siège
                const seatData = grid[rowLetter] && grid[rowLetter][colIndex];
                if (seatData) {
                    seatDiv.classList.add(seatData.type);
                    seatDiv.dataset.seatId = seatData.id;
                    seatDiv.dataset.currentType = seatData.type;
                    
                    // Gestionnaire de clic pour changer le type
                    seatDiv.addEventListener('click', function() {
                        changeSeatType(this);
                    });
                }
                
                rowDiv.appendChild(seatDiv);
            }
            
            seatsGrid.appendChild(rowDiv);
        }
    }
    
    function changeSeatType(seatElement) {
        const currentType = seatElement.dataset.currentType;
        const types = ['normal', 'pmr', 'stair', 'empty'];
        const currentIndex = types.indexOf(currentType);
        const nextIndex = (currentIndex + 1) % types.length;
        const newType = types[nextIndex];
        
        updateSeatType(seatElement.dataset.seatId, newType, seatElement);
    }
    
    async function updateSeatType(seatId, newType, seatElement) {
        try {
            const response = await fetch(`/api/seat/${seatId}/type`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ type: newType })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Mettre à jour l'apparence du siège
                seatElement.className = `seat-admin ${newType}`;
                seatElement.dataset.currentType = newType;
            } else {
                alert('Erreur: ' + result.message);
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la mise à jour');
        }
    }

    // Fonctions pour rafraîchir les affiches après upload/delete
    function refreshPosterImages(movieId) {
        const timestamp = Date.now();
        
        // Rafraîchir l'affiche dans le tableau
        const thumbnailImg = document.querySelector(`img[src*="/movie/${movieId}/poster"]`);
        if (thumbnailImg) {
            const currentSrc = thumbnailImg.src;
            const newSrc = currentSrc.split('?')[0] + '?v=' + timestamp;
            thumbnailImg.src = newSrc;
        }
        
        // Rafraîchir l'affiche dans la modal
        const modalImg = document.getElementById(`currentPoster${movieId}`);
        if (modalImg) {
            const currentSrc = modalImg.src;
            const newSrc = currentSrc.split('?')[0] + '?v=' + timestamp;
            modalImg.src = newSrc;
        }
    }

    // Gestionnaire pour les formulaires d'upload d'affiche
    document.querySelectorAll('form[action*="/poster/upload"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const movieId = this.action.match(/\/movie\/(\d+)\/poster\/upload/)[1];
            
            // Délai pour permettre au serveur de traiter l'upload
            setTimeout(() => {
                refreshPosterImages(movieId);
            }, 1000);
        });
    });

    // Gestionnaire pour les formulaires de suppression d'affiche
    document.querySelectorAll('form[action*="/poster/delete"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const movieId = this.action.match(/\/movie\/(\d+)\/poster\/delete/)[1];
            
            // Délai pour permettre au serveur de traiter la suppression
            setTimeout(() => {
                refreshPosterImages(movieId);
            }, 1000);
        });
    });
});
