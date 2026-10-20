# Parte D — Modelo de ameaças simplificado

**Responsável:** *Giovani Barros Luna Gomes*

| ID | Ativo | Ameaça | Vetor | Impacto | Controle |
|---|---|---|---|---|---|
| R-01 | Processo de planejamento do LLM e integridade do agente | Injeção de instrução indireta (*Indirect Prompt Injection*) | O conteúdo bruto devolvido pela Jina segue para o sumarizador sem separação entre dado e instrução (`tool_visit.py`). | O agente lê uma instrução maliciosa oculta no site, abandona a tarefa original do usuário e produz uma resposta controlada pelo atacante. | Sanitizar o HTML extraído (ex: via *BeautifulSoup*) e separar estritamente o conteúdo recuperado das instruções base no prompt. |
| R-02 | Resposta final (saída do sistema) | Omissão de divergências factuais e falsa noção de consenso | O `EXTRACTOR_PROMPT` resume cada página isoladamente, sem etapa de reconciliação de informações (`inference/prompt.py`). | O usuário recebe uma resposta irreal ou enviesada como se fosse verdade absoluta, já que o modelo não confronta fontes que discordam entre si. | Modificar a arquitetura para realizar cruzamento de fontes conflitantes antes da resposta e exigir URL com trecho de apoio validado. |
| R-03 | Consumo de tokens (API) e Qualidade da Interação | Prompt ambíguo que leva a resposta indevida e alucinação de persona | Usuário insere comandos vagos e o agente (operando com `temperature=0.85`) tenta adivinhar o contexto ao invés de perguntar. | Desperdício de requisições de API, fluxos de raciocínio caóticos e entrega de informações genéricas ou fora da persona esperada. | Reformular o *System Prompt* orientando o agente a recusar agir por suposição e solicitar ativamente mais contexto quando a entrada for insuficiente. |

## Resumo dos Riscos Mapeados

O primeiro risco avaliado (R-01) trata da vulnerabilidade de injeção indireta de prompt. Como o sistema extrai o conteúdo bruto de páginas da web sem a devida sanitização das tags, um site malicioso pode esconder comandos invisíveis no código HTML. Quando o agente consome essa página, ele não consegue separar o que é dado e o que é instrução, correndo o risco de abandonar a tarefa do usuário para seguir a ordem do atacante.

O segundo risco (R-02) aborda uma falha arquitetural no tratamento de fontes conflitantes, sendo o foco central da Missão D. O código atual resume cada página pesquisada de maneira isolada na memória, o que impossibilita a reconciliação de informações contraditórias. Consequentemente, o modelo pode entregar uma resposta enviesada ou que omite divergências factuais importantes, gerando uma falsa sensação de consenso científico.

Por fim, o terceiro risco (R-03) afeta diretamente a usabilidade e o consumo de recursos da aplicação. Devido ao uso de uma temperatura alta e à falta de regras rígidas no prompt de sistema, o agente não sabe lidar com comandos curtos ou ambíguos. Em vez de interromper o fluxo e pedir esclarecimentos ao usuário, o sistema tenta "adivinhar" o contexto, o que provoca alucinações de comportamento e desperdício de chamadas pagas (tokens) às APIs de busca.

## Pontos de partida levantados na Atividade 1

A análise estática da Atividade 1 identificou dois candidatos diretos, ambos documentados em [`parteA-ficha-da-missao.md`](parteA-ficha-da-missao.md), seção A.2:

- **Injeção indireta via conteúdo recuperado** — o conteúdo bruto devolvido pela Jina segue para o sumarizador sem separação entre dado e instrução (`tool_visit.py`).
- **Arbitragem silenciosa entre fontes divergentes** — o `EXTRACTOR_PROMPT` resume cada página isoladamente, sem etapa de reconciliação (`inference/prompt.py`).
