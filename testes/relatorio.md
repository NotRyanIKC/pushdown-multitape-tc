# Relatório de Rastreamento de Execução

Tabelas-resumo dos testes. Os passos completos de execução estão em
`rastreamento_pda.txt` e `rastreamento_mt_multifita.txt`.

## 1. PDA — Delimitadores balanceados `( ) [ ] { }`

| # | Entrada | Esperado | Obtido | Motivo |
|---|---------|----------|--------|--------|
| 1 | `()` | ACEITA | ACEITA (OK) | entrada consumida em estado final com pilha = Z |
| 2 | `([]{})` | ACEITA | ACEITA (OK) | entrada consumida em estado final com pilha = Z |
| 3 | `{[()]}` | ACEITA | ACEITA (OK) | entrada consumida em estado final com pilha = Z |
| 4 | "" | ACEITA | ACEITA (OK) | entrada consumida em estado final com pilha = Z |
| 5 | `(]` | REJEITA | REJEITA (OK) | fechamento ']' não casa com o topo '(' |
| 6 | `([)]` | REJEITA | REJEITA (OK) | fechamento ')' não casa com o topo '[' |
| 7 | `(()` | REJEITA | REJEITA (OK) | fim da entrada com delimitadores ainda abertos na pilha |
| 8 | `)(` | REJEITA | REJEITA (OK) | fechamento ')' não casa com o topo 'Z' |

## 2. MT Multifita — Soma binária (3 fitas)

| # | A | B | Esperado | Obtido | Decimal | Status |
|---|---|---|----------|--------|---------|--------|
| 1 | `1` | `1` | `10` | `10` | 1+1=2 | OK |
| 2 | `101` | `11` | `1000` | `1000` | 5+3=8 | OK |
| 3 | `110` | `101` | `1011` | `1011` | 6+5=11 | OK |
| 4 | `0` | `0` | `0` | `0` | 0+0=0 | OK |
| 5 | `1111` | `1` | `10000` | `10000` | 15+1=16 | OK |
| 6 | `1010` | `1010` | `10100` | `10100` | 10+10=20 | OK |

## 3. Teste de estresse (verificação automática)

- MT soma binária: **5000/5000** somas aleatórias corretas (0–32767).
- PDA delimitadores: **335923/335923** cadeias corretas (todas as cadeias de comprimento 0–7 sobre os 6 símbolos).
