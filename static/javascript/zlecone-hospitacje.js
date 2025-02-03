async function fetchAssignedHospitations() {
    try {
        const userId = 1;
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

function displayAssignedHospitations(hospitationData) {
    const container = document.querySelector('.assigned-hospitations');
    container.innerHTML = '';

    if (!hospitationData || hospitationData.length === 0) {
        const info = document.createElement('p');
        info.textContent = 'Brak zleconych hospitacji.';
        container.appendChild(info);
        return;
    }

    hospitationData.forEach(hospitation => {
        const hospitationDiv = document.createElement('div');
        hospitationDiv.classList.add('hospitation-item');
        hospitationDiv.setAttribute('data-id', hospitation.id);
        console.log("Hospitation id:", hospitation.id);
        console.log("Hospitation status:", hospitation.status);

        const header = document.createElement('div');
        header.classList.add('hospitation-header');

        const title = document.createElement('p');
        title.classList.add('name');
        title.textContent = hospitation.nazwa;

        const date = document.createElement('p');
        date.classList.add('date');
        date.textContent = hospitation.termin;

        const statusIcon = document.createElement('i');
        statusIcon.classList.add('status-icon', 'fa-regular', 'fa-square');

        const editButton = document.createElement('button');
        editButton.textContent = 'Edytuj';
        editButton.addEventListener('click', () => editHospitation(hospitation.id, hospitationDiv));

        header.appendChild(title);
        header.appendChild(date);
        header.appendChild(statusIcon);
        header.appendChild(editButton);
        hospitationDiv.appendChild(header);

        const editContainer = document.createElement('div');
        editContainer.classList.add('edit-container'); // CSS zadba o efekt rozwijania
        hospitationDiv.appendChild(editContainer);

        container.appendChild(hospitationDiv);
    });
}


function editHospitation(id, hospitationDiv) {
    const editContainer = hospitationDiv.querySelector('.edit-container');
    if (editContainer.innerHTML.trim() !== "") {
        if (editContainer.classList.contains('expanded')) {
            editContainer.classList.remove('expanded');
        } else {
            editContainer.classList.add('expanded');
        }
        return;
    }
    showEditFormUsingTemplate(id, hospitationDiv);
}

async function showEditFormUsingTemplate(id, hospitationDiv) {
    const editContainer = hospitationDiv.querySelector('.edit-container');
    editContainer.innerHTML = '';
    try {
        const templateResponse = await fetch('/api/szablon');
        if (!templateResponse.ok) {
            throw new Error("Błąd ładowania szablonu");
        }
        const templateData = await templateResponse.json();

        const form = document.createElement('form');
        form.id = "protocol-form";

        templateData.forEach((section, sectionIndex) => {
            const sectionDiv = document.createElement('div');
            sectionDiv.classList.add('protocol-section');

            const sectionHeader = document.createElement('h3');
            sectionHeader.textContent = section.nazwa;
            sectionDiv.appendChild(sectionHeader);

            if (section.opis) {
                const sectionDesc = document.createElement('p');
                sectionDesc.textContent = section.opis;
                sectionDiv.appendChild(sectionDesc);
            }

            section.info.forEach((item, infoIndex) => {
                const fieldContainer = document.createElement('div');
                fieldContainer.classList.add('protocol-field');

                const label = document.createElement('label');
                label.textContent = item.pytanie;
                label.setAttribute('for', `section${sectionIndex}_field${infoIndex}`);
                fieldContainer.appendChild(label);

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

        const btnSave = document.createElement('button');
        btnSave.textContent = 'Zapisz';
        btnSave.type = 'button';
        btnSave.addEventListener('click', () => {
            saveProtocolTemplate(id, form);
        });

        const btnApprove = document.createElement('button');
        btnApprove.textContent = 'Zatwierdź';
        btnApprove.type = 'button';
        btnApprove.addEventListener('click', () => {
            approveHospitation(id);
        });

        const btnClear = document.createElement('button');
        btnClear.textContent = 'Wyczyść';
        btnClear.type = 'button';
        btnClear.addEventListener('click', () => {
            const inputs = form.querySelectorAll('input[type="text"]');
            inputs.forEach(input => {
                input.value = "";
            });
        });
        
        editContainer.appendChild(btnSave);
        editContainer.appendChild(btnApprove);
        editContainer.appendChild(btnClear);

        editContainer.classList.add('expanded');
    } catch (error) {
        console.error(error);
        alert('Wystąpił błąd podczas ładowania szablonu');
    }
}

function saveProtocolTemplate(id, form) {
    const protocol = [];
    const sectionDivs = form.querySelectorAll('.protocol-section');
    sectionDivs.forEach((sectionDiv) => {
        const section = {};
        section.nazwa = sectionDiv.querySelector('h3').textContent;
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
        const editContainer = form.parentElement;
        editContainer.classList.remove('expanded');
    })
    .catch(error => {
        console.error(error);
        alert('Wystąpił błąd podczas zapisywania protokołu');
    });
}

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
        updateStatusIcon(id);
    } catch (error) {a
        console.error(error);
        alert('Wystąpił błąd podczas zatwierdznia hospitacji');
    }
}

function updateStatusIcon(id) {
    const hospitationDiv = document.querySelector(`.hospitation-item[data-id="${id}"]`);
    if (hospitationDiv) {
        const statusIcon = hospitationDiv.querySelector('.status-icon');
        if (statusIcon) {
            statusIcon.classList.remove('fa-regular', 'fa-square');
            statusIcon.classList.add('fa-solid', 'fa-square-check');
        }
    }
}

window.onload = fetchAssignedHospitations;
