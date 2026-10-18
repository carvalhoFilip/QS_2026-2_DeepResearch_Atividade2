# Parte D — Modelo de ameaças simplificado

**Responsável:** *a definir (pessoa 4)*

> Obrigatório incluir ao menos um risco de injeção de instruções e um risco relacionado a fontes, dados ou saída do sistema.

| ID | Ativo | Ameaça | Vetor | Impacto | Controle |
|---|---|---|---|---|---|
| R-01 | | | | | |
| R-02 | | | | | |
| R-03 | | | | | |

## Pontos de partida levantados na Atividade 1

A análise estática da Atividade 1 identificou dois candidatos diretos, ambos documentados em [`parteA-ficha-da-missao.md`](parteA-ficha-da-missao.md), seção A.2:

- **Injeção indireta via conteúdo recuperado** — o conteúdo bruto devolvido pela Jina segue para o sumarizador sem separação entre dado e instrução (`tool_visit.py`).
- **Arbitragem silenciosa entre fontes divergentes** — o `EXTRACTOR_PROMPT` resume cada página isoladamente, sem etapa de reconciliação (`inference/prompt.py`).
