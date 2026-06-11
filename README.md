# Teoria da Computabilidade — AV2

Seminário técnico com implementação. Estudo, formalização e simulação de dois
modelos de computação, cada um resolvendo um problema distinto, com
rastreamento de execução e testes.

## Identificação

- **Disciplina:** Teoria da Computabilidade — Prof. Daniel Leal Souza (01/2026)
- **Turma:** CC5NA
- **Integrantes:**
  - Felipe de Freitas
  - Benjamin Suzuki
  - Ryan Cavalcanti
  - Lucas Mesquita

## Modelos escolhidos e problemas resolvidos

| Modelo | Problema | Linguagem/função |
|---|---|---|
| Autômato de Pilha (PDA) | Reconhecer delimitadores `( ) [ ] { }` corretamente balanceados e aninhados | Linguagem Livre de Contexto (não regular) |
| Máquina de Turing com Múltiplas Fitas (3 fitas) | Somar dois números binários | Função A + B em binário |

Os dois problemas são distintos (um reconhece linguagem, o outro computa uma
função) e nenhum reutiliza exemplos vistos em aula.

## Estrutura do repositório

```
implementacoes/
  automato_pilha/automato_pilha.py     # PDA: definição formal + simulador (Python)
  automato_pilha/automato_pilha.jff    # PDA no formato JFLAP
  mt_multifita/mt_multifita.py         # MT 3 fitas: definição formal + simulador (Python)
  mt_multifita/mt_multifita.jff        # MT 3 fitas no formato JFLAP
testes/
  rastreamento_pda.txt                 # passos de execução do PDA
  rastreamento_mt_multifita.txt        # passos de execução da MT
  relatorio.md                         # tabelas-resumo + verificação automática
slides/                                # slides da apresentação
uso_ia.md                              # declaração de uso de IA
README.md
```

## Como executar (Python)

Requer apenas **Python 3** (sem dependências externas).

```bash
# Autômato de Pilha
cd implementacoes/automato_pilha
python3 automato_pilha.py             # roda a bateria de exemplos
python3 automato_pilha.py "([]{})"    # testa uma cadeia, com trace passo a passo

# MT Multifita (soma binária)
cd implementacoes/mt_multifita
python3 mt_multifita.py               # roda a bateria de exemplos
python3 mt_multifita.py 101 11        # soma dois binários, com trace passo a passo
```

## Como abrir no JFLAP (arquivos .jff)

Testado no **JFLAP 7.x**.

**PDA — `implementacoes/automato_pilha/automato_pilha.jff`**
Abra com **File ▸ Open**. A pilha já inicia com o símbolo de fundo `Z`. Estados:
`q0` (inicial) → `q1` (laço de empilhar/desempilhar) → `q2` (final); aceitação
por **estado final**. Teste em **Input ▸ Step by State** com, por exemplo,
`()`, `([]{})`, `{[()]}` (aceitas) e `(]`, `([)]`, `(()` (rejeitadas).

**MT Multifita — `implementacoes/mt_multifita/mt_multifita.jff`**
Abra como **Multi-Tape Turing Machine** (3 fitas). Coloque o operando A na
**Fita 1**, B na **Fita 2** (binário, MSB à esquerda, sem zeros à esquerda) e
deixe a **Fita 3** vazia; ao chegar em `q_accept`, o **resultado fica na Fita 1**.
Exemplos: `101` + `11` → `1000`; `1111` + `1` → `10000`; `110` + `101` → `1011`.

> Observação: o JFLAP não admite curingas nas leituras (cada fita exige um
> símbolo concreto por transição). Por isso a tabela da MT foi expandida para
> **44 transições concretas**, extraídas de execuções já validadas do simulador
> em Python. Caso sua versão do JFLAP apresente incompatibilidade ao abrir o
> arquivo multifita, a implementação de referência testada é o `mt_multifita.py`
> (o uso de linguagem de programação também é permitido pela atividade).

## Definições formais (resumo)

**PDA** `M = (Q, Σ, Γ, δ, q0, Z0, F)`
- `Q = {q0, q1, q2}`, `q0` inicial, `F = {q2}`.
- `Σ = { ( ) [ ] { } }`, `Γ = { Z, (, [, { }`, fundo `Z0 = Z`.
- Aceitação por estado final com a pilha de volta ao fundo `Z`.
- A pilha guarda os delimitadores de abertura; cada fechamento só é consumido
  se o topo for o par correspondente. É uma linguagem Livre de Contexto: um
  autômato finito não consegue contar a profundidade do aninhamento.

**MT Multifita** `M = (Q, Σ, Γ, δ, q0, B, F)`, com **k = 3 fitas** e **10 estados**
- Fita 1: operando A (e, ao final, o resultado); Fita 2: operando B; Fita 3: trabalho.
- Soma da direita para a esquerda, com o "vai-um" (carry) codificado no estado
  (`q_add0`/`q_add1`); o resultado é montado na fita 3 e copiado para a fita 1.
- Equivalente em poder à MT de fita única (apenas mais eficiente/organizada).

## Testes e rastreamento

Ver `testes/`. Resumo da verificação automática:

- **PDA:** correto em **todas as 335.923 cadeias** de comprimento 0–7 sobre os
  seis símbolos (conferido contra um verificador de pilha independente).
- **MT soma binária:** **5000/5000** somas aleatórias corretas (operandos de 0 a 32767).

Cada modelo tem no mínimo 3 casos com entradas aceitas/produzidas corretamente
e casos rejeitados ou de fronteira.

## Uso de IA

Ver `uso_ia.md`.

## Referências

- DIVERIO, T. A.; MENEZES, P. B. *Teoria da Computação: Máquinas Universais e Computabilidade*. 3. ed. Porto Alegre: Bookman, 2011.
- MENEZES, P. B. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011.
- SIPSER, M. *Introduction to the Theory of Computation*. 3. ed. Cengage, 2013.
- Documentação do JFLAP.
