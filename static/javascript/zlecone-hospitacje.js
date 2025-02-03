// Funkcja pobierająca zlecone hospitacje dla użytkownika o ID = 1
async function fetchAssignedHospitations() {
    try {
        const userId = 1; // Mockowy użytkownik
        const response = await fetch(`/api/hospitacje/zlecone/${userId}`);
        
        if (!response.ok) {
            throw new Error('Błąd pobierania danych');
        }
        
        const hospitationData = await response.json();
        displayAssignedHospitations(hospitationData);
    } catch (error) {
        console.error('Błąd:', error);
    }
}

// Funkcja odpowiedzialna za wyświetlenie hospitacji w kontenerze
function displayAssignedHospitations(hospitationData) {
    const container = document.querySelector('.assigned-hospitations');
    container.innerHTML = ''; // Czyści poprzednie dane

    if (!hospitationData || hospitationData.length === 0) {
        const info = document.createElement('p');
        info.textContent = 'Brak zleconych hospitacji.';
        container.appendChild(info);
        return;
    }

    hospitationData.forEach(hospitation => {
        // Główny kontener dla jednej hospitacji
        const hospitationDiv = document.createElement('div');
        hospitationDiv.classList.add('hospitation-item');

        // Nagłówek z podstawowymi informacjami
        const header = document.createElement('div');
        header.classList.add('hospitation-header');

        const title = document.createElement('p');
        title.classList.add('name');
        title.textContent = hospitation.nazwa;

        const date = document.createElement('p');
        date.classList.add('date');
        date.textContent = hospitation.termin;

        const statusIcon = document.createElement('i');
        if (hospitation.status === 'completed') {
            statusIcon.classList.add('fa-solid', 'fa-square-check');
        } else {
            statusIcon.classList.add('fa-regular', 'fa-square');
        }

        // Przycisk umożliwiający rozwinięcie i edycję hospitacji
        const editButton = document.createElement('button');
        editButton.textContent = 'Edytuj';
        editButton.addEventListener('click', () => editHospitation(hospitation.id, hospitationDiv));

        // Dodajemy elementy do nagłówka
        header.appendChild(title);
        header.appendChild(date);
        header.appendChild(statusIcon);
        header.appendChild(editButton);
        hospitationDiv.appendChild(header);

        // Kontener dla formularza edycji – ukryty domyślnie (bezpośrednio sterowany przez klasę CSS)
        const editContainer = document.createElement('div');
        editContainer.classList.add('edit-container'); // CSS zadba o efekt rozwijania
        hospitationDiv.appendChild(editContainer);

        container.appendChild(hospitationDiv);
    });
}

// Funkcja inicjująca edycję hospitacji – zamiast ładować istniejący protokół, pobieramy pusty szablon
function editHospitation(id, hospitationDiv) {
    showEditFormUsingTemplate(id, hospitationDiv);
}

// Funkcja pobierająca pusty szablon i generująca formularz edycji
async function showEditFormUsingTemplate(id, hospitationDiv) {
    const editContainer = hospitationDiv.querySelector('.edit-container');
    editContainer.innerHTML = '';
    try {
        const templateResponse = await fetch('/api/szablon');
        if (!templateResponse.ok) {
            throw new Error("Błąd ładowania szablonu");
        }
        const templateData = await templateResponse.json();

        // Tworzymy formularz na podstawie szablonu
        const form = document.createElement('form');
        form.id = "protocol-form";

        templateData.forEach((section, sectionIndex) => {
            const sectionDiv = document.createElement('div');
            sectionDiv.classList.add('protocol-section');

            // Nagłówek sekcji
            const sectionHeader = document.createElement('h3');
            sectionHeader.textContent = section.nazwa;
            sectionDiv.appendChild(sectionHeader);

            // Opcjonalny opis sekcji
            if (section.opis) {
                const sectionDesc = document.createElement('p');
                sectionDesc.textContent = section.opis;
                sectionDiv.appendChild(sectionDesc);
            }

            // Dla każdego pytania w sekcji tworzymy pole tekstowe
            section.info.forEach((item, infoIndex) => {
                const fieldContainer = document.createElement('div');
                fieldContainer.classList.add('protocol-field');

                const label = document.createElement('label');
                label.textContent = item.pytanie;
                label.setAttribute('for', `section${sectionIndex}_field${infoIndex}`);
                fieldContainer.appendChild(label);

                // Pole tekstowe – pozostawiamy puste
                const input = document.createElement('input');
                input.type = 'text';
                input.id = `section${sectionIndex}_field${infoIndex}`;
                input.name = `section${sectionIndex}_field${infoIndex}`;
                input.placeholder = ""; 
                fieldContainer.appendChild(input);

                sectionDiv.appendChild(fieldContainer);
            });
            form.appendChild(sectionDiv);
        });

        editContainer.appendChild(form);

        // Przycisk zapisu – wywołuje funkcję, która zbiera dane z formularza i wysyła do backendu
        const btnSave = document.createElement('button');
        btnSave.textContent = 'Zapisz';
        btnSave.type = 'button';
        btnSave.addEventListener('click', () => {
            saveProtocolTemplate(id, form);
        });

        // Przycisk zatwierdzający hospitację
        const btnApprove = document.createElement('button');
        btnApprove.textContent = 'Zatwierdź';
        btnApprove.type = 'button';
        btnApprove.addEventListener('click', () => {
            approveHospitation(id);
        });

        // Przycisk anulowania edycji – zwija formularz
        const btnCancel = document.createElement('button');
        btnCancel.textContent = 'Anuluj';
        btnCancel.type = 'button';
        btnCancel.addEventListener('click', () => {
            // Usuwamy klasę expanded, aby formularz zwijał się
            editContainer.classList.remove('expanded');
        });

        editContainer.appendChild(btnSave);
        editContainer.appendChild(btnApprove);
        editContainer.appendChild(btnCancel);

        // Dodajemy klasę expanded, która wywoła efekt rozwijania
        editContainer.classList.add('expanded');
    } catch (error) {
        console.error(error);
        alert('Wystąpił błąd podczas ładowania szablonu');
    }
}

// Funkcja zbierająca dane z formularza i zapisująca je w postaci JSON
function saveProtocolTemplate(id, form) {
    const protocol = [];
    const sectionDivs = form.querySelectorAll('.protocol-section');
    sectionDivs.forEach((sectionDiv) => {
        const section = {};
        section.nazwa = sectionDiv.querySelector('h3').textContent;
        // Jeśli istnieje opis, go pobieramy
        const descElem = sectionDiv.querySelector('p');
        section.opis = descElem ? descElem.textContent : "";
        section.info = [];

        const fieldDivs = sectionDiv.querySelectorAll('.protocol-field');
        fieldDivs.forEach((fieldDiv) => {
            const label = fieldDiv.querySelector('label').textContent;
            const input = fieldDiv.querySelector('input');
            section.info.push({
                pytanie: label,
                odpowiedz: input.value
            });
        });
        protocol.push(section);
    });

    // Wysyłamy zebrany protokół do backendu
    fetch(`/api/hospitacja/${id}/zapisz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ protocol: protocol })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Błąd zapisu protokołu');
        }
        return response.json();
    })
    .then(result => {
        alert(result.message);
        // Opcjonalnie: można odświeżyć interfejs lub usunąć klasę expanded
        const editContainer = form.parentElement;
        editContainer.classList.remove('expanded');
    })
    .catch(error => {
        console.error(error);
        alert('Wystąpił błąd podczas zapisywania protokołu');
    });
}

// Funkcja zatwierdzająca hospitację (wywołuje już istniejący endpoint)
async function approveHospitation(id) {
    try {
        const response = await fetch(`/api/hospitacja/${id}/zaakceptuj`, {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error('Błąd zatwierdzania hospitacji');
        }
        const result = await response.json();
        alert(result.message);
        // Opcjonalnie: można zaktualizować interfejs, np. usunąć formularz edycji
    } catch (error) {
        console.error(error);
        alert('Wystąpił błąd podczas zatwierdzania hospitacji');
    }
}

// Uruchamiamy pobieranie zleconych hospitacji po załadowaniu strony
window.onload = fetchAssignedHospitations;
