let selecionados = [];
let horarioDisponivel = false;

function mostrarMensagem(texto, tipo = "info") {
  const mensagem = document.getElementById("mensagem");
  mensagem.className = `mensagem ${tipo}`;

  const icones = {
    sucesso: "✔",
    erro: "✖",
    aviso: "⚠",
    info: "ℹ"
  };

  mensagem.innerHTML = `${icones[tipo] || "ℹ"} ${texto}`;
}

function limparMensagem() {
  const mensagem = document.getElementById("mensagem");
  mensagem.className = "mensagem";
  mensagem.textContent = "";
}

function formatarMoeda(valor) {
  return Number(valor).toFixed(2);
}

function badgeStatus(status) {
  return `<span class="badge ${status}">${status.replace("_", " ")}</span>`;
}

async function carregarServicos() {
  try {
    const response = await fetch("/servicos/");
    const servicos = await response.json();
    renderizarServicos(servicos);
  } catch (error) {
    mostrarMensagem("Erro ao carregar serviços", "erro");
  }
}

async function carregarAgendamentos() {
  try {
    const response = await fetch("/agendamentos/");
    const agendamentos = await response.json();
    renderizarAgendamentos(agendamentos);
  } catch (error) {
    mostrarMensagem("Erro ao carregar agendamentos", "erro");
  }
}

async function carregarResumoGerencial() {
  try {
    const response = await fetch("/gerencial/desempenho-semanal");
    const dados = await response.json();

    const container = document.getElementById("resumo-gerencial");

    container.innerHTML = `
      <div class="resumo-grid">
        <div class="resumo-box">
          <span>Período</span>
          <strong>${dados.periodo.inicio} até ${dados.periodo.fim}</strong>
        </div>
        <div class="resumo-box">
          <span>Agendamentos</span>
          <strong>${dados.total_agendamentos}</strong>
        </div>
        <div class="resumo-box">
          <span>Faturamento</span>
          <strong>R$ ${formatarMoeda(dados.faturamento_total)}</strong>
        </div>
      </div>

      <div class="detalhes-card" style="margin-top: 15px;">
        <p><strong>Cancelados:</strong> ${dados.total_cancelados}</p>
        <p><strong>Serviços mais solicitados:</strong></p>
        <ul>
          ${
            dados.servicos_mais_solicitados.length > 0
              ? dados.servicos_mais_solicitados
                  .map(servico => `<li>${servico.nome} - ${servico.quantidade}</li>`)
                  .join("")
              : "<li>Nenhum serviço registrado nesta semana.</li>"
          }
        </ul>
      </div>
    `;
  } catch (error) {
    const container = document.getElementById("resumo-gerencial");
    container.innerHTML = `<div class="detalhes-card">Não foi possível carregar o resumo semanal.</div>`;
  }
}

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
      <div class="topo-card-servico">
        <h3>${servico.nome}</h3>
        <span class="tag-preco">R$ ${formatarMoeda(servico.preco)}</span>
      </div>

      <p class="descricao-servico">${servico.descricao}</p>

      <div class="info-servico">
        <span>⏱ ${servico.duracao} min</span>
      </div>

      <button>${estaSelecionado ? "Remover serviço" : "Selecionar serviço"}</button>
    `;

    card.querySelector("button").addEventListener("click", () => {
      toggleServico(servico);
    });

    container.appendChild(card);
  });
}

function toggleServico(servico) {
  const index = selecionados.findIndex(s => s.id === servico.id);

  if (index === -1) {
    selecionados.push(servico);
  } else {
    selecionados.splice(index, 1);
  }

  horarioDisponivel = false;
  limparMensagem();

  renderizarSelecionados();
  calcularTotal();
  atualizarResumo();
  carregarServicos();
}

function renderizarSelecionados() {
  const lista = document.getElementById("servicos-selecionados");
  lista.innerHTML = "";

  if (selecionados.length === 0) {
    lista.innerHTML = `<li>Nenhum serviço selecionado.</li>`;
    return;
  }

  selecionados.forEach(servico => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${servico.nome}</strong> - 
      R$ ${formatarMoeda(servico.preco)} - 
      ${servico.duracao} min
    `;
    lista.appendChild(li);
  });
}

function calcularTotal() {
  const total = selecionados.reduce((soma, servico) => soma + Number(servico.preco), 0);
  document.getElementById("total").textContent = total.toFixed(2);
}

function atualizarResumo() {
  const totalDuracao = selecionados.reduce((soma, servico) => soma + Number(servico.duracao), 0);
  document.getElementById("duracao").textContent = totalDuracao;
  document.getElementById("quantidade").textContent = selecionados.length;
}

async function verificarDisponibilidade() {
  const data = document.getElementById("data").value;
  const horario = document.getElementById("horario").value;
  const duracao = selecionados.reduce((soma, s) => soma + Number(s.duracao), 0);

  if (!data || !horario) {
    mostrarMensagem("Preencha a data e o horário", "aviso");
    return;
  }

  if (selecionados.length === 0) {
    mostrarMensagem("Selecione pelo menos um serviço", "aviso");
    return;
  }

  try {
    const response = await fetch(`/agendamentos/disponibilidade?data=${data}&horario=${horario}&duracao=${duracao}`);
    const resultado = await response.json();

    if (resultado.disponivel) {
      horarioDisponivel = true;
      mostrarMensagem("Horário disponível para esse agendamento", "sucesso");
    } else {
      horarioDisponivel = false;
      mostrarMensagem("Horário indisponível para essa duração", "erro");
    }
  } catch (error) {
    horarioDisponivel = false;
    mostrarMensagem("Erro ao verificar disponibilidade", "erro");
  }
}

async function confirmarAgendamento() {
  const cliente = document.getElementById("cliente").value.trim();
  const data = document.getElementById("data").value;
  const horario = document.getElementById("horario").value;
  const observacao = document.getElementById("observacao").value.trim();
  const botao = document.querySelector("button.primary");

  if (!cliente) {
    mostrarMensagem("Digite o nome do cliente", "aviso");
    return;
  }

  if (selecionados.length === 0) {
    mostrarMensagem("Selecione pelo menos um serviço", "aviso");
    return;
  }

  if (!data || !horario) {
    mostrarMensagem("Preencha a data e o horário", "aviso");
    return;
  }

  if (!horarioDisponivel) {
    mostrarMensagem("Verifique a disponibilidade antes de confirmar", "aviso");
    return;
  }

  const agendamento = {
    cliente_nome: cliente,
    servicos: selecionados.map(s => s.id),
    data: data,
    horario: horario,
    observacao: observacao || null
  };

  botao.disabled = true;
  botao.textContent = "Enviando...";

  try {
    const response = await fetch("/agendamentos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(agendamento)
    });

    const resultado = await response.json();

    if (response.ok) {
      let texto = "Agendamento realizado com sucesso";

      if (resultado.sugestao_mesma_data) {
        texto += ` | Sugestão: a cliente já teve agendamento nesta semana em ${resultado.sugestao_mesma_data}`;
      }

      mostrarMensagem(texto, "sucesso");

      selecionados = [];
      horarioDisponivel = false;

      document.getElementById("cliente").value = "";
      document.getElementById("data").value = "";
      document.getElementById("horario").value = "";
      document.getElementById("observacao").value = "";

      renderizarSelecionados();
      calcularTotal();
      atualizarResumo();
      carregarServicos();
      carregarAgendamentos();
      carregarResumoGerencial();
    } else {
      mostrarMensagem(resultado.detail || "Erro ao criar agendamento", "erro");
    }
  } catch (error) {
    mostrarMensagem("Erro inesperado ao criar agendamento", "erro");
  } finally {
    botao.disabled = false;
    botao.textContent = "Confirmar";
  }
}

function renderizarAgendamentos(lista) {
  const ul = document.getElementById("lista-agendamentos");
  ul.innerHTML = "";

  if (lista.length === 0) {
    ul.innerHTML = "<li>Nenhum agendamento encontrado.</li>";
    return;
  }

  lista.forEach(a => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="linha-agendamento">
        <div>
          <strong>${a.cliente_nome}</strong><br>
          ${a.data} às ${a.horario}<br>
          R$ ${formatarMoeda(a.total)} • ${a.duracao} min • ${badgeStatus(a.status)}
        </div>
        <div class="acoes-lista">
          <button onclick="verDetalhes(${a.id})">Detalhes</button>
          <button onclick="confirmarAgendamentoExistente(${a.id})">Confirmar</button>
        </div>
      </div>
    `;
    ul.appendChild(li);
  });
}

async function verDetalhes(id) {
  try {
    const response = await fetch(`/agendamentos/${id}`);
    const agendamento = await response.json();

    const container = document.getElementById("detalhes-agendamento");

    container.innerHTML = `
      <div class="detalhes-card">
        <p><strong>ID:</strong> ${agendamento.id}</p>
        <p><strong>Cliente:</strong> ${agendamento.cliente_nome}</p>
        <p><strong>Data:</strong> ${agendamento.data}</p>
        <p><strong>Horário:</strong> ${agendamento.horario}</p>
        <p><strong>Total:</strong> R$ ${formatarMoeda(agendamento.total)}</p>
        <p><strong>Duração:</strong> ${agendamento.duracao} min</p>
        <p><strong>Status:</strong> ${badgeStatus(agendamento.status)}</p>
        <p><strong>Observação:</strong> ${agendamento.observacao || "Sem observação"}</p>

        <div style="margin-top: 12px;">
          <strong>Serviços:</strong>
          <ul style="margin-top: 8px;">
            ${agendamento.servicos.map(servico => `
              <li style="margin-bottom: 10px;">
                <div style="margin-bottom: 6px;">
                  ${servico.nome} - ${badgeStatus(servico.status)}
                </div>
                <select onchange="alterarStatusServico(${agendamento.id}, ${servico.id}, this.value)">
                  <option value="">Alterar status</option>
                  <option value="pendente">pendente</option>
                  <option value="confirmado">confirmado</option>
                  <option value="em_andamento">em_andamento</option>
                  <option value="concluido">concluido</option>
                  <option value="cancelado">cancelado</option>
                </select>
              </li>
            `).join("")}
          </ul>
        </div>
      </div>
    `;
  } catch (error) {
    mostrarMensagem("Erro ao carregar detalhes do agendamento", "erro");
  }
}

async function confirmarAgendamentoExistente(id) {
  try {
    const response = await fetch(`/agendamentos/${id}/confirmar`, {
      method: "PATCH"
    });

    if (response.ok) {
      mostrarMensagem("Agendamento confirmado com sucesso", "sucesso");
      await carregarAgendamentos();
      await carregarResumoGerencial();
      await verDetalhes(id);
    } else {
      const erro = await response.json();
      mostrarMensagem(erro.detail || "Erro ao confirmar agendamento", "erro");
    }
  } catch (error) {
    mostrarMensagem("Erro ao confirmar agendamento", "erro");
  }
}

async function alterarStatusServico(agendamentoId, servicoId, status) {
  if (!status) return;

  try {
    const response = await fetch(`/agendamentos/${agendamentoId}/servicos/${servicoId}/status`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ status })
    });

    if (response.ok) {
      mostrarMensagem("Status do serviço atualizado com sucesso", "sucesso");
      await verDetalhes(agendamentoId);
      await carregarResumoGerencial();
    } else {
      const erro = await response.json();
      mostrarMensagem(erro.detail || "Erro ao alterar status do serviço", "erro");
    }
  } catch (error) {
    mostrarMensagem("Erro ao alterar status do serviço", "erro");
  }
}

async function buscarHistorico() {
  const dataInicio = document.getElementById("data-inicio").value;
  const dataFim = document.getElementById("data-fim").value;

  if (!dataInicio || !dataFim) {
    mostrarMensagem("Preencha as duas datas do histórico", "aviso");
    return;
  }

  try {
    const response = await fetch(`/agendamentos/historico?data_inicio=${dataInicio}&data_fim=${dataFim}`);
    const historico = await response.json();

    const ul = document.getElementById("lista-historico");
    ul.innerHTML = "";

    if (historico.length === 0) {
      ul.innerHTML = "<li>Nenhum agendamento encontrado no período.</li>";
      return;
    }

    historico.forEach(item => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${item.cliente_nome}</strong><br>
        ${item.data} às ${item.horario}<br>
        Total: R$ ${formatarMoeda(item.total)} | 
        Duração: ${item.duracao} min | 
        ${badgeStatus(item.status)}<br>
        Serviços: ${item.servicos.map(s => `${s.nome} (${s.status})`).join(", ")}
      `;
      ul.appendChild(li);
    });

    mostrarMensagem("Histórico carregado com sucesso", "sucesso");
  } catch (error) {
    mostrarMensagem("Erro ao buscar histórico", "erro");
  }
}

carregarServicos();
carregarAgendamentos();
carregarResumoGerencial();
renderizarSelecionados();
calcularTotal();
atualizarResumo();