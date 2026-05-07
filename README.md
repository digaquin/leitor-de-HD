# AgroEstoque

AgroEstoque é um aplicativo desktop em Python/Tkinter para organizar o estoque de defensivos agrícolas em grandes fazendas, barracões e áreas de teste de produtos.

O foco é evitar que produtos comprados em grande volume fiquem esquecidos no estoque até perderem a validade. Para isso, o app cadastra cada insumo por produto, lote, validade, princípio ativo, quantidade, local de armazenamento e origem/uso.

## Funcionalidades

- Cadastro de defensivos por lote, validade e princípio ativo.
- Ordenação automática por validade, depois princípio ativo e lote.
- Destaque visual para produtos vencidos e produtos que vencem em até 90 dias.
- Busca por produto, lote, princípio ativo, local ou origem de uso.
- Remoção de itens selecionados.
- Persistência local em `agroestoque_dados.json`.
- Interface simples para uso no barracão, sem dependências externas além da biblioteca padrão do Python.

## Como executar

Requisitos:

- Python 3.10 ou superior.
- Tkinter instalado no ambiente Python.

Execute:

```bash
python3 agroestoque.py
```

## Campos de cadastro

| Campo | Objetivo |
| --- | --- |
| Produto comercial | Nome do defensivo ou insumo. |
| Lote | Identificação do lote para rastreabilidade. |
| Validade | Data no formato `AAAA-MM-DD`. |
| Princípio ativo | Ajuda a localizar produtos equivalentes ou priorizar uso técnico. |
| Quantidade e unidade | Volume disponível no estoque. |
| Local no barracão | Prateleira, corredor, baia ou área de armazenamento. |
| Origem/uso | Safra, teste de campo, sobra, devolução ou outro. |
| Observações | Campo livre para informações adicionais. |

## Regra de organização

A tabela principal prioriza a seguinte ordem:

1. validade mais próxima;
2. princípio ativo em ordem alfabética;
3. lote em ordem alfabética.

Essa ordem ajuda a equipe a usar primeiro os produtos com maior risco de vencimento e a encontrar rapidamente alternativas pelo mesmo princípio ativo.
