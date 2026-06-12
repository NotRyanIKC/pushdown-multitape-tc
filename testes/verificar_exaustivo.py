#!/usr/bin/env python3
"""Verificação exaustiva dos dois modelos.

- PDA: 55.987 cadeias (0 a 6 tags do vocabulário)
- MT:  7.905 casos (texto 0-7, padrão 0-4 sobre {a,b})
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

from implementacoes.automato_pilha.automato_pilha import aceita
from implementacoes.mt_multifita.mt_multifita import executar


# ── PDA ──────────────────────────────────────────────────────────────────────

TAGS = ["<p>", "</p>", "<h1>", "</h1>", "<h2>", "</h2>"]


def gerar_cadeias_pda(max_tags=6):
    """Gera todas as sequências de 0 a max_tags escolhidas de TAGS."""
    cadeias = [""]
    for n in range(1, max_tags + 1):
        indices = [0] * n
        while True:
            cadeias.append("".join(TAGS[i] for i in indices))
            i = n - 1
            while i >= 0 and indices[i] == len(TAGS) - 1:
                i -= 1
            if i < 0:
                break
            indices[i] += 1
            for j in range(i + 1, n):
                indices[j] = 0
    return cadeias


def verificar_pda():
    print("PDA — Verificação exaustiva (0 a 6 tags)...")
    cadeias = gerar_cadeias_pda(6)
    total = len(cadeias)
    erros = []
    for idx, cadeia in enumerate(cadeias):
        ok, _, _ = aceita(cadeia)
        esperado = _esperado_pda(cadeia)
        if ok != esperado:
            erros.append((cadeia, esperado, ok))
        if (idx + 1) % 10000 == 0:
            print(f"  progresso: {idx + 1}/{total}")
    print(f"  resultado: {total - len(erros)}/{total} corretos",
          " ✅" if not erros else f" ❌ ({len(erros)} erro(s))")
    for c, esp, obt in erros[:5]:
        print(f"    FALHA: {c!r}  esperado={'ACEITA' if esp else 'REJEITA'}  obtido={'ACEITA' if obt else 'REJEITA'}")
    return erros


def _esperado_pda(cadeia):
    """Simulador de pilha independente — oracle para verificação."""
    MAP = {"<p>": ("p", 3), "</p>": ("p", 4),
           "<h1>": ("h1", 4), "</h1>": ("h1", 5),
           "<h2>": ("h2", 4), "</h2>": ("h2", 5)}
    pilha = []
    i = 0
    while i < len(cadeia):
        match = None
        for token, (nome, tam) in MAP.items():
            if cadeia[i:i+tam] == token:
                match = (token, nome, tam)
                break
        if match is None:
            return False
        token, nome, tam = match
        if token.startswith("</"):
            if not pilha or pilha[-1] != nome:
                return False
            pilha.pop()
        else:
            pilha.append(nome)
        i += tam
    return len(pilha) == 0


# ── MT Multifita ─────────────────────────────────────────────────────────────

def gerar_casos_mt(max_texto=7, max_padrao=4):
    """Gera todos os pares (texto, padrão) sobre {a,b} nos intervalos."""
    def strings(comp):
        if comp == 0:
            yield ""
            return
        for s in strings(comp - 1):
            yield s + "a"
            yield s + "b"
    casos = []
    for t_len in range(max_texto + 1):
        for p_len in range(max_padrao + 1):
            for T in strings(t_len):
                for P in strings(p_len):
                    casos.append((T, P))
    return casos


def verificar_mt():
    print("\nMT Multifita — Verificação exaustiva (texto 0-7, padrão 0-4)...")
    casos = gerar_casos_mt(7, 4)
    total = len(casos)
    erros = []
    for idx, (T, P) in enumerate(casos):
        aceito, _ = executar(T, P)
        esperado = (P in T)
        if aceito != esperado:
            erros.append((T, P, esperado, aceito))
        if (idx + 1) % 2000 == 0:
            print(f"  progresso: {idx + 1}/{total}")
    print(f"  resultado: {total - len(erros)}/{total} corretos",
          " ✅" if not erros else f" ❌ ({len(erros)} erro(s))")
    for T, P, esp, obt in erros[:5]:
        print(f"    FALHA: T={T!r} P={P!r}  esperado={'ACEITA' if esp else 'REJEITA'}  obtido={'ACEITA' if obt else 'REJEITA'}")
    return erros


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    erros_pda = verificar_pda()
    erros_mt = verificar_mt()
    print("\n" + "=" * 50)
    total_erros = len(erros_pda) + len(erros_mt)
    if total_erros == 0:
        print("TODOS OS TESTES PASSARAM ✅")
        return 0
    else:
        print(f"{total_erros} erro(s) encontrado(s) ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
