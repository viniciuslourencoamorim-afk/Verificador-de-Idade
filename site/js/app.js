const STORAGE_KEY = "idade-clara.cadastros.v1";

const form = document.querySelector("#person-form");
const nameInput = document.querySelector("#person-name");
const emailInput = document.querySelector("#person-email");
const ageInput = document.querySelector("#person-age");
const formFeedback = document.querySelector("#form-feedback");
const recordsFeedback = document.querySelector("#records-feedback");
const recordCount = document.querySelector("#record-count");
const recordsSummary = document.querySelector("#records-summary");
const recordsBody = document.querySelector("#records-body");
const tableScroll = document.querySelector("#table-scroll");
const emptyState = document.querySelector("#empty-state");
const clearButton = document.querySelector("#clear-button");
const verdictPanel = document.querySelector("#verdict-panel");
const verdictSymbol = document.querySelector("#verdict-symbol");
const verdictTitle = document.querySelector("#verdict-title");
const verdictDescription = document.querySelector("#verdict-description");
const verdictDetails = document.querySelector("#verdict-details");
const verdictName = document.querySelector("#verdict-name");
const verdictEmail = document.querySelector("#verdict-email");
const tabForm = document.querySelector("#tab-form");
const tabRecords = document.querySelector("#tab-records");
const formView = document.querySelector("#form-view");
const recordsView = document.querySelector("#records-view");

let records = [];
let storageError = false;

try {
  const savedRecords = localStorage.getItem(STORAGE_KEY);
  if (savedRecords) {
    const parsedRecords = JSON.parse(savedRecords);
    if (!Array.isArray(parsedRecords)) {
      throw new TypeError("Formato de dados inválido.");
    }
    records = parsedRecords;
  }
} catch {
  storageError = true;
}

function setFeedback(element, message, kind = "") {
  element.textContent = message;
  element.dataset.kind = kind;
}

function collectFormData() {
  const nome = nameInput.value.trim();
  const email = emailInput.value.trim();
  const idadeTexto = ageInput.value.trim();
  const idade = Number(idadeTexto);

  if (!nome) {
    setFeedback(formFeedback, "Informe o nome.", "error");
    nameInput.focus();
    return null;
  }
  if (!email) {
    setFeedback(formFeedback, "Informe o e-mail.", "error");
    emailInput.focus();
    return null;
  }
  if (!emailInput.validity.valid) {
    setFeedback(formFeedback, "Digite um e-mail válido.", "error");
    emailInput.focus();
    return null;
  }
  if (!idadeTexto || !Number.isSafeInteger(idade) || idade < 0 || idade > 130) {
    setFeedback(formFeedback, "Digite uma idade inteira entre 0 e 130.", "error");
    ageInput.focus();
    return null;
  }

  setFeedback(formFeedback, "");
  return { nome, email, idade };
}

function showVerdict(person) {
  const isAdult = person.idade >= 18;
  verdictPanel.classList.toggle("is-adult", isAdult);
  verdictPanel.classList.toggle("is-minor", !isAdult);
  verdictSymbol.textContent = isAdult ? "18+" : "<18";
  verdictTitle.textContent = isAdult ? "Maior de idade" : "Menor de idade";
  verdictDescription.textContent = isAdult
    ? `${person.idade} anos: maioridade atingida.`
    : `${person.idade} anos: abaixo da maioridade.`;
  verdictName.textContent = person.nome;
  verdictEmail.textContent = person.email;
  verdictDetails.hidden = false;
}

function persistRecords(nextRecords) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextRecords));
    records = nextRecords;
    renderRecords();
    return true;
  } catch {
    setFeedback(formFeedback, "Não foi possível salvar neste navegador.", "error");
    return false;
  }
}

function makeRecordId() {
  if (window.crypto && typeof window.crypto.randomUUID === "function") {
    return window.crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function makeCell(text, className = "") {
  const cell = document.createElement("td");
  cell.textContent = text;
  if (className) {
    cell.className = className;
  }
  return cell;
}

function renderRecords() {
  recordCount.textContent = String(records.length);
  recordsSummary.textContent = `${records.length} ${records.length === 1 ? "cadastro" : "cadastros"}`;
  clearButton.hidden = records.length === 0;
  emptyState.hidden = records.length > 0;
  tableScroll.hidden = records.length === 0;
  recordsBody.replaceChildren();

  for (const person of records) {
    const row = document.createElement("tr");
    row.append(
      makeCell(person.nome, "name-cell"),
      makeCell(person.email, "email-cell"),
      makeCell(`${person.idade} anos`, "age-cell"),
    );

    const resultCell = document.createElement("td");
    const badge = document.createElement("span");
    const isAdult = person.idade >= 18;
    badge.className = `result-badge${isAdult ? "" : " is-minor"}`;
    badge.textContent = isAdult ? "Maior" : "Menor";
    resultCell.append(badge);
    row.append(resultCell);

    const actionCell = document.createElement("td");
    const removeButton = document.createElement("button");
    removeButton.className = "remove-record";
    removeButton.type = "button";
    removeButton.textContent = "Excluir";
    removeButton.setAttribute("aria-label", `Excluir cadastro de ${person.nome}`);
    removeButton.addEventListener("click", () => {
      const nextRecords = records.filter((record) => record.id !== person.id);
      if (persistRecords(nextRecords)) {
        setFeedback(recordsFeedback, "Cadastro removido.", "success");
      }
    });
    actionCell.append(removeButton);
    row.append(actionCell);
    recordsBody.append(row);
  }
}

function activateTab(selectedTab) {
  const showRecords = selectedTab === tabRecords;
  tabForm.setAttribute("aria-selected", String(!showRecords));
  tabRecords.setAttribute("aria-selected", String(showRecords));
  tabForm.tabIndex = showRecords ? -1 : 0;
  tabRecords.tabIndex = showRecords ? 0 : -1;
  formView.hidden = showRecords;
  recordsView.hidden = !showRecords;
  if (showRecords) {
    renderRecords();
  }
}

for (const [tab, otherTab] of [[tabForm, tabRecords], [tabRecords, tabForm]]) {
  tab.addEventListener("click", () => activateTab(tab));
  tab.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      otherTab.focus();
      activateTab(otherTab);
    }
  });
}

document.querySelector("#check-button").addEventListener("click", () => {
  const person = collectFormData();
  if (person) {
    showVerdict(person);
  }
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const person = collectFormData();
  if (!person) {
    return;
  }
  if (storageError) {
    setFeedback(formFeedback, "Não foi possível ler os dados locais existentes.", "error");
    return;
  }

  const record = { id: makeRecordId(), ...person };
  if (persistRecords([record, ...records])) {
    showVerdict(person);
    setFeedback(formFeedback, "Cadastro salvo neste navegador.", "success");
    storageError = false;
  }
});

clearButton.addEventListener("click", () => {
  if (records.length && window.confirm("Excluir todos os cadastros salvos neste navegador?")) {
    if (persistRecords([])) {
      setFeedback(recordsFeedback, "Lista limpa.", "success");
    }
  }
});

document.querySelector("#new-record-button").addEventListener("click", () => {
  activateTab(tabForm);
  nameInput.focus();
});

if (storageError) {
  setFeedback(formFeedback, "Não foi possível ler os dados locais existentes.", "error");
  setFeedback(recordsFeedback, "Os dados armazenados parecem inválidos.", "error");
}

renderRecords();
