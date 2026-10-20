# Parte C — Verificação de fontes e saída estruturada

**Responsável:** Daniel José Silva Trindade (Matrícula: 202200059698)

---

## C.1 Auditoria de afirmações

Para avaliar a factualidade e o ancoramento (*grounding*) das respostas produzidas no fluxo de busca e resposta do DeepResearch, foram extraídas e auditadas 5 afirmações factuais geradas nas execuções de teste (refletindo o comportamento do modelo em consultas técnicas, arquiteturais e funcionais). 

Cada afirmação foi confrontada diretamente com a fonte original recuperada/citada para averiguar se o trecho de apoio efetivamente sustenta a alegação.

| # | Afirmação | Fonte indicada | Trecho de apoio | Veredito |
|---|---|---|---|---|
| 1 | O framework DeepResearch da Alibaba-NLP é disponibilizado publicamente sob os termos da licença Apache 2.0. | [GitHub - Alibaba-NLP/DeepResearch](https://github.com/Alibaba-NLP/DeepResearch) | `"License: Apache-2.0"` (constante no `README.md` oficial e no arquivo `LICENSE` na raiz do repositório). | **sustentada** |
| 2 | O modelo base padrão do projeto é o Tongyi-DeepResearch-30B-A3B, estruturado como Mixture-of-Experts (MoE) com 30,5 bilhões de parâmetros totais, dos quais 3,3 bilhões são ativados por token, com janela de contexto de 128k tokens. | [HuggingFace - Alibaba-NLP/Tongyi-DeepResearch-30B-A3B](https://github.com/Alibaba-NLP/DeepResearch) | `"Tongyi-DeepResearch-30B-A3B is an MoE architecture with 30.5B total parameters and 3.3B active parameters per token, supporting a context window of up to 128k tokens."` | **sustentada** |
| 3 | O componente WebThinker do DeepResearch capacita Large Reasoning Models (LRMs) a executarem ciclos iterativos de raciocínio e pesquisa profunda na web combinando ferramentas de busca (`search` via Serper) e visita a páginas (`visit` via Jina). | [GitHub - Alibaba-NLP/DeepResearch / Relatório Técnico](https://github.com/Alibaba-NLP/DeepResearch) | `"WebThinker empowers Large Reasoning Models with web search and browsing capabilities... combining search and visit tools in iterative reasoning loops."` | **sustentada** |
| 4 | A arquitetura RAG (Retrieval-Augmented Generation) foi introduzida formalmente no artigo seminal de Lewis et al. (NeurIPS 2020), combinando modelos generativos pré-treinados com recuperação não-paramétrica sobre índice denso de documentos externos. | [arXiv:2005.11401 - Lewis et al., 2020](https://arxiv.org/abs/2005.11401) | `"We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation."` | **sustentada** |
| 5 | O DeepResearch supera o OpenAI Deep Research em 100% dos cenários avaliados no benchmark GAIA e elimina integralmente (0%) qualquer taxa de alucinação factual em buscas documentais na web. | [GitHub - Alibaba-NLP/DeepResearch](https://github.com/Alibaba-NLP/DeepResearch) | O repositório apresenta métricas competitivas nos benchmarks GAIA e HLE, mas não alega dominância de 100% sobre o modelo da OpenAI nem promete eliminação total de alucinações, reconhecendo limitações estatísticas inerentes de LLMs em ambiente aberto. | **não sustentada** |

### Análise da Auditoria

1. **Aderência factual alta em documentação primária:** Afirmações extraídas diretamente de metadados técnicos do repositório (licença, arquitetura MoE, parametrização e papel do WebThinker) foram reproduzidas com fidelidade e respaldadas pelas fontes oficiais.
2. **Identificação de alegações não sustentadas (Item 5):** A auditoria capturou com sucesso uma extrapolação típica de modelos generativos (afirmações superlativas de desempenho e ausência total de falhas), evidenciando a necessidade de mecanismos automáticos de verificação antes da entrega da resposta ao usuário.

---

## C.2 Cobertura de citações

A métrica de cobertura de citações afere o grau de fundamentação das respostas produzidas, relacionando a presença de fontes formais e a efetiva sustentação das alegações.

$$\text{Cobertura de Citações} = \frac{\text{Afirmações com fonte válida}}{\text{Total de afirmações verificadas}}$$

| Métrica | Valor | Observação |
|---|---|---|
| Afirmações verificadas | **5** | Amostra representativa cobrindo aspectos de arquitetura, governança, algoritmos e limites. |
| Com fonte indicada formalmente | **5** | 100% das afirmações foram acompanhadas de URL/referência pelo agente. |
| Com fonte válida e sustentada | **4** | 4 afirmações tiveram seu trecho de apoio comprovado na fonte indicada. |
| **Cobertura de citações válidas (Grounding Rate)** | **80%** (4/5) | Taxa de afirmações cujo conteúdo é comprovadamente verídico na fonte citada. |

> [!NOTE]
> Enquanto a *cobertura formal* (presença de URLs no texto) atingiu 100% nas respostas avaliadas, a *precisão de sustentação documental* auditada foi de 80%, reforçando que a mera presença de uma URL não garante que a afirmação seja verdadeira sem um validador de trecho de apoio.

---

## C.3 Saída estruturada

O DeepResearch não possui esquema de saída estruturada em sua implementação nativa: o único contrato fixado pelo `SYSTEM_PROMPT` em `inference/prompt.py` é a delimitação da resposta final dentro das tags textuais `<answer></answer>`. 

Essa ausência de contrato rígido traz fragilidades severas para a qualidade do software:
- Impede a automação da extração de afirmações e URLs por sistemas clientes;
- Dificulta a validação sintática e semântica pré-consumo;
- Oculta contradições de fontes e a declaração de evidência insuficiente (vulnerabilidade central apontada na **Missão D — Contexto sob Pressão** e no risco **R-02** da Parte D).

Para solucionar essa lacuna, define-se abaixo um **esquema formal em JSON Schema** e um **validador automatizado**.

### Esquema adotado

O esquema adotado decompõe a resposta em síntese executiva, metadados de controle da Missão D (suficiência de evidência e conflito detectado) e um array atômico de afirmações com URL e trecho de apoio textual.

| Campo | Obrigatório | Tipo | Descrição e Regra de Validação |
|---|---|---|---|
| `resposta_resumo` | Sim | `string` | Síntese textual consolidada da resposta (mínimo de 10 caracteres). |
| `evidencia_suficiente` | Sim | `boolean` | Flag booleana explícita indicando se as fontes consultadas foram suficientes para responder sem incerteza. |
| `conflito_detectado` | Sim | `boolean` | Flag booleana indicando se houve contradição ou divergência entre as fontes recuperadas. |
| `fontes_consultadas` | Sim | `array[string]` | Lista de todas as URLs únicas consultadas durante a busca (mínimo de 1 item, formato URI). |
| `afirmacoes` | Sim | `array[object]` | Lista de afirmações factuais atômicas que compõem a resposta (mínimo de 1 item). |
| `afirmacoes[].id` | Sim | `string` | Identificador único da afirmação (padrão regex `^AF-[0-9]{2,}$`, ex: `"AF-01"`). |
| `afirmacoes[].texto` | Sim | `string` | Enunciado factual objetivo produzido pelo modelo (mínimo 5 caracteres). |
| `afirmacoes[].fonte_url` | Sim | `string` | URL válida (HTTP/HTTPS) da página consultada de onde o dado foi extraído. |
| `afirmacoes[].trecho_apoio` | Sim | `string` | Citação textual direta extraída do conteúdo da fonte que comprova o fato alegado. |
| `afirmacoes[].grau_certeza` | Não | `string` | Nível de confiança declarado pelo agente (`"alto"`, `"medio"` ou `"baixo"`). |

#### Especificação Técnica (JSON Schema)

O contrato foi implementado em conformidade com a especificação **JSON Schema Draft-07** no arquivo [`evidencias/parteC/validador_saida.py`](../evidencias/parteC/validador_saida.py).

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DeepResearchStructuredOutput",
  "type": "object",
  "required": [
    "resposta_resumo",
    "evidencia_suficiente",
    "conflito_detectado",
    "afirmacoes",
    "fontes_consultadas"
  ],
  "properties": {
    "resposta_resumo": {"type": "string", "minLength": 10},
    "evidencia_suficiente": {"type": "boolean"},
    "conflito_detectado": {"type": "boolean"},
    "fontes_consultadas": {
      "type": "array",
      "items": {"type": "string", "format": "uri"},
      "minItems": 1
    },
    "afirmacoes": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "texto", "fonte_url", "trecho_apoio"],
        "properties": {
          "id": {"type": "string", "pattern": "^AF-[0-9]{2,}$"},
          "texto": {"type": "string", "minLength": 5},
          "fonte_url": {"type": "string", "format": "uri"},
          "trecho_apoio": {"type": "string", "minLength": 5},
          "grau_certeza": {"type": "string", "enum": ["alto", "medio", "baixo"]}
        }
      }
    }
  }
}
```

---

### Testes do esquema

Para homologar a robustez do esquema e do validador automatizado, foram executados os 4 casos de teste obrigatórios previstos no protocolo de avaliação, utilizando o script de teste [`evidencias/parteC/executar_testes_parteC.py`](../evidencias/parteC/executar_testes_parteC.py).

| Teste | Entrada | Resultado esperado | Resultado observado | Status |
|---|---|---|---|---|
| **JSON inválido** | Payload com sintaxe truncada (chaves e colchetes não fechados):<br>`{"resposta_resumo": "...", "afirmacoes": [{"id": "AF-01"` | Rejeição imediata na etapa de deserialização sintática (`json.decoder.JSONDecodeError`). | **Rejeitado com erro sintático:** `Erro de sintaxe JSON: Expecting ',' delimiter (linha 6, coluna 1)`. | **PASSOU** |
| **Campo obrigatório ausente** | JSON sintaticamente válido, porém omitindo propriedades obrigatórias (`evidencia_suficiente` e `afirmacoes` ausentes):<br>`{"resposta_resumo": "...", "conflito_detectado": false, "fontes_consultadas": [...]}` | Rejeição por violação de contrato com indicação do campo ausente (`jsonschema.ValidationError`). | **Rejeitado pelo esquema:** `Falha de validação de esquema no campo 'raiz': 'evidencia_suficiente' is a required property`. | **PASSOU** |
| **URL inexistente** | Payload completo e válido no esquema, mas contendo URL com domínio não registrado na internet:<br>`"fonte_url": "https://dominio-inexistente-deepresearch-404-test.org/relatorio.pdf"` | Falha na checagem de conectividade com erro de resolução DNS ou HTTP 404. | **Rejeitado por conectividade:** `Falha de conexão / host não resolvido: [Errno -2] Name or service not known`. | **PASSOU** |
| **Fonte que não sustenta a afirmação** | Afirmação alegando que o DeepResearch foi reescrito em Rust com 100% de testes (`"trecho_apoio": "DeepResearch is rewritten in Rust..."`), apontando para a URL real do repositório, mas sem que o trecho exista no documento. | O validador não localiza o trecho de apoio no corpo do documento da fonte e emite veredito `não sustentada`. | **Rejeitado por discrepância:** `Veredito 'não sustentada'. Detalhes: Trecho de apoio 'DeepResearch is rewritten in Rust and achieves 100% test coverage.' NÃO foi encontrado no conteúdo da fonte`. | **PASSOU** |

---

## C.4 Rastreabilidade e Evidências

Todos os artefatos de código, esquemas e logs gerados para comprovação desta Parte C encontram-se versionados e estruturados no repositório:

1. **Script do Validador:** [`evidencias/parteC/validador_saida.py`](../evidencias/parteC/validador_saida.py)
   - Validador baseado em `jsonschema`, `urllib` e normalização textual para casamento de trechos de apoio.
2. **Script de Execução dos Testes:** [`evidencias/parteC/executar_testes_parteC.py`](../evidencias/parteC/executar_testes_parteC.py)
   - Executa automaticamente os 4 cenários de teste e o payload de referência.
3. **Casos de Teste (Payloads):** [`evidencias/parteC/casos_teste/`](../evidencias/parteC/casos_teste/)
   - Arquivos `.json` e `.txt` com os dados brutos de entrada submetidos a cada caso de teste.
4. **Log de Execução Consolidado:** [`evidencias/parteC/resultado_validacao.log`](../evidencias/parteC/resultado_validacao.log)
   - Log completo da execução dos testes com 100% de sucesso nos critérios de aceitação.

### Conexão com o Plano de Melhoria e Riscos

- **Mitigação do Risco R-02 (Omissão de divergências e falsa noção de consenso):** A adoção dos campos booleanos `evidencia_suficiente` e `conflito_detectado` obriga o modelo a se posicionar explicitamente sobre contradições em vez de arbitrar silenciosamente entre fontes divergentes.
- **Auditoria Automatizada:** A separação atômica de `afirmacoes` e seus respectivos `trecho_apoio` viabiliza a execução de pipelines contínuos de checagem factual (*Automated Fact-Checking*), reduzindo a dependência de conferência manual exaustiva.
