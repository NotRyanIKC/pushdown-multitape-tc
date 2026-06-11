# Relatório de Rastreamento de Execução

Tabelas-resumo dos testes. Os passos completos estão em `rastreamento_pda.txt`
e `rastreamento_mt_multifita.txt`.

## 1. PDA — Validador de tags aninhadas `<p> <h1> <h2>`

| # | Entrada | Esperado | Obtido | Observação |
|---|---|---|---|---|
| 1 | `<p></p>` | ACEITA | ACEITA | entrada consumida em estado final com pilha = Z |
| 2 | `<p><h1></h1></p>` | ACEITA | ACEITA | entrada consumida em estado final com pilha = Z |
| 3 | `<h1><p></p><p></p></h1>` | ACEITA | ACEITA | entrada consumida em estado final com pilha = Z |
| 4 | "" | ACEITA | ACEITA | entrada consumida em estado final com pilha = Z |
| 5 | `<p></h1>` | REJEITA | REJEITA | tag de fechamento não casa com a tag aberta no topo ('P') |
| 6 | `<p><h1></p></h1>` | REJEITA | REJEITA | tag de fechamento não casa com a tag aberta no topo ('A') |
| 7 | `<p>` | REJEITA | REJEITA | fim da entrada com tags ainda abertas |
| 8 | `</p>` | REJEITA | REJEITA | tag de fechamento não casa com a tag aberta no topo ('Z') |

## 2. MT Multifita — Busca de padrão (2 fitas)

| # | Texto T | Padrão P | Esperado | Obtido | Python `P in T` |
|---|---|---|---|---|---|
| 1 | `aab` | `ab` | ACEITA | ACEITA | True |
| 2 | `baaab` | `aaa` | ACEITA | ACEITA | True |
| 3 | `aaa` | `ab` | REJEITA | REJEITA | False |
| 4 | `ab` | `abb` | REJEITA | REJEITA | False |
| 5 | `bbbb` | `a` | REJEITA | REJEITA | False |
| 6 | `ab` | "" | ACEITA | ACEITA | True |

## 3. Verificação automática (exaustiva)

- **PDA:** correto em **55987/55987** cadeias (todas as combinações de 0 a 6 tags do vocabulário).
- **MT busca de padrão:** correto em **7905/7905** casos (texto de 0–7 e padrão de 0–4 símbolos sobre {a,b}).
