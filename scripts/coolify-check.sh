#!/usr/bin/env bash
# Valida que compose.yaml cumple el contrato del plan B (rama coolify).
# - Punto 1 del contrato: se valida en el render con jq (claves prohibidas
#   como ports, container_name, privileged, etc.).
# - Punto 2 del contrato: se valida en el source con Python+PyYAML (claves
#   'name:' declaradas en raiz, networks o volumes). Compose autocompleta
#   nombres al renderizar, por eso el chequeo source distingue declaracion
#   explicita de autocompletado.
# Falla con "servicio: motivo" si algo no cumple.
set -euo pipefail

cd "$(dirname "$0")/.."

COMPOSE_FILE="compose.yaml"
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT
ENV_FILE="$WORK_DIR/.env"

# Variables detectadas en compose.yaml. Las de host/URL usan ejemplo.invalid;
# el resto, valores ficticios no secretos (no se usan en este script).
cat > "$ENV_FILE" <<EOF
COMPOSE_PROJECT_NAME=hefesto-activos-test
DB_VOLUME=hefesto-activos-test-db
STORAGE_VOLUME=hefesto-activos-test-storage
ASSETS_HOST=ejemplo.invalid
APP_KEY=base64:dGVzdC1rZXktbm90LWEtcmVhbC1zZWNyZXQtdGVzdC1rZXktbm90LWEtcmVhbC1zZWNyZXQ=
DB_PASSWORD=x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd
DB_ROOT_PASSWORD=x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd
APP_TRUSTED_PROXIES=10.0.0.0/8
SMTP_HOST=ejemplo.invalid
SMTP_PORT=587
SMTP_USERNAME=null
SMTP_PASSWORD=null
MAIL_FROM=activos@ejemplo.invalid
EOF

# Render del compose (sin secretos reales; valores ficticios no secretos).
RENDER_JSON=$(docker compose --project-directory . \
  -f "$COMPOSE_FILE" --env-file "$ENV_FILE" \
  config --format json)

fail() { echo "$1"; exit 1; }

# --- Punto 1 del contrato: nada que salte Traefik ni dé poder sobre el host
# (en servicios sin profiles).
SERVICES=$(echo "$RENDER_JSON" | jq -r '
  .services
  | to_entries[]
  | select((.value.profiles // []) | length == 0)
  | .key')

for svc in $SERVICES; do
  svc_json=$(echo "$RENDER_JSON" | jq ".services[\"$svc\"]")

  for forbidden in ports container_name privileged cap_add devices; do
    if echo "$svc_json" | jq -e "has(\"$forbidden\")" >/dev/null; then
      fail "$svc: clave prohibida '$forbidden' (clausula 1)"
    fi
  done

  for k in network_mode pid ipc; do
    val=$(echo "$svc_json" | jq -r ".\"$k\" // empty")
    if [ "$val" = "host" ]; then
      fail "$svc: $k=host es prohibido (clausula 1)"
    fi
  done

  if echo "$svc_json" | jq -e '
      .security_opt // []
      | type == "array"
      and any(
        if type == "string" then test("unconfined")
        else false end
      )' >/dev/null; then
    fail "$svc: security_opt con unconfined (clausula 1)"
  fi

  # Bind a docker.sock en cualquier forma (string u objeto).
  if echo "$svc_json" | jq -e '
      .volumes // []
      | type == "array"
      and any(
        if type == "string" then test("docker\\.sock")
        elif type == "object" then ((.source // "") | test("docker\\.sock"))
                            or ((.target // "") | test("docker\\.sock"))
        else false end
      )' >/dev/null; then
    fail "$svc: bindea docker.sock (clausula 1)"
  fi
done

# --- Punto 2 del contrato: nombres declarados sin forzar.
# Chequeo source-level: Compose autocompleta nombres aun cuando el YAML no
# los declara, asi que mirar el render no sirve para distinguirlos.
python3 - "$COMPOSE_FILE" <<'PY' || exit 1
import sys, re, yaml

src_path = sys.argv[1]
doc = yaml.safe_load(open(src_path)) or {}
fails = []

# Patron estricto: solo se permite un name de volumen que sea EXACTAMENTE
# una interpolacion con default (${VAR:-default}). Cualquier otra forma
# (literal, ${VAR:?}, ${VAR} o substrings como "foo${X:-bar}baz") fuerza al
# operador a configurar variables en Coolify.
DEFAULT_NAME_RE = re.compile(r'^\$\{[A-Za-z_][A-Za-z0-9_]*:-[^\s}]+\}\Z')

if 'name' in doc and isinstance(doc['name'], str) and doc['name']:
    fails.append(f"compose: 'name' raiz fijado a '{doc['name']}' (clausula 2; Coolify pone el nombre de proyecto)")

for nkey, nval in (doc.get('networks') or {}).items():
    if isinstance(nval, dict) and nval.get('name'):
        fails.append(f"compose: network '{nkey}' con name fijado a '{nval['name']}' (clausula 2)")

for vkey, vval in (doc.get('volumes') or {}).items():
    if isinstance(vval, dict) and vval.get('name'):
        vname = vval['name']
        if not (isinstance(vname, str) and DEFAULT_NAME_RE.fullmatch(vname)):
            fails.append(
                f"compose: volumen '{vkey}' con name fijado a '{vname}' sin default (clausula 2)"
            )

if fails:
    print('\n'.join(fails))
    sys.exit(1)
PY

echo "OK: compose.yaml cumple puntos 1 y 2 del contrato (servicios sin profiles)"