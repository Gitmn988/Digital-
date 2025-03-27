/**
 * Library Bibliography Generator
 * Handles searching for books and generating bibliographies
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to main content
    document.querySelector('.app-container').classList.add('fade-in');
    
    // Initialize mode selection
    const modeSelector = document.getElementById('modalita');
    if (modeSelector) {
        modeSelector.addEventListener('change', cambiaModalita);
    }
    
    // Add event listeners to search buttons
    const simpleSearchBtn = document.getElementById('simpleSearchBtn');
    if (simpleSearchBtn) {
        simpleSearchBtn.addEventListener('click', cercaBibliografia);
    }

    // Initialize tooltips and other UI elements
    initializeUI();
});

/**
 * Initialize UI elements and interactions
 */
function initializeUI() {
    // Add subtle hover effects to buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Add input field animations
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('active-input');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('active-input');
        });
    });
}

/**
 * Change between simple and advanced search modes
 */
function cambiaModalita() {
    let modalita = document.getElementById("modalita").value;
    let inputContainer = document.getElementById("inputContainer");
    let formContainer = document.getElementById("formContainer");
    
    // Clear previous results
    document.getElementById("result").innerHTML = "";
    document.getElementById("error-message").innerHTML = "";
    
    if (modalita === "semplice") {
        inputContainer.style.display = "block";
        formContainer.style.display = "none";
    } else {
        inputContainer.style.display = "none";
        formContainer.style.display = "block";
        generaForm();
    }
}

/**
 * Generate form for advanced bibliography input
 */
function generaForm() {
    let numLibri = parseInt(prompt("Quanti libri vuoi inserire?", "1")) || 1; 
    let formContainer = document.getElementById("formContainer");
    formContainer.innerHTML = "";
    
    for (let i = 0; i < numLibri; i++) {
        formContainer.innerHTML += `
            <fieldset class="book-form">
                <legend>Libro ${i + 1}</legend>
                <div class="form-row">
                    <div class="form-group">
                        <label for="nome-${i}">Nome autore:</label>
                        <input type="text" id="nome-${i}" class="nome" required>
                    </div>
                    <div class="form-group">
                        <label for="cognome-${i}">Cognome autore:</label>
                        <input type="text" id="cognome-${i}" class="cognome" required>
                    </div>
                </div>
                <div class="form-group">
                    <label for="titolo-${i}">Titolo opera:</label>
                    <input type="text" id="titolo-${i}" class="titolo" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="editore-${i}">Casa Editrice:</label>
                        <input type="text" id="editore-${i}" class="editore">
                    </div>
                    <div class="form-group">
                        <label for="luogo-${i}">Luogo di stampa:</label>
                        <input type="text" id="luogo-${i}" class="luogo">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="anno-${i}">Anno edizione:</label>
                        <input type="number" id="anno-${i}" class="anno">
                    </div>
                    <div class="form-group">
                        <label for="formato-${i}">Formato citazione:</label>
                        <select id="formato-${i}" class="formato">
                            <option value="MLA">MLA</option>
                            <option value="Chicago">Chicago</option>
                            <option value="APA">APA</option>
                        </select>
                    </div>
                </div>
            </fieldset>
        `;
    }
    
    const createBtn = document.createElement('button');
    createBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-book-open">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
        </svg>
        Crea Bibliografia
    `;
    createBtn.onclick = generaBibliografia;
    formContainer.appendChild(createBtn);
    
    // Initialize UI for new form elements
    initializeUI();
}

/**
 * Generate citation based on format and book details
 */
function generaCitazione(formato, autore, titolo, editore, luogo, anno) {
    if (formato === "MLA") {
        return `${autore}. <i>${titolo}</i>. ${luogo ? luogo + ': ' : ''}${editore ? editore + ', ' : ''}${anno || ''}.`;
    } else if (formato === "Chicago") {
        return `${autore}. <i>${titolo}</i>. ${luogo ? luogo + ': ' : ''}${editore ? editore + ', ' : ''}${anno || ''}.`;
    } else if (formato === "APA") {
        return `${autore}. ${anno ? '(' + anno + '). ' : ''}<i>${titolo}</i>. ${luogo ? luogo + ': ' : ''}${editore || ''}.`;
    }
}

/**
 * Generate bibliography from advanced form input
 */
function generaBibliografia() {
    let libri = document.querySelectorAll("fieldset");
    let result = "";
    let isValid = true;
    
    // Show loading indicator
    document.getElementById("result").innerHTML = '<div class="loading"></div> Generazione bibliografia in corso...';

    setTimeout(() => {
        libri.forEach(libro => {
            let nome = libro.querySelector(".nome").value;
            let cognome = libro.querySelector(".cognome").value;
            let titolo = libro.querySelector(".titolo").value;
            let editore = libro.querySelector(".editore").value;
            let luogo = libro.querySelector(".luogo").value;
            let anno = libro.querySelector(".anno").value;
            let formato = libro.querySelector(".formato").value;

            if (!nome || !cognome || !titolo) {
                isValid = false;
                return;
            }

            let citazione = generaCitazione(formato, `${cognome}, ${nome}`, titolo, editore, luogo, anno);
            result += `<div class="citation-item">${citazione}</div>`;
        });
        
        document.getElementById("result").innerHTML = isValid ? result : "";
        document.getElementById("error-message").innerHTML = isValid ? "" : "Per favore, compila tutti i campi richiesti (Nome, Cognome, Titolo).";
    }, 800); // Simulate processing time
}

/**
 * Search for books using Google Books API
 */
function cercaBibliografia() {
    let titolo = document.getElementById("titoloSemplice").value;
    let formato = document.getElementById("formatoSemplice").value;
    
    if (!titolo) {
        document.getElementById("error-message").innerHTML = "Inserisci un titolo per la ricerca.";
        return;
    }
    
    document.getElementById("error-message").innerHTML = "";
    document.getElementById("result").innerHTML = '<div class="loading"></div> Ricerca in corso...';

    fetch(`https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(titolo)}`)
        .then(response => response.json())
        .then(data => {
            if (data.items && data.items.length > 0) {
                let risultati = data.items.slice(0, Math.max(2, Math.min(4, data.items.length)));
                let citazioni = risultati.map(libro => {
                    let info = libro.volumeInfo;
                    let autore = info.authors ? info.authors.join(", ") : "Autore sconosciuto";
                    let titoloLibro = info.title;
                    let editore = info.publisher || "Editore sconosciuto";
                    let anno = info.publishedDate ? info.publishedDate.split("-")[0] : "Data sconosciuta";
                    
                    return `<div class="citation-item">${generaCitazione(formato, autore, titoloLibro, editore, "", anno)}</div>`;
                }).join("");

                document.getElementById("result").innerHTML = citazioni;
            } else {
                document.getElementById("result").innerHTML = "Nessun risultato trovato.";
            }
        })
        .catch(error => {
            console.error("Errore durante la ricerca:", error);
            document.getElementById("result").innerHTML = "Si è verificato un errore durante la ricerca.";
        });
}
