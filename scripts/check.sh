#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose version
docker compose config --quiet
docker compose ps
printf 'Continuar con docs/ACEPTACION.md; healthy no equivale a aceptacion funcional.\n'
