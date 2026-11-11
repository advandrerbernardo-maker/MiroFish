# MiroFish + RADAR 80/20 | Implantação no Render

Este pacote mantém o Dockerfile original intacto. O arquivo `Dockerfile.render` compila o frontend e hospeda a API Flask sob proxy Nginx, numa única porta e protegido por HTTP Basic.

## Deploy separado do DBOT

1. Criar um **novo Web Service** no Render usando o fork `advandrerbernardo-maker/MiroFish`, com runtime **Docker** e Dockerfile Path `./Dockerfile.render`.
2. Usar a branch `main` somente após revisão e merge desta PR, ou a branch `feat/render-radar-secure-deploy` para testes.
3. Verificar o custo e a memória do plano. O MiroFish pode não caber no plano gratuito. Não contratar serviço pago sem autorização.
4. Em **Environment**, cadastrar as variáveis abaixo. **Não publicar segredos no GitHub nem enviá-los no chat.**
5. Verificar `/__health` (200, verifica somente o proxy); `/` e `/api/` sem senha devem solicitar autenticação (401).
6. Fazer um teste mínimo de chamada Gemini e Zep antes de iniciar uma simulação. Verificar logs e limites de uso.

## Variáveis do Render

| Nome | Valor |
|---|---|
| `LLM_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| `LLM_MODEL_NAME` | `gemini-2.5-flash` (confirmar compatibilidade) |
| `LLM_API_KEY` | chave **secreta** do Google AI Studio, somente no Render |
| `ZEP_API_KEY` | chave **secreta** do Zep, somente no Render |
| `MIROFISH_USER` | nome de acesso (3 a 64 caracteres) |
| `MIROFISH_PASSWORD` | senha exclusiva (mínimo 16 caracteres), somente no Render |
| `OASIS_DEFAULT_MAX_ROUNDS` | `3` para teste inicial |
| `FLASK_DEBUG` | `False` |

A primeira simulação RADAR deve receber apenas os 20 registros de treinamento de Direito Civil e Processo Civil das provas DPE-AM 2022/2023. **Não enviar questões de 2025 nem o edital de 2026 ao experimento retrospectivo.** Registrar as recomendações antes de abrir a amostra de teste.

## Cuidados

- O código original tem licença AGPL-3.0. Respeitar suas condições de distribuição e uso em rede.
- A proteção HTTP Basic não é uma auditoria completa de segurança.
- Serviços sem armazenamento persistente podem perder arquivos e simulações em reinícios.
- O Gemini oferece API com formato compatível ao OpenAI SDK, mas o funcionamento real com JSON e o motor OASIS do MiroFish ainda deve ser testado.
- Não existe instalação em produção nem previsão calculada até concluir o deploy e os testes.
