let selecionados = [];

// CARREGAR SERVIÇOS
async function carregarServicos() {
  const response = await fetch("/servicos/");
  const servicos = await response.json();

  renderizarServicos(servicos);
}

// CARREGAR AGENDAMENTOS
async function carregarAgendamentos() {
  const response = await fetch("/agendamentos/");
  const agendamentos = await response.json();

  renderizarAgendamentos(agendamentos);
}

// RENDERIZA SERVIÇOS
function renderizarServicos(servicos) {
  const container = document.getElementById("lista-servicos");
  container.innerHTML = "";

  servicos.forEach(servico => {
    const card = document.createElement("div");
    card.classList.add("card");

    const estaSelecionado = selecionados.some(s => s.id === servico.id);

    if (estaSelecionado) {
      card.classList.add("selecionado");
    }

    card.innerHTML = `
      <h3>${servico.nome}</h3>
      <p>${servico.descricao}</p>
      <p>R$ ${servico.preco.toFixed(2)}</p>
      <p>${servico.duracao} min</p>
      <button>${estaSelecionado ? "Selecionado" : "Selecionar"}</button>
    `;

    const botao = card.querySelector("button");

    botao.addEventListener("click", () => {
      toggleServico(servico);
    });

    container.appendChild(card);
  });
}

// ADICIONA / REMOVE
function toggleServico(servico) {
  const index = selecionados.findIndex(s => s.id === servico.id);

  if (index === -1) {
    selecionados.push(servico);
  } else {
    selecionados.splice(index, 1);
  }

  carregarServicos();
  renderizarSelecionados();
  calcularTotal();
  atualizarResumo();
}

// MOSTRA SELECIONADOS
function renderizarSelecionados() {
  const lista = document.getElementById("servicos-selecionados");
  lista.innerHTML = "";

  selecionados.forEach(s => {
    const li = document.createElement("li");
    li.textContent = `${s.nome} - R$ ${s.preco.toFixed(2)}`;
    lista.appendChild(li);
  });
}

// CALCULA TOTAL
function calcularTotal() {
  let total = 0;

  selecionados.forEach(servico => {
    total += servico.preco;
  });

  document.getElementById("total").textContent = total.toFixed(2);
}

// ATUALIZA DURAÇÃO E QUANTIDADE
function atualizarResumo() {
  let totalDuracao = 0;

  selecionados.forEach(s => {
    totalDuracao += s.duracao;
  });

  document.getElementById("duracao").textContent = totalDuracao;
  document.getElementById("quantidade").textContent = selecionados.length;
}

// CONFIRMAR AGENDAMENTO
async function confirmarAgendamento() {
  const cliente = document.getElementById("cliente").value;

  if (!cliente) {
    alert("Digite o nome do cliente");
    return;
  }

  if (selecionados.length === 0) {
    alert("Selecione pelo menos um serviço");
    return;
  }

  const agendamento = {
    id: Date.now(),
    cliente_nome: cliente,
    servicos: selecionados.map(s => s.id),
    total: selecionados.reduce((soma, s) => soma + s.preco, 0),
    duracao: selecionados.reduce((soma, s) => soma + s.duracao, 0),
    horario: new Date().toLocaleString()
  };

  const response = await fetch("/agendamentos/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(agendamento)
  });

  if (response.ok) {
    document.getElementById("mensagem").textContent = "Agendamento realizado!";

    selecionados = [];
    document.getElementById("cliente").value = "";

    carregarServicos();
    renderizarSelecionados();
    calcularTotal();
    atualizarResumo();
    carregarAgendamentos();
  } else {
    const erro = await response.json();
    document.getElementById("mensagem").textContent = erro.detail;
  }
}

// MOSTRA AGENDAMENTOS
function renderizarAgendamentos(lista) {
  const ul = document.getElementById("lista-agendamentos");
  ul.innerHTML = "";

  lista.forEach(a => {
    const li = document.createElement("li");
    li.textContent = `${a.cliente_nome} - R$ ${a.total.toFixed(2)} - ${a.horario}`;
    ul.appendChild(li);
  });
}

// INICIALIZAÇÃO
carregarServicos();
carregarAgendamentos();
calcularTotal();
atualizarResumo();