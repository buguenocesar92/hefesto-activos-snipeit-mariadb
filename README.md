# Hefesto Activos · Snipe-IT 8.8.0
Paquete para gestionar patrimonio tecnológico: equipos individualizados, responsables, ubicaciones, asignaciones/devoluciones, garantías, licencias y accesorios. Permite vender implementación, carga inicial, etiquetado, capacitación y mantenimiento.

## Stack
Imagen Docker oficial snipe/snipe-it:8.8.0 fijada por digest, MariaDB11.4 y HTTPS mediante Coolify. Persistencia en /var/lib/snipeit para archivos, respaldos internos y claves, además del volumen MariaDB. El proceso programado de Laravel está incluido en la imagen oficial mediante Supervisor; no añadir otro cron duplicado.

No usa Supabase: Snipe-IT trabaja aquí con su motor MariaDB nativo. No incluye integración Odoo ni conversor automático. Se recomienda instancia separada por cliente si tendrá administración propia.

## Estado real
Paquete de despliegue y documentación revisado estáticamente. Docker, alta inicial, importación, notificaciones, etiquetas y recuperación no han sido probados en un servidor desde este entorno. No hay usuarios reales, credenciales de proveedor ni equipos cargados.

## Inicio
Requisitos: Docker Compose v2, Python3.11+ para scripts, DNS/HTTPS y VPS.
1. `python3 scripts/configure.py cliente-demo activos.tudominio.cl`
2. En el VPS: `docker compose -f compose.yaml -f compose.bootstrap.yaml up -d`
3. Desde tu computador: `ssh -L 8000:127.0.0.1:8000 usuario@IP_DEL_VPS`
4. Abrir http://127.0.0.1:8000 y completar el asistente nativo. Crear administrador único y guardar contraseña/MFA de forma segura.
5. Seguir docs/COOLIFY.md para publicar la instancia ya inicializada sin cambiar volúmenes ni APP_KEY.
6. Configurar catálogos, importar una muestra y ejecutar docs/ACEPTACION.md antes de operar.

No publicar el asistente inicial en Internet. La instalación crea la cuenta administradora desde la interfaz privada; este ZIP no contiene una contraseña predeterminada de aplicación.

## Contenido
Compose de producción y bootstrap, generador de secretos, respaldo de SQL y archivos, guías de recuperación/traspaso, inventario inicial en CSV, flujo operativo, plantillas de actas y propuesta de servicio.

Docker descarga la aplicación; este ZIP no contiene sus binarios. Los ejemplos CSV requieren mapeo y validación en el importador nativo. No representan registros ya importados.

## Alcance
Control de activos TI, no punto de venta, contabilidad, descubrimiento automático de red ni agente que inventarie computadores por sí solo. No incluye SII, firma electrónica, compras automáticas o integración con Odoo. La aceptación de entrega nativa no equivale por sí sola a una firma electrónica cualificada.

## Operación y licencia
Inicio orientativo para pocos usuarios:2vCPU,2GB RAM y20GB SSD más documentos/respaldo; medir carga y retención. Snipe-IT mantiene AGPL-3.0 y sus atribuciones. Respetar obligaciones al modificar, redistribuir u ofrecer versiones modificadas por red. Hefesto cobra implementación y servicio, sin atribuirse autoría del software upstream.

## Despliegue en Coolify (MVP Hefesto)

Coolify levanta este compose detrás de Traefik con TLS. Las únicas variables que Coolify debe inyectar son las del runtime (`ASSETS_HOST`, `APP_KEY`, `DB_PASSWORD`, `DB_ROOT_PASSWORD` y, opcionalmente, `APP_TRUSTED_PROXIES`, `SMTP_*` y `MAIL_FROM`). El nombre del proyecto y los volúmenes los pone Coolify automáticamente.

- **Volúmenes, datos previos y migraciones.** Los volúmenes `database` y `storage` ya no tienen `name:` declarado, así que Coolify los crea con su prefijo de proyecto (`<proyecto>_database` y `<proyecto>_storage`). Esto rompe el uso original: `scripts/configure.py` sigue generando `DB_VOLUME` y `STORAGE_VOLUME` con los nombres `hefesto-activos-<slug>-db` y `hefesto-activos-<slug>-storage`, y esos valores los ignora el compose. En una instalación previa hay que mover los datos de los volúmenes viejos a los nuevos antes de arrancar (por ejemplo, restaurar un respaldo de `scripts/backup.py` o copiar `/var/lib/mysql` y `/var/lib/snipeit` con los contenedores apagados), si no la instancia quedará vacía.
- **Asistente web en Coolify.** Como `compose.bootstrap.yaml` no lo usa Coolify, ese primer paso ya no se hace por SSH al `127.0.0.1:8000`. Flujo correcto: desplegar sin asignarle dominio a `app`; completar el asistente nativo por túnel SSH hacia la IP interna del contenedor (o asignar el dominio agregándole una restricción temporal de IP o basic-auth en Traefik hasta cerrar el asistente); recién entonces exponer el dominio. Si el dominio queda activo antes de cerrar el asistente, queda público en Internet.
- **`APP_TRUSTED_PROXIES`** tiene default `10.0.0.0/8,172.16.0.0/12`. Cubre el CIDR que suele asignarle Coolify a su red interna y el pool por defecto de Docker, donde cae la IP del contenedor de Traefik que hace de proxy inverso. Es seguro en este compose porque `app` no publica puertos: solo lo alcanzan contenedores de redes Docker internas, así que los encabezados `X-Forwarded-For`/`X-Forwarded-Proto` llegan únicamente desde Traefik. En producción conviene acotarlo, opcionalmente, al CIDR exacto de la red `coolify` para reducir la superficie.
- **SMTP** apunta por defecto a `127.0.0.1:2525` sin servidor: la instancia inicia pero no entrega correo. Configurar `SMTP_HOST`/`SMTP_PORT`/`SMTP_USERNAME`/`SMTP_PASSWORD`/`MAIL_FROM` con los datos del proveedor antes de habilitar invitaciones y recuperaciones.
