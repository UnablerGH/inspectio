const hospitationsDate = [
  { name: 'Techniki efektywnego programowania', date: '05/07/2022', status: 'pending' },
  { name: 'Algorytmy i struktury danych', date: '25/01/2022', status: 'pending' },
  { name: 'Techniki efektywnego programowania', date: '02/07/2020', status: 'completed' },
  { name: 'Paradygmaty programowania', date: '08/04/2019', status: 'completed' },
  { name: 'Programowanie strukturalne i obiektowe', date: '10/12/2018', status: 'completed' }
];

function fillHospitations() {
  const container = document.querySelector('.hospitations')

  hospitationsDate.forEach(hospitation => {
      const hospitationDiv = document.createElement('a');
      hospitationDiv.classList.add('hospitation');
      hospitationDiv.href = `/zatwierdzenie-hospitacji/1`

      const name = document.createElement('p');
      name.classList.add('name');
      name.textContent = hospitation.name;

      const date = document.createElement('p');
      date.classList.add('date');
      date.textContent = hospitation.date;

      const icon = document.createElement('i');
      if (hospitation.status === 'pending') {
          icon.classList.add('fa-regular', 'fa-square');
      } else if (hospitation.status === 'completed') {
          icon.classList.add('fa-solid', 'fa-square-check');
      }

      hospitationDiv.appendChild(name);
      hospitationDiv.appendChild(date);
      hospitationDiv.appendChild(icon);

      container.appendChild(hospitationDiv);
  });
}

window.onload = fillHospitations;