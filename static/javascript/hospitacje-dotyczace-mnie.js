async function fetchHospitations() {
    try {
        const response = await fetch(`/api/hospitacje/${userId}`);
        if (!response.ok) {
            throw new Error('Błąd pobierania danych');
        }
        const hospitationData = await response.json();
        fillHospitations(hospitationData);
    } catch (error) {
        console.error('Błąd:', error);
    }
}

function fillHospitations(hospitationData) {
    const container = document.querySelector('.hospitations');
    container.innerHTML = ''; // Czyści poprzednie dane

    hospitationData.forEach(hospitation => {
        const hospitationDiv = document.createElement('a');
        hospitationDiv.classList.add('hospitation');
        hospitationDiv.href = `/zatwierdzenie-hospitacji/${hospitation.id}`;

        const nazwa = document.createElement('p');
        nazwa.classList.add('name');
        nazwa.textContent = hospitation.nazwa;

        const data = document.createElement('p');
        data.classList.add('date');
        data.textContent = hospitation.termin;  // Use termin here

        const icon = document.createElement('i');
        if (hospitation.status === 'completed') {
            icon.classList.add('fa-solid', 'fa-square-check');
        } else {
            icon.classList.add('fa-regular', 'fa-square');
        }

        hospitationDiv.appendChild(nazwa);
        hospitationDiv.appendChild(data);
        hospitationDiv.appendChild(icon);

        container.appendChild(hospitationDiv);
    });
}

window.onload = fetchHospitations;