var protocol = [
  {
    "name": "Informacje wstępne",
    "desc": "",
    "info": [
      {
        "question": "Prowadzący zajęcia jednostka organizacyjna:",
        "answer": "Jan Kowalski"
      },
      {
        "question": "Kod przedmiotu:",
        "answer": "W041ST-S10018L"
      },
      {
        "question": "Sposób realizacji (tradycyjny, zdalny):",
        "answer": "tradycyjny"
      }
    ]
  },
  {
    "name": "Ocena formalna zajęć",
    "desc": "",
    "info": [
      {
        "question": "Czy zajęcia zaczęły się punktualnie (tak, nie, ile spóźnienia):",
        "answer": "5 minut spóźnienia"
      },
      {
        "question": "Czy sprawdzono obecność studentów. Jeżeli tak podać liczbę obecnych:",
        "answer": "tak, 14 obecnych"
      },
      {
        "question": "Czy sala i jej wyposażenie są przystosowane do formy prowadzonych zajęć. Jeżeli nie to z jakich powodów:",
        "answer": "tak"
      }
    ]
  },
  {
    "name": "Ocena merytoryczna i metodyczna przeprowadzonych zajęć",
    "desc": "5,5 - wzorowa, 5 - bardzo dobra, 4 - dobra, 3 - dostateczna, 2 - negatywna, 0 - nie dotyczy",
    "info": [
      {
        "question": "Fajność",
        "answer": "5,5"
      }
    ]
  }
];

function renderProtocol() {
    const container = document.querySelector('.protocol')

    const ol = document.createElement('ol');

    protocol.forEach((section) => {
        const sectionItem = document.createElement('li');
        
        const sectionHeader = document.createElement('strong');
        sectionHeader.innerText = section.name;
        const sectionDesc = section.desc ? document.createElement('span') : null;
        if (sectionDesc) {
            sectionDesc.innerText = section.desc;
        }
        
        sectionItem.appendChild(sectionHeader);
        sectionItem.appendChild(document.createElement('br')); // Add a line break after the section name
        
        if (sectionDesc) {
            sectionItem.appendChild(sectionDesc);
            sectionItem.appendChild(document.createElement('br')); // Add a line break after the description
        }

        const innerOl = document.createElement('ol');
        section.info.forEach((item) => {
            const li = document.createElement('li');
            li.innerHTML = `${item.question} <br/> <span class="response">${item.answer}</span>`;
            innerOl.appendChild(li);
        });

        sectionItem.appendChild(innerOl);
        ol.appendChild(sectionItem);
    });

    container.appendChild(ol);
}


renderProtocol();