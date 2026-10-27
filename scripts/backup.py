#!/usr/bin/env python3
"""Respaldo del kit hefesto-activos (Snipe-IT + MariaDB).

El .env nunca se copia en claro: al respaldo solo van sus nombres (env.vars) y,
si hay receptor age, el .env cifrado (env.age). El manifiesto lleva las cinco
claves del contrato. Ver docs/CONTRATO-RESPALDO.md.

El respaldo contiene datos de personas (asignaciones nominales) y documentos
adjuntos a los activos: cifrar antes de moverlo.
"""
import datetime
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from respaldo_contrato import (escribir_manifiesto, ejecutar,  # noqa: E402
                               exportar_env, marcar_fallido)

SOFTWARE = 'hefesto-activos'
VERSION = '8.8.0'
DATABASE = 'mariadb'
CONFIG = ['compose.yaml']


def dc(*args, **kw):
    return subprocess.run(['docker', 'compose', *args], check=True, **kw)


def main():
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    os.umask(0o077)
    if not (root / '.env').is_file():
        raise SystemExit('Falta .env')
    if not dc('ps', '--status', 'running', '-q', 'app',
              capture_output=True, text=True).stdout.strip():
        raise SystemExit('app no esta activa en este contexto Compose; '
                         'revisar recurso/proyecto.')
    folder = root / 'backups' / datetime.datetime.now(datetime.timezone.utc).strftime(
        '%Y%m%dT%H%M%S%fZ')
    folder.mkdir(parents=True, mode=0o700)
    try:
        dc('stop', 'app')
        with (folder / 'database.sql').open('wb') as out:
            dc('exec', '-T', 'db', 'sh', '-c',
               'MYSQL_PWD="$MARIADB_PASSWORD" mariadb-dump -u "$MARIADB_USER" '
               '--single-transaction --skip-lock-tables --no-tablespaces "$MARIADB_DATABASE"',
               stdout=out)
        with (folder / 'storage.tar.gz').open('wb') as out:
            dc('run', '--rm', '--no-deps', '-T', '--entrypoint', 'tar', 'app',
               '-czf', '-', '-C', '/var/lib/snipeit', '.', stdout=out)
        for n in CONFIG:
            shutil.copy2(root / n, folder / n)
        meta = exportar_env(root, folder)
        escribir_manifiesto(folder, SOFTWARE, VERSION, DATABASE, extra=meta)
    except BaseException:
        marcar_fallido(folder, SOFTWARE, VERSION, DATABASE)
        raise
    finally:
        dc('start', 'app')
    print('Respaldo completo:', folder)
    print('El .env no viaja en claro: solo env.vars y, si hay receptor age, env.age.')
    print('Contiene claves de personas y documentos: cifrar antes de copiar fuera.')
    return 0


if __name__ == '__main__':
    raise SystemExit(ejecutar(main))
