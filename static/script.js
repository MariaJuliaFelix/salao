let selecionados = [];
let horarioDisponivel = false;

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
      <p>Preço: R$ ${servico.preco.toFixed(2)}</p>
      <p>Duração: ${servico.duracao} min</p>
      <button>${estaSelecionado ? "Selecionado" : "Selecionar"}</button>
    `;

    const botao = card.querySelector("button");
    botao.addEventListener("click", () => {
      toggleServico(servico);
    });

    container.appendChild(card);
  });
}

// ADICIONA / REMOVE SERVIÇO
function toggleServico(servico) {
  const index = selecionados.findIndex(s => s.id === servico.id);

  if (index === -1) {
    selecionados.push(servico);
  } else {
    selecionados.splice(index, 1);
  }

  horarioDisponivel = false;
  document.getElementById("mensagem").textContent = "";

  carregarServicos();
  renderizarSelecionados();
  calcularTotal();
  atualizarResumo();
}

// MOSTRA SELECIONADOS
function renderizarSelecionados() {
  const lista = document.getElementById("servicos-selecionados");
  lista.innerHTML = "";

  selecionados.forEach(servico => {
    const li = document.createElement("li");
    li.textContent = `${servico.nome} - R$ ${servico.preco.toFixed(2)} - ${servico.duracao} min`;
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

  selecionados.forEach(servico => {
    totalDuracao += servico.duracao;
  });

  document.getElementById("duracao").textContent = totalDuracao;
  document.getElementById("quantidade").textContent = selecionados.length;
}

// VERIFICAR DISPONIBILIDADE
async function verificarDisponibilidade() {
  const data = document.getElementById("data").value;
  const horario = document.getElementById("horario").value;

  if (!data || !horario) {
    alert("Preencha a data e o horário");
    return;
  }

  const response = await fetch(`/agendamentos/disponibilidade?data=${data}&horario=${horario}`);
  const resultado = await response.json();

  const mensagem = document.getElementById("mensagem");

  if (resultado.disponivel) {
    horarioDisponivel = true;
    mensagem.textContent = "Horário disponível";
  } else {
    horarioDisponivel = false;
    mensagem.textContent = "Horário indisponível";
  }
}

// CONFIRMAR AGENDAMENTO
async function confirmarAgendamento() {
  const cliente = document.getElementById("cliente").value;
  const data = document.getElementById("data").value;
  const horario = document.getElementById("horario").value;

  if (!cliente) {
    alert("Digite o nome do cliente");
    return;
  }

  if (selecionados.length === 0) {
    alert("Selecione pelo menos um serviço");
    return;
  }

  if (!data || !horario) {
    alert("Preencha a data e o horário");
    return;
  }

  if (!horarioDisponivel) {
    alert("Verifique a disponibilidade antes de confirmar");
    return;
  }

  const agendamento = {
    id: Date.now(),
    cliente_nome: cliente,
    servicos: selecionados.map(s => s.id),
    total: selecionados.reduce((soma, s) => soma + s.preco, 0),
    duracao: selecionados.reduce((soma, s) => soma + s.duracao, 0),
    data: data,
    horario: horario
  };

  const response = await fetch("/agendamentos/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(agendamento)
  });

  const mensagem = document.getElementById("mensagem");

  if (response.ok) {
    mensagem.textContent = "Agendamento realizado com sucesso";

    selecionados = [];
    horarioDisponivel = false;

    document.getElementById("cliente").value = "";
    document.getElementById("data").value = "";
    document.getElementById("horario").value = "";

    carregarServicos();
    renderizarSelecionados();
    calcularTotal();
    atualizarResumo();
    carregarAgendamentos();
  } else {
    const erro = await response.json();
    mensagem.textContent = erro.detail;
  }
}

// MOSTRA AGENDAMENTOS
function renderizarAgendamentos(lista) {
  const ul = document.getElementById("lista-agendamentos");
  ul.innerHTML = "";

  lista.forEach(a => {
    const li = document.createElement("li");
    li.textContent = `${a.cliente_nome} - ${a.data} às ${a.horario} - R$ ${a.total.toFixed(2)} - ${a.duracao} min`;
    ul.appendChild(li);
  });
}

// INICIALIZAÇÃO
carregarServicos();
carregarAgendamentos();
calcularTotal();
atualizarResumo();