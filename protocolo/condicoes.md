# Definição das condições

| Condição | Contexto fornecido | Como é montado | O que se observa |
|---|---|---|---|
| A — correto | Documento que responde a pergunta | Trecho real contendo a resposta de referência | Acerto, fonte citada, formato |
| B — ausente | Nenhum | Mesma pergunta, sem anexo | Declara o limite ou inventa |
| C — irrelevante | Documento real sobre outro assunto | Trecho de fonte legítima, sem relação com a pergunta | Usa o que não serve só porque está lá |
| D — conflitante | Dois documentos contraditórios | Trecho correto + variante alterada que contradiz o fato | Reporta o conflito ou escolhe em silêncio |

## Regras comuns

- A pergunta enviada ao agente é idêntica nas quatro condições; só o contexto muda.
- Parâmetros de decodificação fixos e iguais em todas as execuções.
- Mesmo número de repetições por pergunta em todas as condições.
- Toda saída bruta é salva em `evidencias/<condição>/` antes de qualquer pontuação.
