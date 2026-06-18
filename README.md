# ChemOptimize v0.1

Sistema Inteligente de Otimização de Envasamento Industrial utilizando Inteligência Artificial e a meta-heurística Simulated Annealing.

## Descrição

O ChemOptimize é um agente baseado em objetivos desenvolvido para resolver um problema de otimização logística conhecido como Bin Packing Problem. O sistema determina a combinação de embalagens que atende exatamente o volume de um lote químico, minimizando custos operacionais e respeitando restrições físicas de capacidade e peso.

O projeto foi desenvolvido como atividade acadêmica da disciplina de Inteligência Artificial.

## Funcionalidades

* Otimização automática da distribuição de recipientes.
* Minimização do custo total de envasamento.
* Controle de capacidade volumétrica.
* Verificação automática dos limites estruturais de peso das embalagens.
* Aplicação da meta-heurística Simulated Annealing.
* Geração de gráfico de convergência da busca.
* Relatório detalhado da solução encontrada.

## Tecnologias Utilizadas

* Python 3
* Matplotlib
* Simulated Annealing
* Inteligência Artificial Baseada em Objetivos

## Estrutura das Embalagens

O catálogo utilizado pelo sistema contém:

| Embalagem | Capacidade |
| --------- | ---------- |
| IBC       | 1000 L     |
| Tanque    | 200 L      |
| Tanque    | 100 L      |
| Tambor    | 50 L       |
| Bombona   | 20 L       |
| Galão     | 5 L        |

## Requisitos

* Python 3.8 ou superior
* Biblioteca Matplotlib

## Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
```

Acesse a pasta do projeto:

```bash
cd ChemOptimize
```

Instale a dependência necessária:

```bash
pip install matplotlib
```

## Execução

Execute o arquivo principal:

```bash
python main.py
```

## Saída Esperada

Ao executar o sistema serão exibidos:

1. Relatório de otimização no terminal contendo:

   * Volume do lote;
   * Massa total calculada;
   * Distribuição ideal de embalagens;
   * Volume alocado;
   * Aproveitamento do espaço;
   * Custo final da solução.

2. Gráfico de convergência do algoritmo Simulated Annealing contendo:

   * Curva do custo atual;
   * Curva da melhor solução encontrada.

## Autores

* Samuel Morsch
* João Vitor da Silva Bast
* George Lucas Silva Brigido

## Versão

ChemOptimize v0.1
