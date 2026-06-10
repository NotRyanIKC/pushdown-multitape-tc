"""
Autômato de Pilha (PDA) — Reconhecedor de delimitadores balanceados.

Problema: dada uma cadeia formada pelos símbolos ( ) [ ] { }, decidir se os
delimitadores estão corretamente balanceados e aninhados.
  Exemplos aceitos:  "()", "([]{})", "{[()]}"
  Exemplos rejeitados: "(]", "([)]", "(()"

Este arquivo separa explicitamente:
  1. A DEFINIÇÃO FORMAL do PDA (a 7-upla M = (Q, Σ, Γ, δ, q0, Z0, F)).
  2. O SIMULADOR genérico que executa qualquer PDA assim definido, com
     rastreamento (trace) passo a passo de (estado, entrada restante, pilha).

A linguagem reconhecida é Livre de Contexto e NÃO é regular: um autômato
finito não consegue contar a profundidade de aninhamento, mas a pilha sim.

Uso:
    python3 automato_pilha.py            # roda a bateria de exemplos
    python3 automato_pilha.py "([]{})"   # testa uma cadeia, mostrando o trace
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# 1. DEFINIÇÃO FORMAL DO PDA   M = (Q, Σ, Γ, δ, q0, Z0, F)
# ---------------------------------------------------------------------------

Q = {"q0", "q1", "q2"}                       # estados
SIGMA = {"(", ")", "[", "]", "{", "}"}       # alfabeto de entrada
GAMMA = {"Z", "(", "[", "{"}                 # alfabeto da pilha (Z = fundo)
START_STATE = "q0"
START_STACK = "Z"                            # símbolo inicial da pilha
FINAL_STATES = {"q2"}                        # aceitação por estado final

# Pares de abertura/fechamento
ABRE = {"(": ")", "[": "]", "{": "}"}
TOPO_DE = {")": "(", "]": "[", "}": "{"}      # qual topo um fechamento exige

# Função de transição δ.
# Cada regra é uma tupla:
#   (estado, símbolo_de_entrada_ou_ε, topo_da_pilha)
#       -> (novo_estado, string_que_substitui_o_topo)
# Convenção da pilha (topo à esquerda):
#   - empilhar X sobre topo t  => substitui t por "X t"  (X fica no topo)
#   - desempilhar               => substitui t por ""     (remove o topo)
#   - manter                    => substitui t por "t"
#
# EPS representa a transição vazia (ε), que não consome entrada.
EPS = "ε"

def construir_delta():
    delta = {}

    # (0) Inicialização: do estado inicial entra no laço de leitura, mantendo Z.
    delta[("q0", EPS, "Z")] = ("q1", "Z")

    # (1) EMPILHAR um delimitador de abertura, qualquer que seja o topo atual.
    #     Definimos a transição para todos os topos possíveis (Z, (, [, {),
    #     deixando o formalismo completo (δ é total sobre os casos relevantes).
    for abre in ("(", "[", "{"):
        for topo in GAMMA:
            delta[("q1", abre, topo)] = ("q1", abre + " " + topo)

    # (2) DESEMPILHAR ao ler um fechamento, somente se o topo for o par correto.
    for fecha, topo_exigido in TOPO_DE.items():
        delta[("q1", fecha, topo_exigido)] = ("q1", "")   # pop

    # (3) ACEITAÇÃO: fim da entrada com a pilha de volta ao fundo Z.
    delta[("q1", EPS, "Z")] = ("q2", "Z")

    return delta


DELTA = construir_delta()


# ---------------------------------------------------------------------------
# 2. SIMULADOR (configurações e passo de execução)
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """Configuração instantânea do PDA: estado, entrada restante e pilha."""
    estado: str
    entrada: str                 # parte ainda não lida (índice 0 = próximo símbolo)
    pilha: list = field(default_factory=list)   # topo no índice 0

    def topo(self) -> str:
        return self.pilha[0] if self.pilha else ""

    def pilha_str(self) -> str:
        return "".join(self.pilha) if self.pilha else "ε"

    def entrada_str(self) -> str:
        return self.entrada if self.entrada else "ε"


def aplicar(regra_destino, cfg: Config, consumiu_simbolo: bool) -> Config:
    """Gera a próxima configuração a partir de uma regra (novo_estado, subst_topo)."""
    novo_estado, subst = regra_destino
    nova_pilha = cfg.pilha[1:]                    # remove o topo atual
    if subst:                                     # e empilha a substituição
        simbolos = subst.split(" ") if " " in subst else [subst]
        nova_pilha = simbolos + nova_pilha
    nova_entrada = cfg.entrada[1:] if consumiu_simbolo else cfg.entrada
    return Config(novo_estado, nova_entrada, nova_pilha)


def aceita(cadeia: str, trace: bool = False):
    """
    Executa o PDA (determinístico) sobre `cadeia`.
    Retorna (aceito: bool, passos: list[str], motivo: str).
    """
    cfg = Config(START_STATE, cadeia, [START_STACK])
    passos = []
    motivo = ""

    def registrar(desc):
        linha = f"({cfg.estado:>2}, entrada={cfg.entrada_str():<8}, pilha={cfg.pilha_str():<8}) {desc}"
        passos.append(linha)
        if trace:
            print(linha)

    registrar("← configuração inicial")

    # Limite de passos para evitar laços de ε (segurança).
    for _ in range(10000):
        topo = cfg.topo()
        proximo = cfg.entrada[0] if cfg.entrada else None

        # Preferimos transições que consomem entrada; só usamos ε quando
        # não há mais entrada a consumir naquele topo (PDA determinístico).
        regra = None
        consumiu = False
        if proximo is not None and (cfg.estado, proximo, topo) in DELTA:
            regra = DELTA[(cfg.estado, proximo, topo)]
            consumiu = True
        elif (cfg.estado, EPS, topo) in DELTA:
            regra = DELTA[(cfg.estado, EPS, topo)]
            consumiu = False

        if regra is None:
            # Sem transição aplicável: a máquina trava.
            if cfg.estado in FINAL_STATES and not cfg.entrada:
                motivo = "entrada consumida em estado final"
                return True, passos, motivo
            if proximo is not None and proximo in TOPO_DE and topo != TOPO_DE[proximo]:
                motivo = f"fechamento '{proximo}' não casa com o topo '{topo or 'ε'}'"
            elif not cfg.entrada and topo != START_STACK:
                motivo = "fim da entrada com delimitadores ainda abertos na pilha"
            elif proximo is not None:
                motivo = f"nenhuma transição para (estado={cfg.estado}, lê='{proximo}', topo='{topo}')"
            else:
                motivo = "máquina travada sem aceitação"
            registrar(f"⊘ trava — {motivo}")
            return False, passos, motivo

        acao = "ε-move" if not consumiu else f"lê '{proximo}'"
        cfg = aplicar(regra, cfg, consumiu)

        if cfg.estado in FINAL_STATES and not cfg.entrada:
            registrar(f"{acao} → ACEITA")
            motivo = "entrada consumida em estado final com pilha = Z"
            return True, passos, motivo
        registrar(acao)

    motivo = "limite de passos excedido"
    return False, passos, motivo


# ---------------------------------------------------------------------------
# 3. Execução de exemplos / linha de comando
# ---------------------------------------------------------------------------

EXEMPLOS_ACEITOS = ["()", "([]{})", "{[()]}", "(())", "[]{}()", ""]
EXEMPLOS_REJEITADOS = ["(]", "([)]", "(()", "}{", ")(", "((("]


def main(argv):
    if len(argv) > 1:
        cadeia = argv[1]
        print(f"Entrada: \"{cadeia}\"\n")
        ok, _, motivo = aceita(cadeia, trace=True)
        print("\nRESULTADO:", "ACEITA ✓" if ok else "REJEITA ✗", f"({motivo})")
        return

    print("=" * 60)
    print("PDA — Delimitadores balanceados  ( ) [ ] { }")
    print("=" * 60)
    print("\n# Casos que DEVEM ser aceitos:")
    for c in EXEMPLOS_ACEITOS:
        ok, _, motivo = aceita(c)
        marca = "✓" if ok else "✗ (ERRO!)"
        print(f"  {marca}  \"{c}\"  -> {motivo}")

    print("\n# Casos que DEVEM ser rejeitados:")
    for c in EXEMPLOS_REJEITADOS:
        ok, _, motivo = aceita(c)
        marca = "✓" if not ok else "✗ (ERRO!)"
        print(f"  {marca}  \"{c}\"  -> {motivo}")


if __name__ == "__main__":
    import sys
    main(sys.argv)
