# Respaldo y recuperación
Ejecutar `python3 scripts/backup.py` en el contexto Compose real de la instancia. Detiene app (incluido scheduler), vuelca SQL, comprime /var/lib/snipeit y copia .env/compose.yaml. Genera manifest.json con checksums y estado completed; intenta reiniciar app incluso si falla. La parada interrumpe acceso: programar ventana y verificar estado al finalizar.

Si hay integraciones externas que escriben directamente en DB/archivos, detenerlas antes. No usar una carpeta con otro nombre de proyecto para respaldar un recurso de Coolify: confirmar contexto y volúmenes. El script se detiene si no detecta app activa.

Cifrar y copiar fuera del VPS. No se automatiza almacenamiento remoto, cifrado, rotación ni cron. Conservar APP_KEY: protege datos cifrados y no debe regenerarse en una mudanza. Los respaldos pueden contener claves, personas y documentos.

## Restaurar en destino nuevo
1. Usar este paquete/imagen8.8.0 y revisar manifest completed/checksums con SHA-256.
2. Recuperar .env original con permiso0600. Para pruebas usar nombres de proyecto y volúmenes NUEVOS, preservando APP_KEY y contraseñas.
3. `docker compose up -d db`; esperar healthy. Verificar que snipeit está vacía. No sobrescribir una instancia con datos.
4. `docker compose exec -T db sh -c 'MYSQL_PWD="$MARIADB_PASSWORD" mariadb -u "$MARIADB_USER" "$MARIADB_DATABASE"' < /ruta/respaldo/database.sql`
5. `docker compose run --rm --no-deps -T --entrypoint tar app -xzf - -C /var/lib/snipeit < /ruta/respaldo/storage.tar.gz`
6. Revisar SMTP, integraciones y red antes de iniciar una copia de pruebas para evitar notificaciones duplicadas. Arrancar bootstrap privado y confirmar usuarios, equipos, historial, asignaciones y adjuntos.
7. Ajustar ASSETS_HOST, publicar HTTPS y completar aceptación. En migración definitiva detener origen, respaldar estado final y mover DNS cuando destino esté verificado.

No iniciar app antes de importar: su entrada ejecuta migraciones. Las instrucciones son para respaldos propios confiables. No extraer archivos desconocidos ni ejecutar down -v sobre datos reales.

## Actualización
Leer notas oficiales, respaldar, validar en staging y después actualizar imagen. Una migración puede impedir rollback cambiando solo la imagen: restaurar base/archivos compatibles. Conservar registro de versiones y módulos/integraciones.

## Traspaso
Entregar repositorio, dominio/DNS, acceso VPS/Coolify, versiones/digests, volúmenes, APP_KEY, secretos DB, administrador y recuperación MFA, SMTP si está configurado, respaldo probado, catálogos y procedimientos. Transferir secretos aparte mediante gestor seguro. Acordar responsable, retención, soporte y revocación de accesos temporales.
