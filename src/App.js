const produtos = [
  {
    id: 1,
    nome: 'Glifosato',
    lote: 'GL-2026-01',
    validade: '2026-09-10',
    principio: 'Glifosato',
    quantidade: '120 L',
    status: 'Atenção',
  },
  {
    id: 2,
    nome: 'Inseticida X',
    lote: 'INS-992',
    validade: '2025-12-01',
    principio: 'Lambda-cialotrina',
    quantidade: '40 L',
    status: 'Crítico',
  },
  {
    id: 3,
    nome: 'Fungicida Y',
    lote: 'FUN-778',
    validade: '2027-03-15',
    principio: 'Azoxistrobina',
    quantidade: '200 L',
    status: 'OK',
  },
];

const statusColor = {
  OK: 'bg-green-100 text-green-700',
  Atenção: 'bg-yellow-100 text-yellow-700',
  Crítico: 'bg-red-100 text-red-700',
};

const escapeHtml = (value) =>
  String(value).replace(/[&<>'"]/g, (character) => {
    const entities = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;',
    };

    return entities[character];
  });

const renderProduto = (produto) => `
  <tr class="border-b hover:bg-gray-50">
    <td class="p-4 font-medium">${escapeHtml(produto.nome)}</td>
    <td class="p-4">${escapeHtml(produto.lote)}</td>
    <td class="p-4">${escapeHtml(produto.validade)}</td>
    <td class="p-4">${escapeHtml(produto.principio)}</td>
    <td class="p-4">${escapeHtml(produto.quantidade)}</td>
    <td class="p-4">
      <span class="px-3 py-1 rounded-full text-sm font-semibold ${statusColor[produto.status]}">
        ${escapeHtml(produto.status)}
      </span>
    </td>
  </tr>
`;

export default function AgroEstoqueApp() {
  return `
    <div class="min-h-screen bg-gray-100 p-6">
      <div class="max-w-7xl mx-auto space-y-6">
        <div class="bg-white rounded-3xl shadow-lg p-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <div>
            <h1 class="text-4xl font-bold text-green-700">AgroEstoque</h1>
            <p class="text-gray-600 mt-2">
              Controle inteligente de defensivos agrícolas por lote, validade e princípio ativo.
            </p>
          </div>

          <button class="bg-green-700 hover:bg-green-800 text-white px-5 py-3 rounded-2xl font-semibold shadow">
            + Novo Produto
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white rounded-2xl p-5 shadow">
            <p class="text-gray-500 text-sm">Produtos cadastrados</p>
            <h2 class="text-3xl font-bold mt-2">128</h2>
          </div>

          <div class="bg-white rounded-2xl p-5 shadow">
            <p class="text-gray-500 text-sm">Próximos do vencimento</p>
            <h2 class="text-3xl font-bold mt-2 text-yellow-600">14</h2>
          </div>

          <div class="bg-white rounded-2xl p-5 shadow">
            <p class="text-gray-500 text-sm">Produtos vencidos</p>
            <h2 class="text-3xl font-bold mt-2 text-red-600">3</h2>
          </div>

          <div class="bg-white rounded-2xl p-5 shadow">
            <p class="text-gray-500 text-sm">Valor em estoque</p>
            <h2 class="text-3xl font-bold mt-2">R$ 482 mil</h2>
          </div>
        </div>

        <div class="bg-white rounded-3xl shadow-lg p-6">
          <div class="flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
            <h2 class="text-2xl font-bold">Estoque de Defensivos</h2>

            <input
              type="text"
              placeholder="Pesquisar produto ou lote"
              class="border border-gray-300 rounded-2xl px-4 py-3 w-full md:w-80"
            />
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b text-gray-600">
                  <th class="p-4">Produto</th>
                  <th class="p-4">Lote</th>
                  <th class="p-4">Validade</th>
                  <th class="p-4">Princípio Ativo</th>
                  <th class="p-4">Quantidade</th>
                  <th class="p-4">Status</th>
                </tr>
              </thead>

              <tbody>
                ${produtos.map(renderProduto).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white rounded-3xl shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4">Alertas Inteligentes</h2>

            <div class="space-y-4">
              <div class="bg-yellow-50 border border-yellow-200 rounded-2xl p-4">
                <p class="font-semibold text-yellow-700">
                  14 produtos próximos do vencimento.
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  Priorizar utilização nos próximos 30 dias.
                </p>
              </div>

              <div class="bg-red-50 border border-red-200 rounded-2xl p-4">
                <p class="font-semibold text-red-700">3 produtos vencidos encontrados.</p>
                <p class="text-sm text-gray-600 mt-1">Verificar descarte ou devolução.</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-3xl shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4">Integração WhatsApp</h2>

            <div class="bg-green-50 border border-green-200 rounded-2xl p-5 space-y-3">
              <p class="font-semibold text-green-700">Exemplos de comandos:</p>

              <ul class="space-y-2 text-gray-700 text-sm">
                <li>• &quot;Quanto tenho de glifosato?&quot;</li>
                <li>• &quot;Produtos vencendo este mês&quot;</li>
                <li>• &quot;Cadastrar lote INS-992&quot;</li>
                <li>• &quot;Mostrar produtos por princípio ativo&quot;</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="bg-green-700 rounded-3xl p-6 text-white shadow-lg">
          <h2 class="text-2xl font-bold">Visão Estratégica</h2>
          <p class="mt-3 text-green-100 leading-relaxed">
            O AgroEstoque não é apenas um sistema de estoque. Ele atua como uma central de prevenção de perdas agrícolas,
            reduzindo desperdício de defensivos, evitando vencimentos e melhorando o uso inteligente dos insumos dentro da fazenda.
          </p>
        </div>
      </div>
    </div>
  `;
}
