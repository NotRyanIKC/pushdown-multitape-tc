from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 1. DEFINIÇÃO FORMAL DO PDA   M = (Q, Σ, Γ, δ, q0, Z0, F)
# ---------------------------------------------------------------------------

# Estados: leem o nome das tags e distinguem abertura de fechamento.
Q = {
    "q_start",  # estado inicial (coloca o autômato no laço de leitura)
    "q0",       # entre tags: espera '<' (início de tag) ou o fim do documento
    "q_lt",     # leu '<': pode vir um nome de tag (abertura) ou '/' (fechamento)
    "q_oh",     # abertura: leu 'h', falta o dígito (1 ou 2) para <h1>/<h2>
    "q_ogt",    # abertura: nome lido, espera '>'
    "q_c0",     # fechamento: leu '</', espera o nome da tag a fechar
    "q_ch",     # fechamento: leu 'h', falta o dígito (1 ou 2)
    "q_cgt",    # fechamento: nome lido e desempilhado, espera '>'
    "q_accept", # estado final
}                # |Q| = 9 estados (> 8, conforme exigido)
SIGMA = {"<", ">", "/", "p", "h", "1", "2"}     # alfabeto de entrada
GAMMA = {"Z", "P", "A", "B"}                    # pilha: Z=fundo, P=<p>, A=<h1>, B=<h2>
START_STATE = "q_start"
START_STACK = "Z"
FINAL_STATES = {"q_accept"}

EPS = "ε"   # transição vazia (não consome entrada)


TAG_STACK = {"p": "P", "1": "A", "2": "B"}      # 1/2 vêm depois do 'h'


def construir_delta():
    """δ: (estado, entrada|ε, topo) -> (novo_estado, string_que_substitui_o_topo).
    Empilhar X sobre t => substitui t por 'X'+t (X no topo).
    Desempilhar        => substitui t por ''     (remove o topo).
    Manter             => substitui t por t.
    """
    delta = {}
    tops = sorted(GAMMA)

    # (0) Inicialização.
    delta[("q_start", EPS, "Z")] = ("q0", "Z")

    # (1) Início de uma tag: lê '<' (pilha inalterada).
    for t in tops:
        delta[("q0", "<", t)] = ("q_lt", t)

    # (2) ABERTURA -------------------------------------------------------
    # <p>: empilha P
    for t in tops:
        delta[("q_lt", "p", t)] = ("q_ogt", "P" + t)
    # 'h' de <h1>/<h2>: aguarda o dígito (pilha inalterada)
    for t in tops:
        delta[("q_lt", "h", t)] = ("q_oh", t)
    # <h1>: empilha A ; <h2>: empilha B
    for t in tops:
        delta[("q_oh", "1", t)] = ("q_ogt", "A" + t)
        delta[("q_oh", "2", t)] = ("q_ogt", "B" + t)
    # fecha a tag de abertura com '>'
    for t in tops:
        delta[("q_ogt", ">", t)] = ("q0", t)

    # (3) FECHAMENTO -----------------------------------------------------
    # '/' indica tag de fechamento
    for t in tops:
        delta[("q_lt", "/", t)] = ("q_c0", t)
    # </p>: só fecha se o topo for P (desempilha)
    delta[("q_c0", "p", "P")] = ("q_cgt", "")
    # 'h' de </h1>,</h2>: aguarda o dígito (pilha inalterada)
    for t in tops:
        delta[("q_c0", "h", t)] = ("q_ch", t)
    # </h1>: só fecha se o topo for A ; </h2>: só se for B
    delta[("q_ch", "1", "A")] = ("q_cgt", "")
    delta[("q_ch", "2", "B")] = ("q_cgt", "")
    # fecha a tag de fechamento com '>'
    for t in tops:
        delta[("q_cgt", ">", t)] = ("q0", t)

    # (4) ACEITAÇÃO: fim da entrada com a pilha de volta ao fundo Z.
    delta[("q0", EPS, "Z")] = ("q_accept", "Z")

    return delta


DELTA = construir_delta()


# ---------------------------------------------------------------------------
# 2. SIMULADOR
# ---------------------------------------------------------------------------

@dataclass
class Config:
    estado: str
    entrada: str
    pilha: list = field(default_factory=list)   # topo no índice 0

    def topo(self) -> str:
        return self.pilha[0] if self.pilha else ""

    def pilha_str(self) -> str:
        return "".join(self.pilha) if self.pilha else "ε"

    def entrada_str(self) -> str:
        return self.entrada if self.entrada else "ε"


def aplicar(destino, cfg: Config, consumiu: bool) -> Config:
    novo_estado, subst = destino
    nova_pilha = cfg.pilha[1:]
    if subst:
        nova_pilha = list(subst) + nova_pilha
    nova_entrada = cfg.entrada[1:] if consumiu else cfg.entrada
    return Config(novo_estado, nova_entrada, nova_pilha)


def aceita(cadeia: str, trace: bool = False):
    """Executa o PDA (determinístico). Retorna (aceito, passos, motivo)."""
    cfg = Config(START_STATE, cadeia, [START_STACK])
    passos = []

    def registrar(desc):
        linha = (f"({cfg.estado:<8} entrada={cfg.entrada_str():<14} "
                 f"pilha={cfg.pilha_str():<8}) {desc}")
        passos.append(linha)
        if trace:
            print(linha)

    registrar("← configuração inicial")

    for _ in range(100000):
        topo = cfg.topo()
        proximo = cfg.entrada[0] if cfg.entrada else None

        destino = None
        consumiu = False
        if proximo is not None and (cfg.estado, proximo, topo) in DELTA:
            destino = DELTA[(cfg.estado, proximo, topo)]
            consumiu = True
        elif (cfg.estado, EPS, topo) in DELTA:
            destino = DELTA[(cfg.estado, EPS, topo)]

        if destino is None:
            if cfg.estado in FINAL_STATES and not cfg.entrada:
                return True, passos, "entrada consumida em estado final"
            if not cfg.entrada and topo != START_STACK:
                motivo = "fim da entrada com tags ainda abertas"
            elif proximo is not None and cfg.estado in ("q_c0", "q_ch"):
                motivo = f"tag de fechamento não casa com a tag aberta no topo ('{topo}')"
            elif proximo is not None:
                motivo = f"símbolo '{proximo}' inesperado em {cfg.estado}"
            else:
                motivo = "máquina travada sem aceitação"
            registrar(f"⊘ trava — {motivo}")
            return False, passos, motivo

        acao = "ε-move" if not consumiu else f"lê '{proximo}'"
        cfg = aplicar(destino, cfg, consumiu)
        if cfg.estado in FINAL_STATES and not cfg.entrada:
            registrar(f"{acao} → ACEITA")
            return True, passos, "entrada consumida em estado final com pilha = Z"
        registrar(acao)

    return False, passos, "limite de passos excedido"


# ---------------------------------------------------------------------------
# 3. Exemplos / linha de comando
# ---------------------------------------------------------------------------

EXEMPLOS_ACEITOS = [
    "",
    "<p></p>",
    "<h1></h1>",
    "<h2></h2>",
    "<p><h1></h1></p>",
    "<p></p><h2></h2>",
    "<h1><p></p><p></p></h1>",
]
EXEMPLOS_REJEITADOS = [
    "<p></h1>",            # fecha tag errada
    "<p>",                 # não fechou
    "</p>",                # fecha sem abrir
    "<p><h1></p></h1>",    # cruzamento de tags
    "<h3></h3>",           # tag inexistente (dígito 3)
    "<p></p></p>",         # fechamento sobrando
    "<>",                  # tag vazia
]


def main(argv):
    if len(argv) > 1:
        cadeia = argv[1]
        print(f"Entrada: \"{cadeia}\"\n")
        ok, _, motivo = aceita(cadeia, trace=True)
        print("\nRESULTADO:", "ACEITA" if ok else "REJEITA", f"({motivo})")
        return

    print("=" * 60)
    print("PDA — Validador de tags aninhadas  <p> <h1> <h2>")
    print("=" * 60)
    print("\n# Casos que DEVEM ser aceitos:")
    for c in EXEMPLOS_ACEITOS:
        ok, _, motivo = aceita(c)
        print(f"  {'OK ' if ok else 'ERRO'}  \"{c}\"")
    print("\n# Casos que DEVEM ser rejeitados:")
    for c in EXEMPLOS_REJEITADOS:
        ok, _, motivo = aceita(c)
        print(f"  {'OK ' if not ok else 'ERRO'}  \"{c}\"  ->  {motivo}")


if __name__ == "__main__":
    import sys
    main(sys.argv)
