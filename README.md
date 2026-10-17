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
