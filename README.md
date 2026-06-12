# Teoria da Computabilidade — AV2

Seminário técnico com implementação. Estudo, formalização e simulação de dois
modelos de computação, cada um resolvendo um problema distinto, com
rastreamento de execução e testes.

## Identificação

- **Disciplina:** Teoria da Computabilidade — Prof. Daniel Leal Souza
- **Turma:** CC5NA
- **Integrantes:**
  - Felipe de Freitas
  - Benjamin Suzuki
  - Ryan Cavalcanti
  - Lucas Mesquita

## Modelos escolhidos e problemas resolvidos

| Modelo | Problema | Linguagem/função |
|---|---|---|
| Autômato de Pilha (PDA) | Validar **tags aninhadas** `<p>`, `<h1>`, `<h2>` (estilo HTML), casando abertura/fechamento | Linguagem Livre de Contexto (não regular) |
| Máquina de Turing com Múltiplas Fitas (2 fitas) | **Busca de padrão** (string matching): decidir se o padrão P é subcadeia do texto T | Problema de decisão sobre {a, b} |

Os dois problemas são distintos (um valida estrutura aninhada, o outro busca
uma subcadeia) e nenhum reutiliza exemplos vistos em aula.

## Estrutura do repositório

```
implementacoes/
  automato_pilha/automato_pilha.py     # PDA: definição formal + simulador (Python)
  automato_pilha/automato_pilha.jff    # PDA no formato JFLAP
  mt_multifita/mt_multifita.py         # MT (2 fitas): definição formal + simulador (Python)
  mt_multifita/mt_multifita.jff        # MT no formato JFLAP
testes/
  rastreamento_pda.txt                 # passos de execução do PDA
  rastreamento_mt_multifita.txt        # passos de execução da MT
  relatorio.md                         # tabelas-resumo + verificação automática
slides/MT e PDA.pptx                   # slides da apresentação (15 slides)
uso_ia.md                              # declaração de uso de IA
README.md
```

## Como executar (Python)

Requer apenas **Python 3** (sem dependências externas).

```bash
# Autômato de Pilha — validador de tags
cd implementacoes/automato_pilha
python3 automato_pilha.py                      # roda a bateria de exemplos
python3 automato_pilha.py "<p><h1></h1></p>"   # testa uma cadeia, com trace passo a passo

# MT Multifita — busca de padrão
cd implementacoes/mt_multifita
python3 mt_multifita.py            # roda a bateria de exemplos
python3 mt_multifita.py aab ab     # busca o padrão "ab" no texto "aab", com trace
```

## Como abrir no JFLAP (arquivos .jff)

Testado no **JFLAP 7.x**.

**PDA — `implementacoes/automato_pilha/automato_pilha.jff`** (9 estados)
Abra com **File ▸ Open**. A pilha já inicia com o símbolo de fundo `Z`. O nome
de cada tag é lido caractere a caractere (por isso são necessários >8 estados),
e a pilha guarda quais tags estão abertas para casar os fechamentos. Aceitação
por **estado final**. Teste em **Input ▸ Step by State** com, por exemplo,
`<p></p>`, `<p><h1></h1></p>` (aceitas) e `<p></h1>`, `<p><h1></p></h1>` (rejeitadas).

**MT Multifita — `implementacoes/mt_multifita/mt_multifita.jff`** (2 fitas, 9 estados)
Abra como **Multi-Tape Turing Machine**. Coloque o texto na **Fita 1** e o
padrão na **Fita 2** (alfabeto {a, b}); a máquina para em `q_accept` se o padrão
ocorre no texto e em `q_reject` caso contrário. Exemplos: T=`aab`, P=`ab`
(aceita); T=`aaa`, P=`ab` (rejeita).

> Observação: o JFLAP não admite curingas nas leituras (cada fita exige um
> símbolo concreto por transição). Por isso a tabela da MT foi expandida para
> **31 transições concretas**, extraídas de execuções já validadas do simulador
> em Python. Caso sua versão do JFLAP apresente incompatibilidade ao abrir o
> arquivo multifita, a implementação de referência testada é o `mt_multifita.py`
> (o uso de linguagem de programação também é permitido pela atividade).

> **Limitação do JFLAP (fita semi-infinita):** a MT teórica de múltiplas fitas
> usa fita **infinita nos dois sentidos**. Ao falhar um casamento, nosso
> algoritmo **rebobina** as cabeças (`q_reset → q_shift1 → q_shift2`) para
> reposicionar no início do padrão, o que passa **para a esquerda da posição
> inicial**. O JFLAP modela a fita como **semi-infinita (limitada à esquerda)**,
> então bloqueia esse movimento e rejeita justamente os casos que exigem
> retrocesso (ex.: T=`aab`, P=`ab`). Os casos diretos, sem retrocesso (ex.:
> T=`ab`, P=`ab`; T=`ab`, P=`a`), funcionam normalmente no JFLAP. **Não é erro
> do modelo:** pelo teorema de equivalência, a MT de fita bi-infinita tem o
> mesmo poder da de fita semi-infinita — é só uma diferença de representação. O
> simulador em `mt_multifita.py` implementa o modelo padrão (bi-infinito) e está
> correto, verificado em 7.905 casos. Para a demonstração, os casos com
> retrocesso são executados pelo Python.

## Definições formais (resumo)

**PDA** `M = (Q, Σ, Γ, δ, q0, Z0, F)` — **9 estados**
- `Q = {q_start, q0, q_lt, q_oh, q_ogt, q_c0, q_ch, q_cgt, q_accept}`, `F = {q_accept}`.
- `Σ = { <, >, /, p, h, 1, 2 }`, `Γ = { Z, P, A, B }` (P=`<p>`, A=`<h1>`, B=`<h2>`), fundo `Z0 = Z`.
- Ao abrir uma tag, empilha o símbolo correspondente; ao fechar, só desempilha
  se o topo for a tag certa — é assim que o aninhamento é verificado. Aceitação
  por estado final com a pilha de volta ao fundo `Z`. É uma linguagem Livre de
  Contexto: um autômato finito não controlaria a profundidade do aninhamento.

**MT Multifita** `M = (Q, Σ, Γ, δ, q0, B, F)` — **k = 2 fitas, 9 estados**
- Fita 1: texto T; Fita 2: padrão P.
- A máquina lê cada símbolo do padrão para o controle finito (`q_have_a`/`q_have_b`)
  e compara com o texto. Ao falhar, rebobina as duas cabeças em sincronia
  (`q_reset` → `q_shift1` → `q_shift2`) e avança a âncora do texto em uma posição.
- Equivalente em poder à MT de fita única; as duas fitas tornam a comparação natural.

## Testes e rastreamento

Ver `testes/`. Resumo da verificação automática:

- **PDA:** correto em **55.987/55.987** cadeias (todas as combinações de 0 a 6
  tags do vocabulário `<p> </p> <h1> </h1> <h2> </h2>`).
- **MT busca de padrão:** correto em **7.905/7.905** casos (texto de 0–7 e padrão
  de 0–4 símbolos sobre {a, b}), conferido contra o operador `in` do Python.

Cada modelo tem no mínimo 3 casos com entradas aceitas e casos rejeitados ou de fronteira.

## Uso de IA

Ver `uso_ia.md`.

## Referências

- DIVERIO, T. A.; MENEZES, P. B. *Teoria da Computação: Máquinas Universais e Computabilidade*. 3. ed. Porto Alegre: Bookman, 2011.
- MENEZES, P. B. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011.
- SIPSER, M. *Introduction to the Theory of Computation*. 3. ed. Cengage, 2013.
- Documentação do JFLAP.
