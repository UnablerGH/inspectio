const myHospitations = [
    { name: 'Techniki efektywnego programowania', date: '05/07/2022', status: 'pending' },
    { name: 'Algorytmy i struktury danych', date: '25/01/2022', status: 'pending' },
    { name: 'Systemy Operacyjne', date: '17/01/2025', status: 'completed' },
    { name: 'Analiza Matematyczna II', date: '10/02/2025', status: 'completed' }
  ];
  
  function fillMyHospitations() {
    const container = document.querySelector('.hospitations');
    
    myHospitations.forEach(hospitation => {
        const hospitationDiv = document.createElement('a');
        hospitationDiv.classList.add('hospitation');
        hospitationDiv.href = `/zatwierdzenie-hospitacji/1`;
  
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
  
  window.onload = fillMyHospitations;
  