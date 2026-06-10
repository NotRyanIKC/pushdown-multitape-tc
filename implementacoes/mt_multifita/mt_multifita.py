"""
Máquina de Turing com Múltiplas Fitas (3 fitas) — Soma de dois números binários.

Problema: dados dois números naturais A e B em binário (MSB à esquerda),
calcular A + B em binário.
  Fita 1: operando A (entrada)            -> ao final, guarda o RESULTADO.
  Fita 2: operando B (entrada).
  Fita 3: fita de trabalho (resultado parcial, escrito do bit menos
          significativo para o mais significativo).

Por que multifita? Uma MT de fita única também resolve, mas teria de ficar
indo e voltando para alinhar os bits. Com fitas separadas, cada operando tem
sua própria cabeça e a soma percorre os bits da direita para a esquerda de
forma natural, evidenciando a vantagem organizacional do modelo multifita
(que é polinomialmente equivalente à MT padrão).

Este arquivo separa:
  1. A DEFINIÇÃO FORMAL: M = (Q, Σ, Γ, δ, q0, B, F) com 3 fitas.
  2. O SIMULADOR genérico de MT de k fitas, com rastreamento das
     configurações (estado + conteúdo e posição das 3 cabeças).

Uso:
    python3 mt_multifita.py            # bateria de exemplos + verificação
    python3 mt_multifita.py 101 11     # soma 101 + 11, com trace passo a passo
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List

# ---------------------------------------------------------------------------
# 1. DEFINIÇÃO FORMAL   M = (Q, Σ, Γ, δ, q0, B, F),  k = 3 fitas
# ---------------------------------------------------------------------------

BLANK = "_"                                   # símbolo branco (B)
SIGMA = {"0", "1"}                            # alfabeto de entrada
GAMMA = {"0", "1", BLANK}                     # alfabeto da fita
NUM_FITAS = 3

Q = {
    "q_seekA",     # avança a cabeça 1 até o fim de A
    "q_backA",     # recua a cabeça 1 para o último bit (LSB) de A
    "q_seekB",     # avança a cabeça 2 até o fim de B
    "q_backB",     # recua a cabeça 2 para o último bit (LSB) de B
    "q_add0",      # soma os bits com "vai-um" (carry) = 0
    "q_add1",      # soma os bits com "vai-um" (carry) = 1
    "q_prep1",     # posiciona a cabeça 3 sobre o bit mais significativo do resultado
    "q_prep2",     # posiciona a cabeça 1 no início, para receber o resultado
    "q_copy",      # copia o resultado (invertendo) da fita 3 para a fita 1
    "q_accept",    # estado de parada/aceitação
}                  # |Q| = 10 estados (> 8, conforme exigido)
START_STATE = "q_seekA"
FINAL_STATES = {"q_accept"}

# A função de transição δ é dada como uma lista de regras. Cada regra:
#   (estado, (l1, l2, l3))  ->  (novo_estado, (e1, e2, e3), (m1, m2, m3))
# onde:
#   li  = símbolo lido na fita i  (None = curinga: "qualquer símbolo")
#   ei  = símbolo escrito na fita i (None = mantém o que estava)
#   mi  = movimento da cabeça i: 'L', 'R' ou 'S' (estacionária)
#
# A primeira regra cujo padrão casar com a configuração atual é aplicada
# (a máquina é determinística: os padrões de cada estado são disjuntos).

L, R, S = "L", "R", "S"

DELTA: List[Tuple] = [
    # --- Fase 1a: avançar a cabeça 1 até o branco depois de A --------------
    ("q_seekA", ("0", None, None), ("q_seekA", (None, None, None), (R, S, S))),
    ("q_seekA", ("1", None, None), ("q_seekA", (None, None, None), (R, S, S))),
    ("q_seekA", (BLANK, None, None), ("q_backA", (None, None, None), (S, S, S))),
    # --- Fase 1b: recuar a cabeça 1 para o último bit (LSB) de A -----------
    ("q_backA", (None, None, None), ("q_seekB", (None, None, None), (L, S, S))),

    # --- Fase 2a: avançar a cabeça 2 até o branco depois de B --------------
    ("q_seekB", (None, "0", None), ("q_seekB", (None, None, None), (S, R, S))),
    ("q_seekB", (None, "1", None), ("q_seekB", (None, None, None), (S, R, S))),
    ("q_seekB", (None, BLANK, None), ("q_backB", (None, None, None), (S, S, S))),
    # --- Fase 2b: recuar a cabeça 2 para o último bit (LSB) de B -----------
    ("q_backB", (None, None, None), ("q_add0", (None, None, None), (S, L, S))),

    # --- Fase 3: somar da direita para a esquerda -------------------------
    # Em q_add0 (sem vai-um). Escreve o bit da soma na fita 3 e anda L,L,R.
    # As cabeças 1 e 2 recuam (L) enquanto ainda há bits; ao acabar um
    # operando, sua cabeça lê BLANK e fica parada (S), somando 0 implícito.
    ("q_add0", ("0", "0", None), ("q_add0", (None, None, "0"), (L, L, R))),
    ("q_add0", ("0", "1", None), ("q_add0", (None, None, "1"), (L, L, R))),
    ("q_add0", ("1", "0", None), ("q_add0", (None, None, "1"), (L, L, R))),
    ("q_add0", ("1", "1", None), ("q_add1", (None, None, "0"), (L, L, R))),   # gera carry
    ("q_add0", ("0", BLANK, None), ("q_add0", (None, None, "0"), (L, S, R))),
    ("q_add0", ("1", BLANK, None), ("q_add0", (None, None, "1"), (L, S, R))),
    ("q_add0", (BLANK, "0", None), ("q_add0", (None, None, "0"), (S, L, R))),
    ("q_add0", (BLANK, "1", None), ("q_add0", (None, None, "1"), (S, L, R))),
    # ambos acabaram, sem vai-um: resultado pronto na fita 3 -> preparar cópia
    ("q_add0", (BLANK, BLANK, None), ("q_prep1", (None, None, None), (S, S, S))),

    # Em q_add1 (com vai-um = 1).
    ("q_add1", ("0", "0", None), ("q_add0", (None, None, "1"), (L, L, R))),
    ("q_add1", ("0", "1", None), ("q_add1", (None, None, "0"), (L, L, R))),
    ("q_add1", ("1", "0", None), ("q_add1", (None, None, "0"), (L, L, R))),
    ("q_add1", ("1", "1", None), ("q_add1", (None, None, "1"), (L, L, R))),
    ("q_add1", ("0", BLANK, None), ("q_add0", (None, None, "1"), (L, S, R))),
    ("q_add1", ("1", BLANK, None), ("q_add1", (None, None, "0"), (L, S, R))),
    ("q_add1", (BLANK, "0", None), ("q_add0", (None, None, "1"), (S, L, R))),
    ("q_add1", (BLANK, "1", None), ("q_add1", (None, None, "0"), (S, L, R))),
    # ambos acabaram com vai-um pendente: escreve o 1 final na fita 3
    ("q_add1", (BLANK, BLANK, None), ("q_prep1", (None, None, "1"), (S, S, R))),

    # --- Fase 4: inverter o resultado da fita 3 para a fita 1 -------------
    # A fita 3 tem o resultado com o LSB à esquerda. Recuamos a cabeça 3 ao
    # bit mais significativo (último escrito) e a cabeça 1 ao início.
    ("q_prep1", (None, None, None), ("q_prep2", (None, None, None), (S, S, L))),
    ("q_prep2", (None, None, None), ("q_copy",  (None, None, None), (R, S, S))),
    # Copiar lendo a fita 3 do MSB para o LSB (cabeça 3 anda L) e escrevendo
    # na fita 1 do início para o fim (cabeça 1 anda R): resultado MSB-first.
    ("q_copy", (None, None, "0"), ("q_copy", ("0", None, None), (R, S, L))),
    ("q_copy", (None, None, "1"), ("q_copy", ("1", None, None), (R, S, L))),
    ("q_copy", (None, None, BLANK), ("q_accept", (None, None, None), (S, S, S))),
]


# ---------------------------------------------------------------------------
# 2. SIMULADOR DE MT DE k FITAS
# ---------------------------------------------------------------------------

class Tape:
    """Fita infinita nos dois sentidos, indexada por um dicionário."""
    def __init__(self, conteudo: str = ""):
        self.cells = {i: ch for i, ch in enumerate(conteudo)}
        self.head = 0

    def read(self) -> str:
        return self.cells.get(self.head, BLANK)

    def write(self, sym: str):
        if sym is not None:
            self.cells[self.head] = sym

    def move(self, m: str):
        if m == "L":
            self.head -= 1
        elif m == "R":
            self.head += 1

    def snapshot(self) -> str:
        if not self.cells:
            idxs = [0]
        else:
            idxs = range(min(self.cells), max(self.cells) + 1)
        out = []
        for i in idxs:
            sym = self.cells.get(i, BLANK)
            out.append(f"[{sym}]" if i == self.head else sym)
        s = "".join(out)
        if self.head not in self.cells and not (
            min(self.cells, default=0) <= self.head <= max(self.cells, default=0)
        ):
            s += f" (cabeça@{self.head})"
        return s if s else f"[{BLANK}]"


def casa(padrao, leituras) -> bool:
    return all(p is None or p == l for p, l in zip(padrao, leituras))


def executar(A: str, B: str, trace: bool = False, limite: int = 100000):
    """Executa a MT sobre os operandos A e B. Retorna (resultado_str, passos)."""
    fitas = [Tape(A), Tape(B), Tape("")]
    estado = START_STATE
    passos = []

    def registrar(n, acao):
        linha = (f"{n:>3} | {estado:<9} | "
                 f"F1:{fitas[0].snapshot():<14} "
                 f"F2:{fitas[1].snapshot():<10} "
                 f"F3:{fitas[2].snapshot():<14} | {acao}")
        passos.append(linha)
        if trace:
            print(linha)

    registrar(0, "configuração inicial")

    n = 0
    while estado not in FINAL_STATES and n < limite:
        leituras = tuple(f.read() for f in fitas)
        regra = next((r for r in DELTA if r[0] == estado and casa(r[1], leituras)), None)
        if regra is None:
            registrar(n, f"⊘ sem transição para leituras {leituras}")
            raise RuntimeError(f"MT travada em {estado} lendo {leituras}")
        _, _, (novo_estado, escritas, movimentos) = regra
        for f, e, m in zip(fitas, escritas, movimentos):
            f.write(e)
            f.move(m)
        estado = novo_estado
        n += 1
        registrar(n, f"-> {estado}")

    # Lê o resultado da fita 1 (MSB-first), ignorando brancos das pontas.
    cells = fitas[0].cells
    if cells:
        lo, hi = min(cells), max(cells)
        bits = "".join(cells.get(i, BLANK) for i in range(lo, hi + 1)).strip(BLANK)
    else:
        bits = ""
    resultado = bits if bits else "0"
    return resultado, passos


# ---------------------------------------------------------------------------
# 3. Exemplos, verificação e linha de comando
# ---------------------------------------------------------------------------

def soma_binaria(A: str, B: str) -> str:
    """Referência (não-MT) só para conferir a corretude do simulador."""
    return format(int(A, 2) + int(B, 2), "b")


EXEMPLOS = [
    ("0", "0"),
    ("1", "1"),
    ("101", "11"),       # 5 + 3 = 8  -> 1000
    ("1111", "1"),       # 15 + 1 = 16 -> 10000
    ("1010", "1010"),    # 10 + 10 = 20 -> 10100
    ("110", "101"),      # 6 + 5 = 11 -> 1011
]


def main(argv):
    if len(argv) > 2:
        A, B = argv[1], argv[2]
        print(f"Soma binária:  {A} + {B}\n")
        resultado, _ = executar(A, B, trace=True)
        esperado = soma_binaria(A, B)
        print(f"\nRESULTADO (fita 1): {resultado}")
        print(f"Esperado:           {esperado}")
        print("OK" if resultado == esperado else "DIVERGENCIA")
        return

    print("=" * 60)
    print("MT Multifita (3 fitas) — Soma binária")
    print("=" * 60)
    for A, B in EXEMPLOS:
        resultado, _ = executar(A, B)
        esperado = soma_binaria(A, B)
        ok = resultado == esperado
        print(f"  {'OK ' if ok else 'ERRO'}  {A:>6} + {B:<6} = {resultado:<8} "
              f"(esperado {esperado}; {int(A,2)}+{int(B,2)}={int(A,2)+int(B,2)})")


if __name__ == "__main__":
    import sys
    main(sys.argv)
