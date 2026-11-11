#!/usr/bin/env bash
set -euo pipefail

: "${LLM_API_KEY:?Cadastre LLM_API_KEY como secret no Render}"
: "${ZEP_API_KEY:?Cadastre ZEP_API_KEY como secret no Render}"
: "${MIROFISH_USER:?Cadastre MIROFISH_USER no Render}"
: "${MIROFISH_PASSWORD:?Cadastre MIROFISH_PASSWORD como secret no Render}"

if [[ ! "$MIROFISH_USER" =~ ^[a-zA-Z0-9._-]{3,64}$ ]]; then
  echo 'MIROFISH_USER deve ter de 3 a 64 caracteres (letras, números, . _ -)' >&2
  exit 1
fi
if [[ ${#MIROFISH_PASSWORD} -lt 16 ]]; then
  echo 'MIROFISH_PASSWORD precisa ter pelo menos 16 caracteres' >&2
  exit 1
fi

export PORT="${PORT:-10000}"
export LLM_BASE_URL="${LLM_BASE_URL:-https://generativelanguage.googleapis.com/v1beta/openai/}"
export LLM_MODEL_NAME="${LLM_MODEL_NAME:-gemini-2.5-flash}"
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5001
export FLASK_DEBUG=False
export SECRET_KEY="${SECRET_KEY:-$(python3 -c 'import secrets; print(secrets.token_hex(32))')}"

# Senha lida por stdin: não expor segredo na lista de processos.
printf '%s\n' "$MIROFISH_PASSWORD" | htpasswd -icB /etc/nginx/.mirofish_htpasswd "$MIROFISH_USER" >/dev/null
# O envsubst modifica somente PORT, preservando as variáveis internas do Nginx.
envsubst '${PORT}' < /etc/nginx/templates/mirofish.conf.template > /etc/nginx/sites-enabled/default
nginx -t

cd /app/backend
/app/backend/.venv/bin/gunicorn --workers 1 --threads 4 --timeout 600 --bind 127.0.0.1:5001 'app:create_app()' &
backend_pid=$!
nginx -g 'daemon off;' &
nginx_pid=$!

shutdown() {
  kill -TERM "$backend_pid" "$nginx_pid" 2>/dev/null || true
  wait "$backend_pid" "$nginx_pid" 2>/dev/null || true
}
trap shutdown EXIT TERM INT
wait -n "$backend_pid" "$nginx_pid"
