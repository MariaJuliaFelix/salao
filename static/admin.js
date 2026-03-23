let agendamentoEditando = null;

async function carregarAgendamentos() {
  const res = await fetch("/agendamentos/");
  const lista = await res.json();

  const ul = document.getElementById("lista-agendamentos");
  ul.innerHTML = "";

  lista.forEach(a => {
    const li = document.createElement("li");

    li.innerHTML = `
      <strong>${a.cliente_nome}</strong> - ${a.data} ${a.horario}
      <br>Status: ${a.status}
      <br>
      <button onclick="editar(${a.id})">Editar</button>
      <button onclick="confirmar(${a.id})">Confirmar</button>
    `;

    ul.appendChild(li);
  });
}

async function editar(id) {
  const res = await fetch(`/agendamentos/${id}`);
  const a = await res.json();

  agendamentoEditando = id;

  document.getElementById("edit-cliente").value = a.cliente_nome;
  document.getElementById("edit-data").value = a.data;
  document.getElementById("edit-horario").value = a.horario;
}

async function salvarEdicao() {
  if (!agendamentoEditando) return;

  const cliente = document.getElementById("edit-cliente").value;
  const data = document.getElementById("edit-data").value;
  const horario = document.getElementById("edit-horario").value;

  await fetch(`/agendamentos/${agendamentoEditando}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      cliente_nome: cliente,
      servicos: [1], // simples (nível junior)
      data,
      horario
    })
  });

  alert("Atualizado!");

  agendamentoEditando = null;
  carregarAgendamentos();
}

async function confirmar(id) {
  await fetch(`/agendamentos/${id}/confirmar`, {
    method: "PATCH"
  });

  carregarAgendamentos();
}

async function buscarHistorico() {
  const inicio = document.getElementById("data-inicio").value;
  const fim = document.getElementById("data-fim").value;

  const res = await fetch(`/agendamentos/historico?data_inicio=${inicio}&data_fim=${fim}`);
  const lista = await res.json();

  const ul = document.getElementById("lista-historico");
  ul.innerHTML = "";

  lista.forEach(a => {
    const li = document.createElement("li");
    li.innerHTML = `${a.cliente_nome} - ${a.data}`;
    ul.appendChild(li);
  });
}

async function carregarResumo() {
  const res = await fetch("/gerencial/desempenho-semanal");
  const dados = await res.json();

  document.getElementById("resumo-gerencial").innerHTML = `
    <p>Total: ${dados.total_agendamentos}</p>
    <p>Faturamento: R$ ${dados.faturamento_total}</p>
  `;
}

carregarAgendamentos();
carregarResumo();