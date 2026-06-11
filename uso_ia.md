# Declaração de Uso de Inteligência Artificial

Conforme a Seção 8 da atividade, declaramos abaixo como ferramentas de IA foram
utilizadas neste trabalho.

## Ferramenta e data

- **Ferramenta:** Claude (Anthropic).
- **Data aproximada de uso:** junho de 2026.

## Finalidade do uso

A IA foi usada como **apoio**, nas seguintes etapas:

- Discussão e escolha dos dois modelos (Autômato de Pilha e Máquina de Turing
  com Múltiplas Fitas), avaliando facilidade de explicação e de implementação.
- Geração inicial dos simuladores em Python, com a definição formal explícita
  (estados, alfabetos, função de transição) separada da rotina de simulação.
- Conversão das máquinas para o formato JFLAP (`.jff`).
- Geração dos rastreamentos de execução e dos testes de verificação automática.
- Organização do repositório e redação inicial do README.

## Resumo dos prompts utilizados

- "Dentre as nove opções da atividade, quais modelos são mais simples de
  explicar e implementar?"
- "Implemente em Python um PDA que reconheça delimitadores `( ) [ ] { }`
  balanceados e uma MT de múltiplas fitas que some dois números binários, com
  definição formal e rastreamento passo a passo."
- "Gere casos de teste (aceitos, rejeitados e de fronteira) e verifique a
  corretude automaticamente."
- "Converta as duas máquinas para arquivos `.jff` do JFLAP."

## O que a equipe revisou, modificou ou rejeitou

> **A PREENCHER PELA EQUIPE antes da entrega.** Sejam específicos; isto é o que
> sustenta a nota de domínio conceitual na arguição. Sugestões do que registrar:
>
> - Quais trechos cada integrante leu, executou e entendeu.
> - Decisões de modelagem discutidas/alteradas pela equipe, por exemplo:
>   - a MT foi ajustada para ter **10 estados** (o requisito é mais de 8);
>   - a convenção de representação dos números nas fitas (MSB à esquerda) e a
>     fase de cópia/inversão do resultado para a fita 1;
>   - a expansão da tabela da MT para **44 transições concretas** no `.jff`,
>     já que o JFLAP não admite curingas nas leituras.
> - Qualquer parte que a equipe reescreveu, renomeou ou corrigiu por conta própria.

## Declaração final

Declaramos que todos os integrantes revisaram os trechos incorporados,
compreendem o funcionamento das duas máquinas (definição formal, transições,
código e resultados dos testes) e são capazes de explicá-los na arguição.

Felipe de Freitas · Benjamin Suzuki · Ryan Cavalcanti · Lucas Mesquita
