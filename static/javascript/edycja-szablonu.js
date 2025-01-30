var protocol = []

async function loadProtocol() {
  try {
    const response = await fetch('/api/szablon');
    const data = await response.json();
    protocol = data;
  } catch (error) {
    console.error('Błąd podczas pobierania szablonu:', error);
  }
}

async function saveProtocol() {
  try {
    const response = await fetch('/api/szablon', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(protocol) 
    });
    if (response.status === 201) {
      return true; 
    } else {
      throw new Error('Nie udało się zapisać zmian');
    }
  } catch (error) {
    console.error('Błąd podczas zapisywania szablonu:', error);
    return false;
  }
}

function renderProtocol() {
  const container = document.querySelector('.protocol');
  container.innerHTML = '';
  protocol.forEach((section, index) => {
      const sectionElement = document.createElement('div');
      sectionElement.className = 'info-section';
      sectionElement.innerHTML = `
          <div class="info-header">
              <div class="text">
                  <p contenteditable="false" class="section-name">${section.nazwa}</p>
                  <div class="vertical-line"></div>
                  <p contenteditable="false" class="section-desc">${section.opis}</p>
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
                          <p contenteditable="false">${item.pytanie}</p>
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

async function initialize() {
  await loadProtocol();
  renderProtocol();
}

async function toggleEditSection(sectionIndex) {
  const nameElement = document.querySelectorAll('.info-section')[sectionIndex].querySelector('.section-name');
  const descElement = document.querySelectorAll('.info-section')[sectionIndex].querySelector('.section-desc');

  const icon = document.getElementById(`edit-icon-${sectionIndex}`);
  const isEditable = nameElement.contentEditable === "true";

  if (!isEditable) {
    nameElement.contentEditable = descElement.contentEditable = true;
    nameElement.focus();
    icon.classList.replace('fa-pen', 'fa-check');
  } else {
    if(await saveProtocol()) {
      protocol[sectionIndex].nazwa = nameElement.innerText.trim()
      protocol[sectionIndex].opis = descElement.innerText.trim()
    } else {
      nameElement.innerText = protocol[sectionIndex].nazwa;
      descElement.innerText = protocol[sectionIndex].opis;
    }
    nameElement.contentEditable = descElement.contentEditable = false;
    icon.classList.replace('fa-check', 'fa-pen');
  }
}

async function toggleEditItem(sectionIndex, itemIndex) {
  const element = document.querySelectorAll('.info-section')[sectionIndex].querySelectorAll('.info-item .text p')[itemIndex];
  const icon = document.getElementById(`edit-icon-${sectionIndex}-${itemIndex}`);

  const isEditable = element.contentEditable === "true";

  if (!isEditable) {
    element.contentEditable = true;
    element.focus();
    icon.classList.replace('fa-pen', 'fa-check');
  } else {
    await saveProtocol() ?
      protocol[sectionIndex].info[itemIndex].pytanie = element.innerText.trim() :
      element.innerText = protocol[sectionIndex].info[itemIndex].pytanie;
    element.contentEditable = false;
    icon.classList.replace('fa-check', 'fa-pen');
  }
}

async function addSection() {
  protocol.push({ nazwa: "-uzupełnij tekst-", opis: "", info: [] });
  if(await saveProtocol()) {
    renderProtocol();
  }
}

async function deleteSection(index) {
  protocol.splice(index, 1);
  if(await saveProtocol()) {
    renderProtocol();
  }
}

async function addItem(sectionIndex) {
  protocol[sectionIndex].info.push({ pytanie: "-uzupełnij tekst-", odpowiedz: "" });
  if(await saveProtocol()) {
    renderProtocol();
  }
}

async function deleteItem(sectionIndex, itemIndex) {
  protocol[sectionIndex].info.splice(itemIndex, 1);
  if(await saveProtocol()) {
    renderProtocol();
  }
}

async function moveSectionUp(index) {
  if (index > 0) {
    [protocol[index], protocol[index - 1]] = [protocol[index - 1], protocol[index]];
    if(await saveProtocol()) {
      renderProtocol();
    }
  }
}

async function moveSectionDown(index) {
  if (index < protocol.length - 1) {
    [protocol[index], protocol[index + 1]] = [protocol[index + 1], protocol[index]];
    if(await saveProtocol()) {
      renderProtocol();
    }
  }
}

async function moveItemUp(sectionIndex, itemIndex) {
  if (itemIndex > 0) {
    [protocol[sectionIndex].info[itemIndex], protocol[sectionIndex].info[itemIndex - 1]] =
      [protocol[sectionIndex].info[itemIndex - 1], protocol[sectionIndex].info[itemIndex]];
    if(await saveProtocol()) {
      renderProtocol();
    }
  }
}

async function moveItemDown(sectionIndex, itemIndex) {
  if (itemIndex < protocol[sectionIndex].info.length - 1) {
    [protocol[sectionIndex].info[itemIndex], protocol[sectionIndex].info[itemIndex + 1]] =
      [protocol[sectionIndex].info[itemIndex + 1], protocol[sectionIndex].info[itemIndex]];
    if(await saveProtocol()) {
      renderProtocol();
    }
  }
}

window.onload = initialize;