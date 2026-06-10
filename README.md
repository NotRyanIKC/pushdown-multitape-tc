# Teoria da Computabilidade — AV2

Seminário técnico com implementação. Estudo, formalização e simulação de dois modelos de computação, com problemas distintos para cada um.

## Identificação

- **Disciplina:** Teoria da Computabilidade — Prof. Daniel Leal Souza
- **Turma:** CC5NA
- **Integrantes:**
  - Felipe de Freitas
  - Benjamin Suzuki
  - Ryan Cavalcanti
  - Lucas Mesquita

## Modelos escolhidos

| Modelo | Problema resolvido |
|---|---|
| Autômato de Pilha (PDA) | _(definir — ex.: reconhecer aⁿbⁿ ou parênteses balanceados)_ |
| Máquina de Turing com Múltiplas Fitas | _(definir — ex.: soma binária ou reconhecer ww)_ |

> Cada implementação resolve um **problema diferente** e tem mais de 8 estados / pelo menos 10 transições relevantes.

## Estrutura do repositório

```
implementacoes/   # arquivos .jff e/ou código-fonte
slides/           # slides ou link da apresentação
testes/           # entradas, saídas esperadas/obtidas e rastreamento de execução
uso_ia.md         # declaração de uso de IA
README.md
```

## Como executar

**JFLAP:** abrir os arquivos `.jff` em `implementacoes/` no JFLAP (versão 7.x) e usar *Input → Step/Run* com as entradas de `testes/`.

_(Atualizar com instruções de código, dependências e exemplos de entrada/saída caso seja usada linguagem de programação.)_

## Rastreamento de execução

Para cada modelo, no mínimo 3 casos de teste: aceitos/produzidos corretamente e rejeitados/de fronteira. Ver pasta `testes/`.

## Uso de IA

Ver `uso_ia.md` (obrigatório, mesmo que não tenha havido uso).

## Referências

- DIVERIO, T. A.; MENEZES, P. B. *Teoria da Computação: Máquinas Universais e Computabilidade*. 3. ed. Porto Alegre: Bookman, 2011.
- MENEZES, P. B. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011.
- Documentação do JFLAP.
