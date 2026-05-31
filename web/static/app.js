const examples = {
  valid: `$ Isso e um comentario
DEFINIR(bpm, 120);
DEFINIR(volume, 80);
REPETIR(4) {
    NOTA(C, 500);
    ESPERAR(250);
    NOTA(E, 500);
}
`,
  lexical: `NOTA(C, 500);
@`,
  syntax: `DEFINIR(bpm, 120);
NOTA(C, 500)
ESPERAR(250);
`,
  semantic: `DEFINIR(bpm, 500);
DEFINIR(pin, 8);
DEFINIR(pin, 9);
REPETIR(0) {
}
`,
};

const codeInput = document.querySelector("#codeInput");
const compileButton = document.querySelector("#compileButton");
const exampleSelect = document.querySelector("#exampleSelect");
const statusBox = document.querySelector("#status");
const tokensBody = document.querySelector("#tokensBody");
const astOutput = document.querySelector("#astOutput");
const symbolsOutput = document.querySelector("#symbolsOutput");
const errorsOutput = document.querySelector("#errorsOutput");
const arduinoOutput = document.querySelector("#arduinoOutput");

function formatValue(value) {
  if (value === null || value === undefined) {
    return "EOF";
  }
  return String(value);
}

function renderTokens(tokens) {
  tokensBody.innerHTML = "";

  tokens.forEach((token) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><code>${token.tipo}</code></td>
      <td>${formatValue(token.valor)}</td>
      <td>${token.linha}</td>
      <td>${token.coluna}</td>
    `;
    tokensBody.appendChild(row);
  });
}

function renderErrors(errors) {
  errorsOutput.innerHTML = "";

  if (errors.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "Nenhum erro encontrado.";
    errorsOutput.appendChild(empty);
    return;
  }

  errors.forEach((error) => {
    const item = document.createElement("article");
    item.className = `error-card ${error.tipo.toLowerCase()}`;
    item.innerHTML = `
      <strong>${error.tipo}</strong>
      <span>Linha ${error.linha}${error.coluna ? `, coluna ${error.coluna}` : ""}</span>
      <p>${error.mensagem}</p>
    `;
    errorsOutput.appendChild(item);
  });
}

function renderResult(result) {
  renderTokens(result.tokens);
  astOutput.textContent = JSON.stringify(result.ast, null, 2);
  symbolsOutput.textContent = JSON.stringify(result.tabela_simbolos, null, 2);
  arduinoOutput.textContent = result.codigo_arduino || "";
  renderErrors(result.erros);

  statusBox.textContent = result.sucesso
    ? "Compilação concluída sem erros."
    : `Compilação concluída com ${result.erros.length} erro(s).`;
  statusBox.className = result.sucesso ? "status success" : "status failure";
}

async function compileCode() {
  compileButton.disabled = true;
  statusBox.textContent = "Compilando...";
  statusBox.className = "status";

  try {
    const response = await fetch("/compilar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo: codeInput.value }),
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.erro || "Falha ao compilar.");
    }

    renderResult(result);
  } catch (error) {
    statusBox.textContent = error.message;
    statusBox.className = "status failure";
  } finally {
    compileButton.disabled = false;
  }
}

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
    document
      .querySelectorAll(".tab-content")
      .forEach((content) => content.classList.remove("active"));

    button.classList.add("active");
    document.querySelector(`#${button.dataset.tab}`).classList.add("active");
  });
});

exampleSelect.addEventListener("change", () => {
  codeInput.value = examples[exampleSelect.value];
  compileCode();
});

compileButton.addEventListener("click", compileCode);
compileCode();
