#!/usr/bin/env python3
import datetime,hashlib,json,os,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1];os.chdir(root);os.umask(0o077)
def dc(*args,**kw):return subprocess.run(['docker','compose',*args],check=True,**kw)
if not (root/'.env').is_file():raise SystemExit('Falta .env')
if not dc('ps','--status','running','-q','app',capture_output=True,text=True).stdout.strip():raise SystemExit('app no esta activa en este contexto Compose; revisar recurso/proyecto.')
folder=root/'backups'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');folder.mkdir(parents=True)
try:
    dc('stop','app')
    with (folder/'database.sql').open('wb') as out:
        dc('exec','-T','db','sh','-c','MYSQL_PWD="$MARIADB_PASSWORD" mariadb-dump -u "$MARIADB_USER" --single-transaction --skip-lock-tables --no-tablespaces "$MARIADB_DATABASE"',stdout=out)
    with (folder/'storage.tar.gz').open('wb') as out:
        dc('run','--rm','--no-deps','-T','--entrypoint','tar','app','-czf','-','-C','/var/lib/snipeit','.',stdout=out)
    for name in ['.env','compose.yaml']:(folder/name).write_bytes((root/name).read_bytes())
    hashes={}
    for name in ['database.sql','storage.tar.gz','.env','compose.yaml']:
        with (folder/name).open('rb') as stream:hashes[name]=hashlib.file_digest(stream,'sha256').hexdigest()
    (folder/'manifest.json').write_text(json.dumps({'version':'8.8.0','status':'completed','sha256':hashes},indent=2))
finally:
    dc('start','app')
print(f'Respaldo completo: {folder}. Contiene claves y documentos: cifrar y copiar fuera del VPS.')
