# Política de tratamiento de datos personales — Activos (Snipe-IT) (Hefesto Studio)

Estado: vigente desde 2026-10-20. Responsable del tratamiento: el cliente que
opera el kit. Este documento describe qué datos guarda el kit, por qué, cuánto
tiempo los retiene y cómo se ejercen los derechos del titular (Ley 21.719).

## 1. Qué datos guarda este kit

El kit de activos (Snipe-IT) guarda, por persona:

- **Personas usuarias**: nombre, correo, **RUT** cuando la empresa lo exige,
  teléfono y cargo.
- **Asignación de activos**: quién tiene cada equipo, desde cuándo y el
  historial de traspasos (tracking).
- **Cuentas de la aplicación**: usuario, hash de contraseña, rol y estado.
- **Archivos y documentos**: archivos adjuntos a los activos (por ejemplo,
  facturas, garantías o certificados), que pueden contener datos de terceros.
- **Copias locales de respaldo**: `backups/<timestamp>/` con el dump de MariaDB
  (`database.sql`), el almacenamiento (`storage.tar.gz`) y la configuración.

El histórico de asignaciones es el registro más sensible: dice qué equipo tuvo
cada persona y en qué fechas.

## 2. Qué datos NO guarda este kit

- El `.env` **no** se copia en claro al respaldo: solo sus nombres de variable
  (`env.vars`) y, si hay un receptor `age` configurado, el `.env` cifrado
  (`env.age`). Ver `docs/CONTRATO-RESPALDO.md`, regla 5.
- El kit no guarda datos bancarios ni el historial de不详 payroll del personal.

## 3. Base legal y deberes

- **Minimización**: el kit guarda la asignación porque es el propósito del inventario. No se duplican datos de RR.HH. ni de planillas: si el RUT es necesario para el traspaso, es el que la empresa ya trata.
- **Finalidad**: inventariar los activos de la empresa y registrar su custodia. Los datos no se usan para otros fines ni se ceden a terceros.
- **Seguridad**: los respaldos se cifran en reposo hacia el destino del
  operador, la clave privada no está en este servidor y el `.env` nunca sale
  en claro.
- **Auditoría**: cada respaldo y cada restauración dejan registro en
  `logs/restore.log` con origen, sha256 verificado, destino y resultado. Es
  registro de actividades de tratamiento: no guarda valores de secretos.

## 4. Retención

| Dato | Dónde | Retención por defecto | Quién lo borra |
|---|---|---|---|
| Personas usuarias y RUT | MariaDB (volumen de base de datos) | mientras la cuenta exista; el RUT según la política de la empresa | el operador, desde la interfaz |
| Asignaciones e historial | MariaDB (volumen de base de datos) | según la política de la empresa | el operador |
| Archivos y documentos | volumen `/var/lib/snipeit` (`storage.tar.gz`) | mientras el activo exista | el operador |
| Cuentas de la aplicación | MariaDB (volumen de base de datos) | mientras la cuenta exista | el operador |
| Respaldos en disco | `backups/<timestamp>/` | **a definir por el operador**; el kit no borra nada por su cuenta | el operador |
| Registro de auditoría | `logs/restore.log` | append-only; se trunca por política del cliente | el operador |

**El kit no borra respaldos ni datos por su cuenta.** Borrar es una decisión del
operador, porque un respaldo borrado no se recupera.

## 5. Derechos del titular (acceso, rectificación y supresión)

1. **Acceso**: entregar los datos de un titular concreto desde la interfaz del
   kit o desde el dump de la base.
2. **Rectificación**: corregir los datos desde la interfaz del kit.
3. **Supresión**: eliminar el registro y dejar constancia de la supresión en el
   registro de auditoría.
4. **Revocación del consentimiento**: si el tratamiento depende del
   consentimiento, eliminar el registro.

El kit garantiza que los datos son localizables, corregibles y borrables; el
cliente es quien conoce la identidad de los titulares.

## 6. Verificación

- `bats tests/backup_restore.bats` comprueba, con datos sintéticos, que el
  `.env` no queda en claro, que el manifiesto lleva las cinco claves, que un
  artefacto alterado se rechaza y que un destino no vacío aborta la
  restauración.
- `gitleaks` corre en CI sobre el repositorio y su historial.
