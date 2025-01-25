var protocol = [
  {
    name:"Informacje wstępne",
    desc: "",
    info:[
      {question:"Prowadzący zajęcia/jednostka organizacyjna:", anwser:""},
      {question:"Kod przedmiotu:", anwser:""},
      {question:"Sposób realizacji (tradycyjny, zdalny):", anwser:""}
    ]
  },
  {
    name:"Ocena merytoryczna i metodyczna przeprowadzonych zajęć",
    desc: "5,5 - wzorowa, 5 - bardzo dobra, 4 - dobra, 3 - dostateczna, 2 - negatywna, 0 - nie dotyczy",
    info:[
      {question:"Prowadzący przedstawił temat cel i zakres zajęć", anwser:""},
      {question:"i takie", anwser:""},
      {question:"różne", anwser:""}
    ]
  },
]

function renderProtocol() {
  const container = document.querySelector('.protocol');
  container.innerHTML = '';
  protocol.forEach((section, index) => {
      const sectionElement = document.createElement('div');
      sectionElement.className = 'info-section';
      sectionElement.innerHTML = `
          <div class="info-header">
              <div class="text">
                  <p contenteditable="false" class="section-name">${section.name}</p>
                  <div class="vertical-line"></div>
                  <p contenteditable="false" class="section-desc">${section.desc}</p>
              </div>
              <div class="buttons">
                  <i class="fa-solid fa-arrow-down" onclick="moveSectionDown(${index})"></i>
                  <i class="fa-solid fa-arrow-up" onclick="moveSectionUp(${index})"></i>
                  <i class="fa-solid fa-pen" id="edit-icon-${index}" onclick="toggleEditSection(${index})"></i>
                  <i class="fa-solid fa-trash" onclick="deleteSection(${index})"></i>
              </div>
          </div>
          <div class="info">
              ${section.info.map((item, itemIndex) => `
                  <div class="info-item">
                      <div class="text">
                          <p contenteditable="false">${item.question}</p>
                      </div>
                      <div class="buttons">
                          <i class="fa-solid fa-arrow-down" onclick="moveItemDown(${index}, ${itemIndex})"></i>
                          <i class="fa-solid fa-arrow-up" onclick="moveItemUp(${index}, ${itemIndex})"></i>
                          <i class="fa-solid fa-pen" id="edit-icon-${index}-${itemIndex}" onclick="toggleEditItem(${index}, ${itemIndex})"></i>
                          <i class="fa-solid fa-trash" onclick="deleteItem(${index}, ${itemIndex})"></i>
                      </div>
                  </div>
              `).join('')}
              <i class="fa-solid fa-plus" onclick="addItem(${index})"></i>
          </div>
      `;
      container.appendChild(sectionElement);
  });
}

function toggleEditSection(sectionIndex) {
  const nameElement = document.querySelectorAll('.info-section')[sectionIndex].querySelector('.section-name');
  const descElement = document.querySelectorAll('.info-section')[sectionIndex].querySelector('.section-desc');

  const icon = document.getElementById(`edit-icon-${sectionIndex}`);
  const isEditable = nameElement.contentEditable === "true";

  if (!isEditable) {
    nameElement.contentEditable = descElement.contentEditable = true;
    nameElement.focus();
    icon.classList.replace('fa-pen', 'fa-check');
  } else {
    nameElement.contentEditable = descElement.contentEditable = false;
    protocol[sectionIndex].name = nameElement.innerText.trim();
    protocol[sectionIndex].desc = descElement.innerText.trim();
    icon.classList.replace('fa-check', 'fa-pen');
  }
}

function toggleEditItem(sectionIndex, itemIndex) {
  const element = document.querySelectorAll('.info-section')[sectionIndex].querySelectorAll('.info-item .text p')[itemIndex];
  const icon = document.getElementById(`edit-icon-${sectionIndex}-${itemIndex}`);

  const isEditable = element.contentEditable === "true";

  console.log(isEditable)

  if (!isEditable) {
    console.log('obvious')
    element.contentEditable = true;
    console.log(element.contentEditable)
    element.focus();
    icon.classList.replace('fa-pen', 'fa-check');
  } else {
    element.contentEditable = false;
    protocol[sectionIndex].info[itemIndex].question = element.innerText.trim();
    icon.classList.replace('fa-check', 'fa-pen');
  }
}

function addSection() {
  protocol.push({ name: "-uzupełnij tekst-", desc: "", info: [] });
  renderProtocol();
}

function deleteSection(index) {
  protocol.splice(index, 1);
  renderProtocol();
}

function addItem(sectionIndex) {
  protocol[sectionIndex].info.push({ question: "-uzupełnij tekst-", anwser: "" });
  renderProtocol();
}

function deleteItem(sectionIndex, itemIndex) {
  protocol[sectionIndex].info.splice(itemIndex, 1);
  renderProtocol();
}

function moveSectionUp(index) {
  if (index > 0) {
    [protocol[index], protocol[index - 1]] = [protocol[index - 1], protocol[index]];
    renderProtocol();
  }
}

function moveSectionDown(index) {
  if (index < protocol.length - 1) {
    [protocol[index], protocol[index + 1]] = [protocol[index + 1], protocol[index]];
    renderProtocol();
  }
}

function moveItemUp(sectionIndex, itemIndex) {
  if (itemIndex > 0) {
    [protocol[sectionIndex].info[itemIndex], protocol[sectionIndex].info[itemIndex - 1]] =
      [protocol[sectionIndex].info[itemIndex - 1], protocol[sectionIndex].info[itemIndex]];
    renderProtocol();
  }
}

function moveItemDown(sectionIndex, itemIndex) {
  if (itemIndex < protocol[sectionIndex].info.length - 1) {
    [protocol[sectionIndex].info[itemIndex], protocol[sectionIndex].info[itemIndex + 1]] =
      [protocol[sectionIndex].info[itemIndex + 1], protocol[sectionIndex].info[itemIndex]];
    renderProtocol();
  }
}

window.onload = renderProtocol;