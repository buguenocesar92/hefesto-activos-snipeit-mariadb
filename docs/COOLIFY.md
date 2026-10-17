# Publicación
## Preparación privada
Usar bootstrap y túnel del README. La base inicia primero y el entrypoint nativo aplica migraciones. Completar asistente, empresa y administrador. No incorporar usuarios/equipos reales hasta probar acceso y permisos. Activar MFA según las opciones nativas y guardar recuperación.

## Publicar
1. Detener bootstrap: `docker compose -f compose.yaml -f compose.bootstrap.yaml down` SIN `-v`.
2. Subir archivos versionables al repositorio privado, excluyendo .env y backups.
3. Crear recurso Docker Compose usando compose.yaml. Copiar variables generadas al editor seguro de Coolify; conservar APP_KEY, claves DB y nombres de volúmenes exactamente.
4. Configurar ASSETS_HOST=activos.cliente.cl. Asignar https://activos.cliente.cl al servicio app, puerto80. No publicar db ni puertos de bootstrap.
5. Configurar APP_TRUSTED_PROXIES con la IP/CIDR real del proxy cuando corresponda; evitar confiar indiscriminadamente en cualquier origen. Coolify debe conservar Host y protocolo HTTPS.
6. Desplegar y revisar URL, login, cookies seguras, imágenes, adjuntos y persistencia. Si vuelve a aparecer el asistente, retirar el dominio y verificar que se utilizan los volúmenes preparados.

El healthcheck valida respuesta HTTP, no instalación completa ni permisos. El scheduler de la imagen corre cada minuto; verificar su estado y logs en la aceptación. No duplicarlo con n8n/cron externo.

## Correo
Por defecto apunta a127.0.0.1:2525 sin servidor: no entrega mensajes; invitaciones, aceptación por correo y restablecimientos pueden fallar. Configurar SMTP_HOST/PORT/USERNAME/PASSWORD y MAIL_FROM usando los datos reales del proveedor. Comprobar requisitos de transporte TLS con la documentación de esa versión. Mantener validación de certificados; no habilitar opciones inseguras para forzar conexión.

Probar desde ajustes nativos con un destinatario autorizado antes de habilitar envíos operativos. Este paquete no envía correos ni configura WhatsApp.

## Archivos
/var/lib/snipeit conserva uploads públicos/privados, claves y respaldos internos. Las imágenes públicas de modelos/logos no deben contener documentos confidenciales. Usar las funciones privadas adecuadas para adjuntos y verificar accesos directos sin sesión.

## Actualizaciones
BookStack de la entrega anterior y Snipe-IT son instancias independientes: no compartir sus bases o volúmenes. Esta imagen Snipe-IT está fijada por digest. MariaDB está en rama11.4; registrar digest desplegado y probar cambios antes de actualizar.
