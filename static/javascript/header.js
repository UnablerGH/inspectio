const userId = localStorage.getItem('userId');

async function updateHeader() {
  try {
    const response = await fetch(`/api/pracownik/${userId}`);

    if (!response.ok) {
      throw new Error('Błąd przy pobieraniu danych');
    }

    const data = await response.json();

    if (data.imie) {
      document.querySelector('.account-bar p').textContent = data.imie + " " + data.nazwisko;
    } else {
      console.error('Nie znaleziono imienia w danych');
    }
  } catch (error) {
    console.error('Błąd przy pobieraniu danych:', error);
  }
}

updateHeader();