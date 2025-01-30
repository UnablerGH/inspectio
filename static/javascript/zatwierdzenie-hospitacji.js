async function fetchHospitacjaDetails(id) {
  try {
      const response = await fetch(`/api/hospitacja/${id}`);
      if (!response.ok) {
          throw new Error('Błąd pobierania danych');
      }
      const data = await response.json();
      renderHospitacjaDetails(data);
      renderProtocol(data);
      setupButton(id, data.status);  // Przekazanie statusu do setupButton
  } catch (error) {
      console.error('Błąd:', error);
  }
}

function renderHospitacjaDetails(hospitacja) {
  const leftDiv = document.querySelector('.left');
  const rightDiv = document.querySelector('.right');

  // Tworzymy jedno p dla danych w lewej sekcji
  leftDiv.innerHTML = `
      <p>${hospitacja.przedmiot_nazwa} <br/>
      ${hospitacja.przedmiot_kod} <br/>
      Zespół hospitujący: ${hospitacja.zespol_hospitujacy.join(', ')}</p>
  `;

  // Tworzymy jedno p dla danych w prawej sekcji
  rightDiv.innerHTML = `
      <p>${hospitacja.termin} <br/>
      ${hospitacja.miejsce}</p>
      <button>${hospitacja.status === 'completed' ? 'Zatwierdzono' : 'Zatwierdź'}</button>
  `;
}

async function setupButton(id, status) {
  const button = document.querySelector('.right button');
  
  if (status === 'completed') {
      button.classList.add('accepted');
      button.disabled = true; 
  } else {
      button.classList.remove('accepted');
      button.disabled = false;

      // Dodanie event listener do przycisku
      button.addEventListener('click', async () => {
        try {
            const response = await fetch(`/api/hospitacja/${id}/zaakceptuj`, {
                method: 'POST',
            });

            if (response.ok) {
                button.classList.add('accepted');
                button.disabled = true;
                button.textContent = 'Zatwierdzono';  // Zmieniamy tekst na "Zatwierdzono"
            } else {
                throw new Error('Nie udało się zaakceptować hospitacji');
            }
        } catch (error) {
            console.error('Błąd przy akceptacji hospitacji:', error);
        }
      });
  }
}

function renderProtocol(hospitacja) {
  const container = document.querySelector('.protocol');

  const protocol = JSON.parse(hospitacja.protokol);

  const ol = document.createElement('ol');

  protocol.forEach((section) => {
      const sectionItem = document.createElement('li');
      
      const sectionHeader = document.createElement('strong');
      sectionHeader.innerText = section.nazwa;
      const sectionopis = section.opis ? document.createElement('span') : null;
      if (sectionopis) {
          sectionopis.innerText = section.opis;
      }
      
      sectionItem.appendChild(sectionHeader);
      sectionItem.appendChild(document.createElement('br'));
      
      if (sectionopis) {
          sectionItem.appendChild(sectionopis);
          sectionItem.appendChild(document.createElement('br'));
      }

      const innerOl = document.createElement('ol');
      section.info.forEach((item) => {
          const li = document.createElement('li');
          li.innerHTML = `${item.pytanie} <br/> <span class="response">${item.odpowiedz}</span>`;
          innerOl.appendChild(li);
      });

      sectionItem.appendChild(innerOl);
      ol.appendChild(sectionItem);
  });

  container.appendChild(ol);
}

const hospitacjaId = document.querySelector('.info').getAttribute('data-hospitacja-id');
fetchHospitacjaDetails(hospitacjaId);