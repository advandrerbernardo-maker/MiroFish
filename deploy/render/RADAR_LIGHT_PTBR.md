# RADAR 80/20 | Modo leve, sem OASIS

Este modo alternativo **não reproduz a simulação de agentes original do MiroFish**. Ele é uma análise documental com Gemini, com consulta opcional de leitura a um grafo existente no Zep. Os dados do Zep são exibidos em separado e **não** entram como evidência histórica.

## Acesso

Após o deploy no Render, usar `https://mirofish-radar-8020.onrender.com/radar-light.html`, com a autenticação HTTP Basic já configurada. Também há um atalho na página inicial.

1. Carregar `mirofish_treino_fcc_2022_2023.md` ou outro documento delimitado de até 64 KiB e 25 mil caracteres.
2. Se desejar, informar o identificador de um grafo Zep já existente. Não cria nem atualiza grafo e não executa OASIS.
3. Tocar em **Analisar com Gemini**. É realizada **uma solicitação** de classificação JSON (podendo haver uma negociação adicional caso o provedor não suporte o modo JSON).
4. Cada subassunto exibido precisa trazer um trecho de texto que realmente ocorra no arquivo carregado. O ranking apresentado é uma **hipótese qualitativa**.
5. Copiar os resultados em JSON e comparar, posteriormente, com uma prova reservada usando subassuntos fixados antes da avaliação.

## Limites metodológicos

- **Não mede taxa de acerto, probabilidade, frequência real de cobrança ou 80/20 estatístico**. Esses indicadores só podem ser calculados após individualização verificável das questões.
- Os trechos são verificados por correspondência de texto, mas isso não transforma a classificação do Gemini em gabarito oficial.
- Os documentos devem ter a procedência confirmada pelo pesquisador. A validação da fonte não é automática.
- Não consulta provas de 2025 nem outros dados externos: o prompt orienta a análise somente do arquivo recebido.
- A semelhança com o MiroFish se limita ao aproveitamento de sua infraestrutura de IA e Zep. O modo leve não tem OASIS, agentes interagindo, rodadas ou relatório social.
- É permitido `.md`, `.markdown`, `.txt` em UTF-8; PDF não é suportado neste modo para limitar memória.
- O arquivo não é salvo pela nova rota. O Gemini recebe o conteúdo para processar; aplicam-se as condições de uso e a cota da API contratada.
- O Render Free tem armazenamento efêmero e RAM limitada; o modo leve evita intencionalmente a biblioteca OASIS, que anteriormente causou OOM.

## Endpoints

- `GET /api/radar-light/status`
- `POST /api/radar-light/analyze` com `multipart/form-data`:
  - `arquivo`: arquivo .md, .markdown ou .txt de até 64 KiB
  - `graph_id`: opcional (leitura sem mutação)

Credenciais devem permanecer exclusivamente nas variáveis secretas do Render.
