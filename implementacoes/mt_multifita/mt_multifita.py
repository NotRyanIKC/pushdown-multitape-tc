from typing import Optional, Tuple, List

# ---------------------------------------------------------------------------
# 1. DEFINIÇÃO FORMAL   M = (Q, Σ, Γ, δ, q0, B, F),  k = 2 fitas
# ---------------------------------------------------------------------------

BLANK = "_"                                   # símbolo branco (B)
SIGMA = {"a", "b"}                            # alfabeto de entrada
GAMMA = {"a", "b", BLANK}                     # alfabeto da fita
NUM_FITAS = 2

Q = {
    "q_read",     # lê o símbolo atual do PADRÃO (fita 2) e o guarda no controle
    "q_have_a",   # lembra que o padrão exige 'a' aqui; compara com o texto
    "q_have_b",   # lembra que o padrão exige 'b' aqui; compara com o texto
    "q_adv",      # casou: avança as duas cabeças
    "q_reset",    # falhou: rebobina as duas cabeças até o início do padrão
    "q_shift1",   # recoloca a cabeça do padrão no 1º símbolo / texto na âncora
    "q_shift2",   # avança a âncora do texto em uma posição
    "q_accept",   # padrão encontrado (parada com aceitação)
    "q_reject",   # texto esgotado sem casar (parada com rejeição)
}                  # |Q| = 9 estados (> 8, conforme exigido)
START_STATE = "q_read"
FINAL_STATES = {"q_accept"}              # aceitação
REJECT_STATES = {"q_reject"}             # parada sem aceitação
HALT_STATES = FINAL_STATES | REJECT_STATES

# δ como lista de regras (mesma notação da outra máquina):
#   (estado, (l1, l2))  ->  (novo_estado, (e1, e2), (m1, m2))
#   li None = curinga | ei None = mantém | mi em {L, R, S}
# (determinística: os padrões de cada estado são disjuntos.)

L, R, S = "L", "R", "S"

DELTA: List[Tuple] = [
    ("q_read", (None, "a"), ("q_have_a", (None, None), (S, S))),
    ("q_read", (None, "b"), ("q_have_b", (None, None), (S, S))),
    ("q_read", (None, BLANK), ("q_accept", (None, None), (S, S))),

    ("q_have_a", ("a", None), ("q_adv",    (None, None), (S, S))),   # casou
    ("q_have_a", ("b", None), ("q_reset",  (None, None), (S, S))),   # falhou
    ("q_have_a", (BLANK, None), ("q_reject", (None, None), (S, S))), # texto acabou

    ("q_have_b", ("b", None), ("q_adv",    (None, None), (S, S))),
    ("q_have_b", ("a", None), ("q_reset",  (None, None), (S, S))),
    ("q_have_b", (BLANK, None), ("q_reject", (None, None), (S, S))),

    ("q_adv", (None, None), ("q_read", (None, None), (R, R))),

    ("q_reset", (None, "a"), ("q_reset",  (None, None), (L, L))),
    ("q_reset", (None, "b"), ("q_reset",  (None, None), (L, L))),
    ("q_reset", (None, BLANK), ("q_shift1", (None, None), (S, S))),

    ("q_shift1", (None, None), ("q_shift2", (None, None), (R, R))),
    ("q_shift2", (None, None), ("q_read", (None, None), (R, S))),
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

    def write(self, sym):
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


def executar(T: str, P: str, trace: bool = False, limite: int = 100000):
    """Executa a MT. Retorna (aceito: bool, passos: list[str])."""
    fitas = [Tape(T), Tape(P)]
    estado = START_STATE
    passos = []

    def registrar(n, acao):
        linha = (f"{n:>3} | {estado:<9} | "
                 f"Texto:{fitas[0].snapshot():<16} "
                 f"Padrão:{fitas[1].snapshot():<10} | {acao}")
        passos.append(linha)
        if trace:
            print(linha)

    registrar(0, "configuração inicial")

    n = 0
    while estado not in HALT_STATES and n < limite:
        leituras = tuple(f.read() for f in fitas)
        regra = next((r for r in DELTA if r[0] == estado and casa(r[1], leituras)), None)
        if regra is None:
            registrar(n, f"⊘ sem transição para {leituras}")
            raise RuntimeError(f"MT travada em {estado} lendo {leituras}")
        _, _, (novo_estado, escritas, movimentos) = regra
        for f, e, mv in zip(fitas, escritas, movimentos):
            f.write(e)
            f.move(mv)
        estado = novo_estado
        n += 1
        registrar(n, f"-> {estado}")

    aceito = estado in FINAL_STATES
    return aceito, passos


# ---------------------------------------------------------------------------
# 3. Exemplos, verificação e linha de comando
# ---------------------------------------------------------------------------

EXEMPLOS = [
    ("aab",   "ab",   True),    # ocorre na posição 1
    ("aaa",   "ab",   False),   # nunca ocorre
    ("abba",  "bb",   True),    # ocorre na posição 1
    ("abab",  "aba",  True),    # ocorre na posição 0
    ("ab",    "abb",  False),   # padrão maior que o texto
    ("baaab", "aaa",  True),    # ocorre na posição 1
    ("bbbb",  "a",    False),   # símbolo ausente
    ("ab",    "",     True),    # padrão vazio ocorre em qualquer texto
]


def main(argv):
    if len(argv) > 2:
        T, P = argv[1], argv[2]
        print(f"Busca de padrão:  P=\"{P}\"  em  T=\"{T}\"\n")
        aceito, _ = executar(T, P, trace=True)
        print("\nRESULTADO:", "ACEITA (P é subcadeia de T)" if aceito
              else "REJEITA (P não ocorre em T)")
        return

    print("=" * 60)
    print("MT Multifita (2 fitas) — Busca de padrão (string matching)")
    print("=" * 60)
    for T, P, esperado in EXEMPLOS:
        aceito, _ = executar(T, P)
        ref = (P in T)
        ok = (aceito == esperado == ref)
        print(f"  {'OK ' if ok else 'ERRO'}  T={T:<7} P={P:<5} -> "
              f"{'ACEITA' if aceito else 'REJEITA':<8} (Python: {P!r} in {T!r} = {ref})")


if __name__ == "__main__":
    import sys
    main(sys.argv)
