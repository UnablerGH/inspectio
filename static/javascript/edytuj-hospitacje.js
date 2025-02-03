const hospitacjaId = 1;

async function fetchHospitationDetails(id) {
    try {
        const response = await fetch(`/api/hospitacja/${id}`);
        if (!response.ok) {
            throw new Error('Błąd pobierania szczegółów hospitacji');
        }
        const data = await response.json();
        populateHospitationEditor(data);
    } catch (e) {
        console.error(e);
    }
}

function populateHospitationEditor(data) {
    document.getElementById('hospitacja-id').textContent = data.id_hospitacji;
    document.getElementById('hospitacja-termin').textContent = data.termin;
    
    const editor = document.getElementById('protocol-editor');
    try {
        const protocolObj = JSON.parse(data.protokol);
        editor.value = JSON.stringify(protocolObj, null, 4);
    } catch (e) {
        editor.value = data.protokol;
    }
}

async function saveProtocol(id) {
    const editor = document.getElementById('protocol-editor');
    let newProtocol;
    try {
        newProtocol = JSON.parse(editor.value);
    } catch (e) {
        alert('Nieprawidłowy format JSON w protokole!');
        return;
    }
    try {
        const response = await fetch(`/api/hospitacja/${id}/zapisz`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ protocol: newProtocol })
        });
        if (!response.ok) {
            throw new Error('Błąd zapisu protokołu');
        }
        const result = await response.json();
        alert(result.message);
    } catch (e) {
        console.error(e);
        alert('Wystąpił błąd podczas zapisywania protokołu');
    }
}

async function acceptHospitation(id) {
    try {
        const response = await fetch(`/api/hospitacja/${id}/zaakceptuj`, {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error('Błąd zatwierdzania hospitacji');
        }
        const result = await response.json();
        alert(result.message);
    } catch (e) {
        console.error(e);
        alert('Wystąpił błąd podczas zatwierdzania hospitacji');
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
        fetchHospitationDetails(id);
    })
    .catch(error => {
        console.error(error);
        alert('Wystąpił błąd podczas zapisywania protokołu');
    });
}


function cancelEditing(id) {
    fetchHospitationDetails(id);
}

document.getElementById('btn-zapisz').addEventListener('click', () => saveProtocol(hospitacjaId));
document.getElementById('btn-zatwierdz').addEventListener('click', () => acceptHospitation(hospitacjaId));
document.getElementById('btn-anuluj').addEventListener('click', () => cancelEditing(hospitacjaId));

window.addEventListener('DOMContentLoaded', () => {
    fetchHospitationDetails(hospitacjaId);
});
