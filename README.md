# Equipe 06 — DeepResearch · Atividade 2

**Missão D — Contexto sob Pressão**
Disciplina: Qualidade de Software — AV2 (2026.2)

Avaliação de como o agente se comporta quando o contexto fornecido varia entre correto, ausente, irrelevante e conflitante.

| | |
|---|---|
| Projeto analisado | https://github.com/Alibaba-NLP/DeepResearch |
| Licença do projeto | Apache-2.0 |
| Commit/tag avaliado | *a registrar* |
| Atividade 1 | https://github.com/BrennoPh/QS_2026-2_DeepReserach_Atividade1 |

## A missão

Uma mesma bateria de perguntas é submetida ao agente sob quatro condições de contexto. O resultado da atividade é a **comparação entre as condições**, não o desempenho em cada uma isoladamente.

| Condição | Contexto fornecido | O que se observa |
|---|---|---|
| A | Documento que responde a pergunta | Baseline: acerto, fonte citada, formato |
| B | Nenhum documento | Declara o limite ou inventa? |
| C | Documento real, sobre outro assunto | Usa o que não serve só porque está lá? |
| D | Dois documentos que se contradizem | Reporta o conflito ou escolhe em silêncio? |

## Índice das partes

| Parte | Eixo | Responsável | Documento |
|---|---|---|---|
| 1 | Protocolo, corpus e rubrica | *a definir* | [docs/parte1-protocolo.md](docs/parte1-protocolo.md) |
| 2 | Condição A — contexto correto | *a definir* | [docs/parte2-condicao-a.md](docs/parte2-condicao-a.md) |
| 3 | Condição B — contexto ausente | *a definir* | [docs/parte3-condicao-b.md](docs/parte3-condicao-b.md) |
| 4 | Condição C — contexto irrelevante | *a definir* | [docs/parte4-condicao-c.md](docs/parte4-condicao-c.md) |
| 5 | Condição D — contexto conflitante | *a definir* | [docs/parte5-condicao-d.md](docs/parte5-condicao-d.md) |
| 6 | Métricas e consolidação | *a definir* | [docs/parte6-metricas.md](docs/parte6-metricas.md) |
| 7 | Achados, plano de melhoria e limitações | *a definir* | [docs/parte7-achados.md](docs/parte7-achados.md) |

A Parte 1 precisa estar fechada antes de qualquer execução: se o protocolo não for idêntico entre as quatro condições, a comparação não se sustenta. A Parte 6 deve ser conduzida por quem não executou nenhuma condição, para que ninguém pontue o próprio resultado.

## Estrutura do repositório

```
docs/         uma parte por arquivo
protocolo/    perguntas-base, definição das condições, rubrica de pontuação
corpus/       documentos de contexto fabricados para cada condição
evidencias/   saídas brutas do agente, por condição e repetição
resultados/   planilha de pontuação e gráficos comparativos
assets/       imagens usadas no relatório
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

## Vídeo da atividade

**URL:** *a preencher*

Detalhes de gravação e participantes em [`VIDEO.md`](VIDEO.md).
