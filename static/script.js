
const servicos = [
  {
    id: 1,
    nome: "Corte de Cabelo - Feminino",
    descricao: "Corte personalizado com lavagem, finalização e escova.",
    preco: 70.00,
    duracao: 60
  },
  {
    id: 2,
    nome: "Corte de Cabelo - Masculino",
    descricao: "Corte tradicional ou moderno com acabamento e alinhamento.",
    preco: 40.00,
    duracao: 30
  },
  {
    id: 3,
    nome: "Penteado",
    descricao: "Penteados para eventos, festas e ocasiões especiais.",
    preco: 90.00,
    duracao: 60
  },
  {
    id: 4,
    nome: "Hidratação Intensa",
    descricao: "Tratamento profundo para revitalização e brilho dos fios.",
    preco: 80.00,
    duracao: 45
  }
];

const container = document.getElementById("lista-servicos");

servicos.forEach(servico => {
  const card = document.createElement("div");
  card.classList.add("card-servico");

  card.innerHTML = `
    <h3 class="servico-nome">${servico.nome}</h3>
    
    <p class="servico-descricao">
      ${servico.descricao}
    </p>
    
    <div class="servico-info">
      <span class="servico-preco">R$ ${servico.preco.toFixed(2)}</span>
      <span class="servico-duracao">${servico.duracao} min</span>
    </div>

    <button class="btn-selecionar">
      Selecionar
    </button>
  `;

  container.appendChild(card);
});