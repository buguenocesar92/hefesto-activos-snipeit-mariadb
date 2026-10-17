#!/usr/bin/env python3
import os,sys,re,secrets,base64
from pathlib import Path
if len(sys.argv)!=3 or not re.fullmatch(r'[a-z][a-z0-9-]{2,39}',sys.argv[1]) or not re.fullmatch(r'(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}',sys.argv[2]):
    raise SystemExit('Uso: python3 scripts/configure.py cliente-demo activos.tudominio.cl')
root=Path(__file__).resolve().parents[1];slug=sys.argv[1]
values={'COMPOSE_PROJECT_NAME':f'hefesto-activos-{slug}','DB_VOLUME':f'hefesto-activos-{slug}-db','STORAGE_VOLUME':f'hefesto-activos-{slug}-storage','ASSETS_HOST':sys.argv[2], 'APP_KEY':'base64:'+base64.b64encode(secrets.token_bytes(32)).decode(),'DB_PASSWORD':secrets.token_hex(32),'DB_ROOT_PASSWORD':secrets.token_hex(32)}
try:fd=os.open(root/'.env',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
except FileExistsError:raise SystemExit('.env ya existe; no se modifico.')
with os.fdopen(fd,'w') as f:
    for k,v in values.items():f.write(f'{k}={v}\n')
print('.env creado. Conservar APP_KEY y secretos en gestor seguro; no subir a Git.')
