# Declaração de Uso de Inteligência Artificial

## Ferramenta e data

- **Ferramenta:** Claude (Anthropic).
- **Data aproximada de uso:** junho de 2026.

## Finalidade do uso

A IA foi usada como **apoio**, nas seguintes etapas:

- Discussão e escolha dos dois modelos (Autômato de Pilha e Máquina de Turing
  com Múltiplas Fitas), avaliando facilidade de explicação e de implementação.
- Geração inicial dos simuladores em Python, com a definição formal explícita
  (estados, alfabetos, função de transição) separada da rotina de simulação.
- Geração dos rastreamentos de execução e dos testes de verificação automática.
- Organização do repositório e redação inicial do README.
- Geração do deck de slides da apresentação.

## Resumo dos prompts utilizados

- "Dentre as nove opções da atividade, quais modelos são mais simples de
  explicar e implementar?"
- "Implemente em Python um PDA que valide tags aninhadas (`<p>`, `<h1>`, `<h2>`),
  casando abertura/fechamento pela pilha, e uma MT de múltiplas fitas que faça
  busca de padrão, com definição formal e rastreamento passo a passo."
- "Gere casos de teste (aceitos, rejeitados e de fronteira) e verifique a
  corretude automaticamente."
- "Monte o deck de slides do seminário (tema escuro) refletindo os dois modelos."


## O que a equipe modificou, corrigiu ou rejeitou

- Verificamos nos slides das aulas o que já havia sido trabalhado. **Rejeitamos
  a soma binária**, pois a MT de soma já foi vista em aula; trocamos por **busca
  de padrão**.
- Trocamos o PDA de delimitadores `( ) [ ] { }` (que teria apenas 3 estados) por
  um **validador de tags nomeadas**, para cumprir o requisito de **mais de 8
  estados** de forma legítima (a leitura do nome de cada tag exige controle
  finito). O PDA final tem **9 estados** e a MT tem **9 estados**.
- Para o JFLAP, expandimos a tabela da MT para **31 transições concretas**, já
  que o JFLAP não admite curingas nas leituras.
- Corrigimos algumas inconsistências no slide como nomes e datas erradas e citações inválidas


## Declaração final

Declaramos que todos os integrantes revisaram os trechos incorporados,
compreendem o funcionamento das duas máquinas (definição formal, transições,
código e resultados dos testes) e são capazes de explicá-los na arguição.

Felipe de Freitas · Benjamin Suzuki · Ryan Cavalcanti · Lucas Mesquita
