# Importación controlada
Los CSV de examples son fichas de ejemplo con datos ficticios, no un formato de importación garantizado para todos los módulos. No contienen datos personales reales ni claves de licencias.
1. Definir identificador único por activo y separar modelos, ubicaciones y responsables.
2. Descargar/consultar la plantilla del importador nativo8.8.0 y mapear columnas explícitamente.
3. Crear catálogos necesarios o confirmar cómo los crea el importador. No asumir campos o estados por su nombre.
4. Respaldar antes de importar en una instancia con datos.
5. Ensayar2-5 filas ficticias en staging; comprobar modelo, categoría, etiqueta, fecha, moneda y responsable.
6. Detectar etiquetas duplicadas y series incompletas antes de cargar el lote real. No importar nuevamente un lote sin decidir si actualiza o crea.
7. Registrar archivo original, fecha, mapeo, operador, resultado y errores. Restringir acceso si contiene datos personales.
8. Confirmar mediante inventario físico; una importación exitosa no prueba que los equipos existan o estén en la ubicación indicada.

No hay sincronizador Odoo ni colector de hardware instalado. Para migraciones, exportar desde origen y preparar un mapeo revisado; SQL de Odoo no se restaura directamente en Snipe-IT.
