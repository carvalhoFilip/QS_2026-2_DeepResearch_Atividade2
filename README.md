# Equipe 06 — DeepResearch · Atividade 2 (AV2)

**Missão Contexto Confiável** — verificação, segurança e melhoria de aplicações de IA generativa
Disciplina: Qualidade de Software — 2026.2

| | |
|---|---|
| Projeto analisado | https://github.com/Alibaba-NLP/DeepResearch |
| Licença | Apache-2.0 |
| Commit/tag avaliado | *a registrar* |
| Missão escolhida | **D — Contexto sob Pressão** |
| Fluxo avaliado | Busca documental com resposta fundamentada em fontes |
| Atividade 1 | https://github.com/BrennoPh/QS_2026-2_DeepReserach_Atividade1 |

## A missão

Comparação do comportamento do agente quando o contexto fornecido varia entre **correto, ausente, irrelevante e conflitante**.

A escolha tem continuidade direta com a Atividade 1, que previu por análise estática — sem conseguir executar — dois comportamentos que esta atividade submete a teste: o `EXTRACTOR_PROMPT` resume cada página isoladamente, sem reconciliar fontes divergentes; e o `SYSTEM_PROMPT` não traz instrução que obrigue declarar evidência insuficiente.

## Partes

| Parte | Conteúdo | Responsável | Documento |
|---|---|---|---|
| A | Ficha da missão | Filipe de Carvalho Godoy | [docs/parteA-ficha-da-missao.md](docs/parteA-ficha-da-missao.md) |
| B | Laboratório de contexto e prompts | *a definir* | [docs/parteB-laboratorio-prompts.md](docs/parteB-laboratorio-prompts.md) |
| C | Verificação de fontes e saída estruturada | *a definir* | [docs/parteC-verificacao-fontes.md](docs/parteC-verificacao-fontes.md) |
| D | Modelo de ameaças simplificado | Giovani Barros Luna Gomes | [docs/parteD-modelo-ameacas.md](docs/parteD-modelo-ameacas.md) |
| E | Testes obrigatórios | Thiago Mecena Silva | [docs/parteE-testes-obrigatorios.md](docs/parteE-testes-obrigatorios.md) |
| — | Classificação de falhas e plano de melhoria | *a definir* | [docs/classificacao-falhas-melhoria.md](docs/classificacao-falhas-melhoria.md) |

## Estrutura do repositório

```
docs/         uma parte por arquivo
evidencias/   saídas brutas, capturas e logs, por parte
resultados/   planilha de casos de teste e gráficos
assets/       imagens do relatório
```

## Integrantes

| Nº | Nome | Matrícula |
|---|---|---|
| 01 | Brenno Phelipe Silva dos Santos | 202400050750 |
| 02 | Daniel José Silva Trindade | 202200059698 |
| 03 | Emilly Kathellen de Jesus Oliveira | 202400050830 |
| 04 | Filipe de Carvalho Godoy | 202100115408 |
| 05 | Giovani Barros Luna Gomes | 202400050885 |
| 06 | Lais Santos de Sousa | 202100115364 |
| 07 | Thiago Mecena Silva | 202100045840 |

## Contribuição individual

| Nome | Matrícula | Parte | Contribuição |
|---|---|---|---|
| Brenno Phelipe Silva dos Santos | 202400050750 | *a definir* | |
| Daniel José Silva Trindade | 202200059698 | *a definir* | |
| Emilly Kathellen de Jesus Oliveira | 202400050830 | *a definir* | |
| Filipe de Carvalho Godoy | 202100115408 | A — Ficha da missão | Ficha do sistema atualizada a partir da Atividade 1, com ferramentas, prompts e fontes de dados do fluxo avaliado; desenho do fluxo simplificado mapeado ao código do projeto; classificação dos dados do recorte em público, sintético, interno e não permitido para teste; reestruturação do repositório. |
| Giovani Barros Luna Gomes | 202400050885 | *a definir* | |
| Lais Santos de Sousa | 202100115364 | *a definir* | |
| Thiago Mecena Silva | 202100045840 | Elaboração e execução prática de 5 casos de teste obrigatórios da Parte E no pipeline do DeepResearch (cobrindo testes funcionais, de contexto, metamórficos e adversariais de privacidade/LGPD); coleta de logs e consolidação das evidências de execução via API; apuração das métricas de qualidade (cobertura de citações, precisão, taxa de injeção e latência); estruturação da planilha de casos de teste e da planilha de evidências e métricas; e apresentação demonstrativa dos resultados no vídeo da equipe. | |

## Vídeo da atividade

**URL:** *a preencher*

Até 20 minutos, com participação de todos. Detalhes em [`VIDEO.md`](VIDEO.md).

## Entregáveis (até 21/10/2026, 23h59)

- [ ] Relatório técnico em PDF
- [ ] Repositório com README, prompts versionados, casos de teste, resultados, evidências, tabela de ameaças e plano de melhoria
- [ ] Planilha ou CSV com casos de teste e resultados
- [ ] Apresentação em PDF ou slides
- [ ] Vídeo de até 20 minutos, URL no README, no relatório e em `VIDEO.md`
- [ ] Tabela de contribuição individual

**Apresentação:** 22/10/2026 — 10 a 12 minutos, mais 3 a 5 de perguntas.
