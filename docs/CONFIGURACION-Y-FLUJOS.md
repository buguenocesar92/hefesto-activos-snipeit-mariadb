# Configuración funcional
## Catálogos
1. Empresa y datos generales; idioma, zona horaria y moneda predeterminada CLP cuando corresponda.
2. Ubicaciones y departamentos.
3. Categorías (notebook, monitor, teléfono), fabricantes y modelos.
4. Estados: disponible, asignable, en reparación y baja según equivalencias nativas; definir cuáles permiten asignar.
5. Personas responsables con cuentas y permisos mínimos; no crear superadministradores para usuarios comunes.
6. Proveedores, compra, garantía y mantenimiento cuando se disponga de evidencia.

Mantener etiqueta patrimonial única por unidad, diferente del número de serie del fabricante. Ejemplo HFS-NB-0001. No reutilizar etiquetas de bienes dados de baja.

## Flujo de equipo
Recepción → revisar serie/modelo/estado → registrar compra y garantía → etiquetar → asignar al responsable → confirmar recepción según procedimiento → registrar mantenimiento si corresponde → devolución/check-in → revisar condición → reasignación o baja autorizada.

Antes de entregar, revisar físicamente accesorios y estado. La devolución debe quedar registrada: modificar solo un comentario no sustituye el check-in. No marcar como disponible un equipo aún asignado.

## Licencias y accesorios
Registrar asientos de licencias y vencimientos de acuerdo con el contrato real; asignar/devolver según comportamiento nativo. No guardar credenciales de cuentas dentro de nombres o notas. Consumibles y accesorios tienen flujos distintos a los activos con número de serie; no forzarlos a una misma tabla.

## Auditoría física
Crear campaña con ubicación, lista esperada y responsable. Comparar etiqueta/serie/responsable con equipo físico, registrar diferencias y resolverlas con autorización. No eliminar registros para esconder diferencias. Una auditoría de inventario no equivale a auditoría de seguridad o legal.

## Permisos
Propuesta: administrador técnico, gestor de inventario, auditor de consulta y usuario receptor. Configurar grupos nativos, validar lectura/escritura/exportación y limitar acceso a datos personales. Las restricciones entre empresas deben probarse; para entregas con administradores independientes preferir despliegues separados.

## Etiquetas
Usar generador nativo de códigos de barras/QR. Probar tamaño, impresora y lectura de una etiqueta antes de imprimir un lote. El enlace QR debe requerir la autenticación apropiada; no incrustar datos personales o credenciales dentro del código. No se incluyen impresora ni consumibles.
